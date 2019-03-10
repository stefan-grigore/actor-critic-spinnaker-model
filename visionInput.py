import pyNN.spiNNaker as sim
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt
import threading
from random import randint, uniform
from time import sleep
from pykeyboard import PyKeyboard
import keyboard
import cv2
import numpy as np
import pyautogui
from datetime import datetime


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

# 900 ms latency when debugging
def receive_spikes(label, time, neuron_ids):
    try:
        time = datetime.time(datetime.now())
        for neuron_id in neuron_ids:
            if str(neuron_id) is '0':
                print str(time) + ' press right'
                k.press_key(k.right_key)
            # if str(neuron_id) is '1':
                sleep(1)
                print str(time) + ' release right'
                k.release_key(k.right_key)
            if str(neuron_id) is '2':
                print str(time) + ' press left'
                k.press_key(k.left_key)
            # if str(neuron_id) is '3':
                sleep(1)
                print str(time) + ' release left'
                k.release_key(k.left_key)
            if str(neuron_id) is '4':
                print str(time) + ' press space'
                k.press_key(k.space)
            # if str(neuron_id) is '5':
                sleep(1)
                print str(time) + ' release space'
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


# def on_press(key):
#     if key == Key.ctrl_l:
#         # Stop listener
#         return False
#     send_spike('stateSpikeInjector', live_spikes_connection2)
#
#
# def input_thread():
#     print 'Started thread'
#     with Listener(
#             on_press=on_press) as listener:
#         listener.join()
#
#
# thread = threading.Thread(target=input_thread)
# thread.start()

def send_spikes(id):
    live_spikes_connection2.send_spike('stateSpikeInjector', id,
                                       send_full_keys=True)


def send_right_press_spikes_thread():
    sleep(12)
    while True:
        time = datetime.time(datetime.now())
        print time
        image = pyautogui.screenshot(region=(0, 200, 1250, 700))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cv2.imwrite("screenCapture.png", image)
        meatboy_image = cv2.imread('meatboy.png')
        meatgirl_image = cv2.imread('meatgirl.png')
        large_image = cv2.imread("screenCapture.png")
        method = cv2.TM_SQDIFF_NORMED
        result = cv2.matchTemplate(meatboy_image.astype(np.float32), large_image.astype(np.float32), method)
        result2 = cv2.matchTemplate(meatgirl_image.astype(np.float32), large_image.astype(np.float32), method)
        mn, _, mnLoc, _ = cv2.minMaxLoc(result)
        mn2, _, mnLoc2, _ = cv2.minMaxLoc(result2)
        MPx, MPy = mnLoc
        MPx2, MPy2 = mnLoc2
        # MPx = MPx + 200

        # # Step 2: Get the size of the template. This is the same size as the match.
        # trows, tcols = meatboy_image.shape[:2]
        # trows2, tcols2 = meatgirl_image.shape[:2]
        #
        # # Step 3: Draw the rectangle on large_image
        # cv2.rectangle(large_image, (MPx, MPy), (MPx + tcols, MPy + trows), (0, 255, 0), 2)
        # cv2.rectangle(large_image, (MPx2, MPy2), (MPx2 + tcols2, MPy2 + trows2), (0, 255, 0), 2)
        # cv2.imwrite("screenCapture.png", large_image)

        xOffset = MPx2 - MPx
        yOffset = MPy2 - MPy
        print str(time) + ' X offset:' + str(xOffset)
        print str(time) + ' Y offset:' + str(yOffset)
        # too much to the left
        if xOffset > 0:
            # release left
            send_spikes(3)
            print str(time) + ' command release left'
            # press right
            send_spikes(0)
            print str(time) + ' command press right'
        else:
            # too much to the right
            # release right
            send_spikes(1)
            print str(time) + ' command release right'
            # press left
            send_spikes(2)
            print str(time) + ' command press left'
        sleep(1)


def send_left_press_spikes_thread():
    sleep(12)
    while True:
        time = datetime.time(datetime.now())
        print time
        image = pyautogui.screenshot(region=(0, 200, 1250, 700))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cv2.imwrite("screenCapture.png", image)
        meatboy_image = cv2.imread('meatboy.png')
        meatgirl_image = cv2.imread('meatgirl.png')
        large_image = cv2.imread("screenCapture.png")
        method = cv2.TM_SQDIFF_NORMED
        result = cv2.matchTemplate(meatboy_image.astype(np.float32), large_image.astype(np.float32), method)
        result2 = cv2.matchTemplate(meatgirl_image.astype(np.float32), large_image.astype(np.float32), method)
        mn, _, mnLoc, _ = cv2.minMaxLoc(result)
        mn2, _, mnLoc2, _ = cv2.minMaxLoc(result2)
        MPx, MPy = mnLoc
        MPx2, MPy2 = mnLoc2
        # MPx = MPx - 200

        # # Step 2: Get the size of the template. This is the same size as the match.
        # trows, tcols = meatboy_image.shape[:2]
        # trows2, tcols2 = meatgirl_image.shape[:2]
        #
        # # Step 3: Draw the rectangle on large_image
        # cv2.rectangle(large_image, (MPx, MPy), (MPx + tcols, MPy + trows), (0, 255, 0), 2)
        # cv2.rectangle(large_image, (MPx2, MPy2), (MPx2 + tcols2, MPy2 + trows2), (0, 255, 0), 2)
        # cv2.imwrite("screenCapture.png", large_image)

        xOffset = MPx2 - MPx
        yOffset = MPy2 - MPy
        print str(time) + ' X offset:' + str(xOffset)
        print str(time) + ' Y offset:' + str(yOffset)
        # too much to the left
        if xOffset > 0:
            # release left
            send_spikes(3)
            print str(time) + ' command release left'
            # press right
            send_spikes(0)
            print str(time) + ' command press right'
        else:
            # too much to the right
            # release right
            send_spikes(1)
            print str(time) + ' command release right'
            # press left
            send_spikes(2)
            print str(time) + ' command press left'
        sleep(1)


def send_jump_press_spikes_thread():
    sleep(12)
    while True:
        try:
            time = datetime.time(datetime.now())
            print time
            image = pyautogui.screenshot(region=(0, 200, 1250, 700))
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv2.imwrite("screenCapture.png", image)
            meatboy_image = cv2.imread('meatboy.png')
            meatgirl_image = cv2.imread('meatgirl.png')
            large_image = cv2.imread("screenCapture.png")
            method = cv2.TM_SQDIFF_NORMED
            result = cv2.matchTemplate(meatboy_image.astype(np.float32), large_image.astype(np.float32), method)
            result2 = cv2.matchTemplate(meatgirl_image.astype(np.float32), large_image.astype(np.float32), method)
            mn, _, mnLoc, _ = cv2.minMaxLoc(result)
            mn2, _, mnLoc2, _ = cv2.minMaxLoc(result2)
            MPx, MPy = mnLoc
            MPx2, MPy2 = mnLoc2

            # # Step 2: Get the size of the template. This is the same size as the match.
            # trows, tcols = meatboy_image.shape[:2]
            # trows2, tcols2 = meatgirl_image.shape[:2]
            #
            # # Step 3: Draw the rectangle on large_image
            # cv2.rectangle(large_image, (MPx, MPy), (MPx + tcols, MPy + trows), (0, 255, 0), 2)
            # cv2.rectangle(large_image, (MPx2, MPy2), (MPx2 + tcols2, MPy2 + trows2), (0, 255, 0), 2)
            # cv2.imwrite("screenCapture.png", large_image)

            xOffset = MPx2 - MPx
            yOffset = MPy2 - MPy
            print str(time) + ' X offset:' + str(xOffset)
            print str(time) + ' Y offset:' + str(yOffset)
            # too much to the left
            if yOffset < 0:
                # too much to the left
                if xOffset > 0:
                    # release left
                    send_spikes(3)
                    print str(time) + ' command release left'
                    # press right
                    send_spikes(0)
                    print str(time) + ' command press right'
                else:
                    # too much to the right
                    # release right
                    send_spikes(1)
                    print str(time) + ' command release right'
                    # press left
                    send_spikes(2)
                    print str(time) + ' command press left'
                # press space
                send_spikes(4)
                print str(time) + ' command press space'
            sleep(2)
            # release space
            send_spikes(5)
            print str(time) + ' command release space'
        except AttributeError:
            pass


thread0 = threading.Thread(target=send_right_press_spikes_thread)
thread2 = threading.Thread(target=send_left_press_spikes_thread)
thread4 = threading.Thread(target=send_jump_press_spikes_thread)

thread0.start()
thread2.start()
thread4.start()

sim.run(13000)

# neo = actorPopulation.get_data(variables=["spikes", "v"])
# spikes = neo.segments[0].spiketrains
# v = neo.segments[0].filter(name='v')[0]
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