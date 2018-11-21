import pyNN.spiNNaker as sim
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt
import threading
from time import sleep
from pykeyboard import PyKeyboard
import cv2
import numpy as np
import pyautogui
from datetime import datetime


sim.setup(timestep=1.0)
sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 100)

numberOfSteps = 3

input1 = sim.Population(numberOfSteps*4, sim.external_devices.SpikeInjector(), label="input1")

pre_pop = sim.Population(numberOfSteps*4, sim.IF_curr_exp(tau_syn_E=100, tau_refrac=50), label="pre_pop")
post_pop = sim.Population(numberOfSteps*4, sim.IF_curr_exp(tau_syn_E=25, tau_refrac=100), label="post_pop")

sim.external_devices.activate_live_output_for(pre_pop, database_notify_host="localhost", database_notify_port_num=19996)
sim.external_devices.activate_live_output_for(input1, database_notify_host="localhost", database_notify_port_num=19998)
sim.external_devices.activate_live_output_for(post_pop, database_notify_host="localhost", database_notify_port_num=20000)

timing_rule = sim.SpikePairRule(tau_plus=50.0, tau_minus=50.0,
                                A_plus=0.001, A_minus=0.001)
weight_rule = sim.AdditiveWeightDependence(w_max=5.0, w_min=-5.0)
stdp_model = sim.STDPMechanism(timing_dependence=timing_rule,
                               weight_dependence=weight_rule,
                               weight=2, delay=1)

stdp_projection = sim.Projection(pre_pop, post_pop, sim.OneToOneConnector(),
                                 synapse_type=stdp_model)
input_projection1 = sim.Projection(input1, pre_pop, sim.OneToOneConnector(),
                            synapse_type=sim.StaticSynapse(weight=5, delay=1))

pre_pop.record(["spikes", "v"])
post_pop.record(["spikes", "v"])

k = PyKeyboard()

step = 0
firedIndex = []


def execute_commands():
    global step, firedIndex
    try:
        print 'step: ' + str(step)
        time = datetime.time(datetime.now())
        commands = list(set(firedIndex))
        print 'no duplicates fireIndex ' + str(commands)
        commands.sort()
        print 'sorted fireIndex ' + str(commands)
        for neuron_id in commands:
            print 'doing ' + str(neuron_id)
            neuron_id %= 4
            if str(neuron_id) is '0':
                print str(time) + ' press right'
                k.press_key(k.right_key)
                sleep(1)
                print str(time) + ' release right'
                k.release_key(k.right_key)
            if str(neuron_id) is '1':
                print str(time) + ' press left'
                k.press_key(k.left_key)
                sleep(1)
                print str(time) + ' release left'
                k.release_key(k.left_key)
            if str(neuron_id) is '2':
                print str(time) + ' press space + right'
                k.press_key(k.space)
                k.press_key(k.right_key)
                sleep(1)
                print str(time) + ' release space + right'
                k.release_key(k.space)
                k.release_key(k.right_key)
            if str(neuron_id) is '3':
                print str(time) + ' press space + left'
                k.press_key(k.space)
                k.press_key(k.left_key)
                sleep(1)
                print str(time) + ' release space + left'
                k.release_key(k.space)
                k.release_key(k.left_key)
    except RuntimeError:
        pass


def receive_spikes(label, time, neuron_ids):
    global firedIndex
    try:
        print str(neuron_ids)
        for neuron_id in neuron_ids:
            print 'fired ' + str(neuron_id)
            firedIndex.append(neuron_id)
    except RuntimeError:
        pass


numberOfSpikes = 1


live_spikes_connection = sim.external_devices.SpynnakerLiveSpikesConnection(
    receive_labels=["post_pop"], local_port=20000, send_labels=None)

live_spikes_connection2 = sim.external_devices.SpynnakerLiveSpikesConnection(
    receive_labels=None, local_port=19998, send_labels=['input1'])

live_spikes_connection.add_receive_callback("post_pop", receive_spikes)


def send_spike(label, sender, index):
    sender.send_spike(label, index, send_full_keys=True)


initialWeights = stdp_projection.getWeights()

weightRight = []
weightLeft = []
weightJumpRight = []
weightJumpLeft = []


def press_key(key):
    k.press_key(key)
    sleep(0.2)
    k.release_key(key)
    sleep(0.2)


image = pyautogui.screenshot(region=(0, 200, 1250, 700))
image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
cv2.imwrite("screenCapture.png", image)
meatboy_image = cv2.imread('meatboy.png')
meatgirl_image = cv2.imread('meatgirl.png')
large_image = cv2.imread("screenCapture.png")
method = cv2.TM_SQDIFF_NORMED
result = cv2.matchTemplate(meatboy_image.astype(np.float32),
                           large_image.astype(np.float32), method)
result2 = cv2.matchTemplate(meatgirl_image.astype(np.float32),
                            large_image.astype(np.float32), method)
mn, _, mnLoc, _ = cv2.minMaxLoc(result)
mn2, _, mnLoc2, _ = cv2.minMaxLoc(result2)
MPx, MPy = mnLoc
MPx2, MPy2 = mnLoc2

xOffset = MPx2 - MPx
yOffset = MPy2 - MPy
# too low
if yOffset < 0:
    # too much to the left
    if xOffset > 0:
        live_spikes_connection2.add_start_callback('input1', send_spike, 2)
    # too much to the right
    else:
        live_spikes_connection2.add_start_callback('input1', send_spike, 3)
else:
    # too much to the left
    if xOffset > 0:
        live_spikes_connection2.add_start_callback('input1',
                                                   send_spike, 0)
    # too much to the right
    else:
        live_spikes_connection2.add_start_callback('input1',
                                                   send_spike, 1)

weights = []
weightPlotRight = [[0 for x in range(numberOfSteps)] for y in range(numberOfSteps)]
weightPlotLeft = [[0 for x in range(numberOfSteps)] for y in range(numberOfSteps)]
weightPlotJumpRight = [[0 for x in range(numberOfSteps)] for y in range(numberOfSteps)]
weightPlotJumpLeft = [[0 for x in range(numberOfSteps)] for y in range(numberOfSteps)]


def restarting_simulation():
    press_key(k.escape_key)
    press_key(k.down_key)
    press_key(k.enter_key)
    sleep(0.2)
    press_key(k.right_key)
    press_key(k.enter_key)
    sleep(0.5)

    press_key(k.escape_key)
    press_key(k.down_key)
    press_key(k.enter_key)
    sleep(0.2)
    press_key(k.left_key)
    press_key(k.enter_key)


for i in range(numberOfSteps):

    restarting_simulation()
    step += 1
    if i > 0:
        for j in range(i+1):
            action = weights[j*4:(j+1)*4-1].argmax()
            print str(weights[j*4:(j+1)*4-1]) + '=============================='
            if action == 0:
                print 'go right'
                live_spikes_connection2.add_start_callback('input1',
                                                           send_spike, j*4)
            if action == 1:
                print 'go left'
                live_spikes_connection2.add_start_callback('input1',
                                                           send_spike, j*4 + 1)
            if action == 2:
                print 'jump right'
                live_spikes_connection2.add_start_callback('input1',
                                                           send_spike, j*4 + 2)
            if action == 3:
                print 'jump left'
                live_spikes_connection2.add_start_callback('input1',
                                                           send_spike, j*4 + 3)

    sim.run(2000 + i*3000)
    sleep(1.5)
    weights = stdp_projection.getWeights()
    print weights
    execute_commands()
    for j in range(numberOfSteps):
        weightPlotRight[j].append(weights[j*4])
        weightPlotLeft[j].append(weights[j*4+1])
        weightPlotJumpRight[j].append(weights[j*4+2])
        weightPlotJumpLeft[j].append(weights[j*4+3])

    live_spikes_connection2.clear_start_resume_callbacks('input1')
    firedIndex = []


neo = post_pop.get_data(variables=["spikes", "v"])
spikes2 = neo.segments[0].spiketrains
v2 = neo.segments[0].filter(name='v')[0]

sim.end()

for j in range(numberOfSteps):
    plt.plot(weightPlotRight[j], label='right weights at step ' + str(j))
    plt.plot(weightPlotLeft[j], label='left weights at step ' + str(j))
    plt.plot(weightPlotJumpRight[j], label='jump right weights at step ' + str(j))
    plt.plot(weightPlotJumpLeft[j], label='jump left weights at step ' + str(j))

plt.legend()
plt.show()

plot.Figure(
    plot.Panel(v2, ylabel="Membrane potential (mV)",
               data_labels=['controls'], yticks=True),
    plot.Panel(spikes2, yticks=True, markersize=5),
    title="Simple Example",
    annotations="Simulated with {}".format(sim.name())
)
plt.show()