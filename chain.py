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

step = 1
firedIndex = []
history = []
nextAction = 0


def execute_commands():
    global step, firedIndex, nextAction
    try:
        print 'Executing commands for step: ' + str(step)
        historyStep = 'step ' + str(step) + ': '
        step += 1
        commands = list(set(firedIndex))
        commands.sort()
        for neuron_id in commands:
            print 'doing ' + str(neuron_id)
            neuron_id %= 4
            if str(neuron_id) is '0':
                sleep(0.1)
                historyStep += ' went right, '
                time = datetime.time(datetime.now())
                print str(time) + ' press right'
                k.press_key(k.right_key)
                sleep(1)
                time = datetime.time(datetime.now())
                print str(time) + ' release right'
                k.release_key(k.right_key)
            if str(neuron_id) is '1':
                sleep(0.1)
                historyStep += ' went left, '
                time = datetime.time(datetime.now())
                print str(time) + ' press left'
                k.press_key(k.left_key)
                sleep(1)
                time = datetime.time(datetime.now())
                print str(time) + ' release left'
                k.release_key(k.left_key)
            if str(neuron_id) is '2':
                sleep(0.1)
                historyStep += ' jumped right, '
                time = datetime.time(datetime.now())
                print str(time) + ' press space + right'
                k.press_key(k.space)
                k.press_key(k.right_key)
                sleep(1)
                time = datetime.time(datetime.now())
                print str(time) + ' release space + right'
                k.release_key(k.space)
                k.release_key(k.right_key)
            if str(neuron_id) is '3':
                sleep(0.1)
                historyStep += ' jumped left, '
                time = datetime.time(datetime.now())
                print str(time) + ' press space + left'
                k.press_key(k.space)
                k.press_key(k.left_key)
                sleep(1)
                time = datetime.time(datetime.now())
                print str(time) + ' release space + left'
                k.release_key(k.space)
                k.release_key(k.left_key)
        history.append(historyStep)
        sleep(0.5)
        print 'For the next action in step ' + str(step)
        image = pyautogui.screenshot(region=(0, 200, 1250, 700))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cv2.imwrite("screenCapture" + str(step) + ".png", image)
        meatboy_image = cv2.imread('meatboy.png')
        meatgirl_image = cv2.imread('meatgirl.png')
        large_image = cv2.imread("screenCapture" + str(step) + ".png")
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
        print '=============================='
        print 'xOffset: ' + str(xOffset)
        print 'yOffset: ' + str(yOffset)

        trows, tcols = meatboy_image.shape[:2]
        trows2, tcols2 = meatgirl_image.shape[:2]

        cv2.rectangle(large_image, (MPx, MPy), (MPx + tcols, MPy + trows),
                      (0, 255, 0), 2)
        cv2.rectangle(large_image, (MPx2, MPy2),
                      (MPx2 + tcols2, MPy2 + trows2), (0, 255, 0), 2)
        cv2.imwrite("screenCapture" + str(step) + ".png", large_image)
        # too low
        if yOffset < 0:
            # too much to the left
            if xOffset > 0:
                print 'jump right'
                nextAction = (step-1) * 4 + 2
            # too much to the right
            else:
                print 'jump left'
                nextAction = (step-1) * 4 + 3
        else:
            # too much to the left
            if xOffset > 0:
                print 'go right'
                nextAction = (step-1) * 4
            # too much to the right
            else:
                print 'go left'
                nextAction = (step-1) * 4 + 1
        print 'Next action: ' + str(nextAction)
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


restarting_simulation()
sleep(2)
image = pyautogui.screenshot(region=(0, 200, 1250, 700))
image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
cv2.imwrite("screenCapture" + str(step) + ".png", image)
meatboy_image = cv2.imread('meatboy.png')
meatgirl_image = cv2.imread('meatgirl.png')
large_image = cv2.imread("screenCapture" + str(step) + ".png")
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
print '=============================='
print 'xOffset: ' + str(xOffset)
print 'yOffset: ' + str(yOffset)

trows, tcols = meatboy_image.shape[:2]
trows2, tcols2 = meatgirl_image.shape[:2]

cv2.rectangle(large_image, (MPx, MPy), (MPx + tcols, MPy + trows),
              (0, 255, 0), 2)
cv2.rectangle(large_image, (MPx2, MPy2),
              (MPx2 + tcols2, MPy2 + trows2), (0, 255, 0), 2)
cv2.imwrite("screenCapture" + str(step) + ".png", large_image)
# too low
if yOffset < 0:
    # too much to the left
    if xOffset > 0:
        print 'jump right'
        nextAction = (step-1) * 4 + 2
    # too much to the right
    else:
        print 'jump left'
        nextAction = (step-1) * 4 + 3
else:
    # too much to the left
    if xOffset > 0:
        print 'go right'
        nextAction = (step-1) * 4
    # too much to the right
    else:
        print 'go left'
        nextAction = (step-1) * 4 + 1
print 'Next action: ' + str(nextAction)


for i in range(numberOfSteps):

    for j in range(i+1):
        if j != i:
            print 'Looking at the history of weights in order to choose actions'
            print 'The weights ' + str(weights)
            print 'For action ' + str(j+1)
            action = weights[j*4:(j+1)*4].argmax()
            print str(weights[j*4:(j+1)*4])
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
        else:
            live_spikes_connection2.add_start_callback('input1',
                                                       send_spike,
                                                       nextAction)

    sim.run(2000 + i*2000)
    sleep(1.5)
    weights = stdp_projection.getWeights()
    print weights
    execute_commands()
    sleep(1)
    for j in range(numberOfSteps):
        weightPlotRight[j].append(weights[j*4])
        weightPlotLeft[j].append(weights[j*4+1])
        weightPlotJumpRight[j].append(weights[j*4+2])
        weightPlotJumpLeft[j].append(weights[j*4+3])

    live_spikes_connection2.clear_start_resume_callbacks('input1')
    firedIndex = []
    restarting_simulation()


neo = post_pop.get_data(variables=["spikes", "v"])
spikes2 = neo.segments[0].spiketrains
v2 = neo.segments[0].filter(name='v')[0]

sim.end()

for historyStep in history:
    print historyStep

# for j in range(numberOfSteps):
#     plt.plot(weightPlotRight[j], label='right weights at step ' + str(j))
#     plt.plot(weightPlotLeft[j], label='left weights at step ' + str(j))
#     plt.plot(weightPlotJumpRight[j], label='jump right weights at step ' + str(j))
#     plt.plot(weightPlotJumpLeft[j], label='jump left weights at step ' + str(j))
#
# plt.legend()
# plt.show()
#
# plot.Figure(
#     plot.Panel(v2, ylabel="Membrane potential (mV)",
#                data_labels=['controls'], yticks=True),
#     plot.Panel(spikes2, yticks=True, markersize=5),
#     title="Simple Example",
#     annotations="Simulated with {}".format(sim.name())
# )
# plt.show()