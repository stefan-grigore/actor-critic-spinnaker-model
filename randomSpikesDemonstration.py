import pyNN.spiNNaker as sim
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt
import threading
from random import uniform
from time import sleep
from pykeyboard import PyKeyboard

sim.setup(timestep=1.0)
sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 100)

input1 = sim.Population(6, sim.external_devices.SpikeInjector(), label="stateSpikeInjector")

pre_pop = sim.Population(6, sim.IF_curr_exp(tau_syn_E=100, tau_refrac=50), label="statePopulation")

post_pop = sim.Population(1, sim.IF_curr_exp(), label="actorPopulation")
sim.external_devices.activate_live_output_for(pre_pop, database_notify_host="localhost", database_notify_port_num=19996)
sim.external_devices.activate_live_output_for(input1, database_notify_host="localhost", database_notify_port_num=19998)

timing_rule = sim.SpikePairRule(tau_plus=20.0, tau_minus=20.0,
                                A_plus=0.5, A_minus=0.5)
weight_rule = sim.AdditiveWeightDependence(w_max=25.0, w_min=0.0)
stdp_model = sim.STDPMechanism(timing_dependence=timing_rule,
                               weight_dependence=weight_rule,
                               weight=2.0, delay=1)
stdp_projection = sim.Projection(pre_pop, post_pop, sim.OneToOneConnector(),
                                 synapse_type=stdp_model)
input_projection1 = sim.Projection(input1, pre_pop, sim.OneToOneConnector(),
                            synapse_type=sim.StaticSynapse(weight=5, delay=1))

pre_pop.record(["spikes", "v"])
post_pop.record(["spikes", "v"])
simtime = 100

k = PyKeyboard()


def receive_spikes(label, time, neuron_ids):
    try:
        for neuron_id in neuron_ids:
            if str(neuron_id) is '0':
                print 'press right'
                k.press_key(k.right_key)
            if str(neuron_id) is '1':
                print 'release right'
                k.release_key(k.right_key)
            if str(neuron_id) is '2':
                print 'press left'
                k.press_key(k.left_key)
            if str(neuron_id) is '3':
                print 'release left'
                k.release_key(k.left_key)
            if str(neuron_id) is '4':
                print 'press space'
                k.press_key(k.space)
            if str(neuron_id) is '5':
                print 'release space'
                k.release_key(k.space)
    except RuntimeError:
        pass


def send_spike(label, sender):
    print 'Sending spike'
    sender.send_spike(label, 0, send_full_keys=True)


live_spikes_connection = sim.external_devices.SpynnakerLiveSpikesConnection(
    receive_labels=["statePopulation"], local_port=19996, send_labels=None)

live_spikes_connection2 = sim.external_devices.SpynnakerLiveSpikesConnection(
    receive_labels=None, local_port=19998, send_labels=['stateSpikeInjector'])

live_spikes_connection.add_receive_callback("statePopulation", receive_spikes)

def send_spikes(id):
    sleep(12)
    while True:
        live_spikes_connection2.send_spike('stateSpikeInjector', id,
                                           send_full_keys=True)
        sleep(uniform(0, 3))


def send_random_right_press_spikes_thread():
    send_spikes(0)


def send_random_right_release_spikes_thread():
    send_spikes(1)


def send_random_left_press_spikes_thread():
    send_spikes(2)


def send_random_left_release_spikes_thread():
    send_spikes(3)


def send_random_jump_press_spikes_thread():
    send_spikes(4)


def send_random_jump_release_spikes_thread():
    send_spikes(5)


thread0 = threading.Thread(target=send_random_right_press_spikes_thread)
thread1 = threading.Thread(target=send_random_right_release_spikes_thread)
thread2 = threading.Thread(target=send_random_left_press_spikes_thread)
thread3 = threading.Thread(target=send_random_left_release_spikes_thread)
thread4 = threading.Thread(target=send_random_jump_press_spikes_thread)
thread5 = threading.Thread(target=send_random_jump_release_spikes_thread)

thread0.start()
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()

sim.run(13000)

neo = pre_pop.get_data(variables=["spikes", "v"])
spikes2 = neo.segments[0].spiketrains
v2 = neo.segments[0].filter(name='v')[0]

sim.end()

plot.Figure(
    plot.Panel(v2, ylabel="Membrane potential (mV)",
               data_labels=['controls'], yticks=True),
    plot.Panel(spikes2, yticks=True, markersize=5),
    title="Simple Example",
    annotations="Simulated with {}".format(sim.name())
)
plt.show()