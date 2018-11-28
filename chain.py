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
from random import randint


sim.setup(timestep=1.0)
sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 100)

numberOfSteps = 11

input1 = sim.Population(numberOfSteps*4, sim.external_devices.SpikeInjector(), label="input1")

input2 = sim.Population(numberOfSteps*4, sim.external_devices.SpikeInjector(), label="input2")

pre_pop = sim.Population(numberOfSteps*4, sim.IF_curr_exp(tau_syn_E=100, tau_refrac=50), label="pre_pop")
post_pop = sim.Population(numberOfSteps*4, sim.IF_curr_exp(tau_syn_E=25, tau_refrac=100), label="post_pop")

sim.external_devices.activate_live_output_for(pre_pop, database_notify_host="localhost", database_notify_port_num=19996)
sim.external_devices.activate_live_output_for(input1, database_notify_host="localhost", database_notify_port_num=19998)
sim.external_devices.activate_live_output_for(post_pop, database_notify_host="localhost", database_notify_port_num=20000)
sim.external_devices.activate_live_output_for(input2, database_notify_host="localhost", database_notify_port_num=20002)

timing_rule = sim.SpikePairRule(tau_plus=50.0, tau_minus=50.0,
                                A_plus=0.001, A_minus=0.001)
weight_rule = sim.AdditiveWeightDependence(w_max=5.0, w_min=-5.0)
stdp_model = sim.STDPMechanism(timing_dependence=timing_rule,
                               weight_dependence=weight_rule,
                               weight=2, delay=1)

stdp_projection = sim.Projection(pre_pop, post_pop, sim.OneToOneConnector(),
                                 synapse_type=stdp_model)

input_projection1 = sim.Projection(input1, pre_pop, sim.OneToOneConnector(),
                            synapse_type=sim.StaticSynapse(weight=5, delay=2))

input_projection2 = sim.Projection(input2, post_pop, sim.OneToOneConnector(),
                            synapse_type=sim.StaticSynapse(weight=5, delay=0))

pre_pop.record(["spikes", "v"])
post_pop.record(["spikes", "v"])

k = PyKeyboard()

step = 1
firedIndex = []
history = []
nextAction = 0

# these are absolutes
prevXOffset = 0
prevYOffset = 0

didExplore = False
exploring = False


def execute_commands():
    global step, firedIndex, nextAction, prevXOffset, prevYOffset, exploring, didExplore
    try:
        print 'Executing commands for step: ' + str(step)
        historyStep = 'step ' + str(step) + ': '
        commands = list(set(firedIndex))
        commands.sort()
        for neuron_id in commands:
            print 'doing ' + str(neuron_id)
            neuron_id %= 4
            if str(neuron_id) is '0':
                sleep(0.15)
                historyStep += ' went right, '
                time = datetime.time(datetime.now())
                print str(time) + ' press right'
                k.press_key(k.right_key)
                sleep(0.5)
                time = datetime.time(datetime.now())
                print str(time) + ' release right'
                k.release_key(k.right_key)
            if str(neuron_id) is '1':
                sleep(0.15)
                historyStep += ' went left, '
                time = datetime.time(datetime.now())
                print str(time) + ' press left'
                k.press_key(k.left_key)
                sleep(0.5)
                time = datetime.time(datetime.now())
                print str(time) + ' release left'
                k.release_key(k.left_key)
            if str(neuron_id) is '2':
                sleep(0.15)
                historyStep += ' jumped right, '
                time = datetime.time(datetime.now())
                print str(time) + ' press space + right'
                k.press_key(k.space)
                k.press_key(k.right_key)
                sleep(0.5)
                time = datetime.time(datetime.now())
                print str(time) + ' release space + right'
                k.release_key(k.space)
                k.release_key(k.right_key)
            if str(neuron_id) is '3':
                sleep(0.15)
                historyStep += ' jumped left, '
                time = datetime.time(datetime.now())
                print str(time) + ' press space + left'
                k.press_key(k.space)
                k.press_key(k.left_key)
                sleep(0.5)
                time = datetime.time(datetime.now())
                print str(time) + ' release space + left'
                k.release_key(k.space)
                k.release_key(k.left_key)
        sleep(0.5)
        print 'For the next action in step ' + str(step + 1)
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
        mn1, _, mnLoc, _ = cv2.minMaxLoc(result)
        mn21, _, mnLoc2, _ = cv2.minMaxLoc(result2)
        MPx, MPy = mnLoc
        MPx2, MPy2 = mnLoc2

        xOffset1 = MPx2 - MPx
        yOffset1 = MPy2 - MPy

        while abs(xOffset - xOffset1) > 5 and abs(yOffset - yOffset1) > 5:
            xOffset = xOffset1
            yOffset = yOffset1
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
            mn1, _, mnLoc, _ = cv2.minMaxLoc(result)
            mn21, _, mnLoc2, _ = cv2.minMaxLoc(result2)
            MPx, MPy = mnLoc
            MPx2, MPy2 = mnLoc2
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
                nextAction = 2
            # too much to the right
            else:
                print 'jump left'
                nextAction = 3
        else:
            # too much to the left
            if xOffset > 0:
                print 'go right'
                nextAction = 0
            # too much to the right
            else:
                print 'go left'
                nextAction = 1
        if not exploring:
            nextAction = step * 4 + nextAction
        else:
            print 'Exploring'
            print 'Action suggested by environment ' + str(nextAction)
            chosenAction = randint(0, 3)
            # while the explored action belongs to the same class as the action suggested by the environment
            # try to pick another action to explore
            while chosenAction%2 is nextAction%2:
                chosenAction = randint(0, 3)
            nextAction = chosenAction
            nextAction = step * 4 + nextAction
        print 'Next action: ' + str(nextAction%4)
        print 'Checking progress'
        if step is 1:
            prevXOffset = abs(xOffset)
            prevYOffset = abs(yOffset)
        # if progress has been made in any direction
        # TODO: also check if progress has been made globally
        elif abs(xOffset) + 5 < prevXOffset or abs(yOffset) + 5 < prevYOffset:
            exploring = False
            historyStep += ' better than previous step'
            # reward
            for index in range(0, len(commands)):
                reward = numberOfSteps - step + index + 1
                print 'Rewarding command ' + str(index) + ' which is ' + str(commands[index]) + ' with ' + str(reward) + ' spikes'
                for i in range(0, reward):
                    live_spikes_connection2.add_start_callback('input1', send_spike, commands[index])
                reward -= 1
                print 'Previous xOffset ' + str(prevXOffset)
                print 'Previous yOffset ' + str(prevYOffset)
                prevXOffset = abs(xOffset)
                prevYOffset = abs(yOffset)
        else:
            if not didExplore:
                exploring = True
            historyStep += ' worse than previous step'
            # punishment
            for index in range(0, len(commands)):
                punishment = numberOfSteps - step + index + 1
                print 'Punishing command ' + str(index) + ' which is ' + str(commands[index]) + ' with ' + str(punishment) + ' spikes'
                for i in range(0, punishment):
                    live_spikes_connection3.add_start_callback('input2', send_spike, commands[index])
                    live_spikes_connection2.add_start_callback('input1',
                                                               send_spike,
                                                               commands[index])
                punishment -= 1
            print 'Previous xOffset ' + str(prevXOffset)
            print 'Previous yOffset ' + str(prevYOffset)
            prevXOffset = abs(xOffset)
            prevYOffset = abs(yOffset)
        didExplore = exploring
        step += 1
        history.append(historyStep)
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

live_spikes_connection3 = sim.external_devices.SpynnakerLiveSpikesConnection(
    receive_labels=None, local_port=20002, send_labels=['input2'])

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


class Step:
    weightPlotRight = []
    weightPlotLeft = []
    weightPlotJumpRight = []
    weightPlotJumpLeft = []


listOfStepObjects = [Step() for i in range(numberOfSteps)]


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
mn1, _, mnLoc, _ = cv2.minMaxLoc(result)
mn21, _, mnLoc2, _ = cv2.minMaxLoc(result2)
MPx, MPy = mnLoc
MPx2, MPy2 = mnLoc2

xOffset1 = MPx2 - MPx
yOffset1 = MPy2 - MPy

while abs(xOffset-xOffset1) > 5 and abs(yOffset-yOffset1) > 5:
    xOffset = xOffset1
    yOffset = yOffset1
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
    mn1, _, mnLoc, _ = cv2.minMaxLoc(result)
    mn21, _, mnLoc2, _ = cv2.minMaxLoc(result2)
    MPx, MPy = mnLoc
    MPx2, MPy2 = mnLoc2

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
            action = weights[j*4:(j+1)*4].argmax()
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
    live_spikes_connection2.clear_start_resume_callbacks('input1')
    sleep(1.5)
    weights = stdp_projection.getWeights()
    print weights
    execute_commands()
    print 'Executing rewards / punishments'
    sim.run(2000 + i*2000)
    live_spikes_connection2.clear_start_resume_callbacks('input1')
    weights = stdp_projection.getWeights()
    print weights
    sleep(1)
    for j in range(numberOfSteps):
        listOfStepObjects[j].weightPlotRight.append(weights[j*4])
        listOfStepObjects[j].weightPlotLeft.append(weights[j*4+1])
        listOfStepObjects[j].weightPlotJumpRight.append(weights[j*4+2])
        listOfStepObjects[j].weightPlotJumpLeft.append(weights[j*4+3])

    firedIndex = []
    restarting_simulation()


neo = post_pop.get_data(variables=["spikes", "v"])
spikes2 = neo.segments[0].spiketrains
v2 = neo.segments[0].filter(name='v')[0]

sim.end()

for historyStep in history:
    print historyStep

# for j in range(numberOfSteps):
#     if (listOfStepObjects[j].weightPlotRight.count(listOfStepObjects[j].weightPlotRight[0]) != len(listOfStepObjects[j].weightPlotRight)):
#         plt.plot(listOfStepObjects[j].weightPlotRight, label='right weights at step ' + str(j))
#         print 'right weights at step ' + str(j) + ' ' + str(listOfStepObjects[j].weightPlotRight)
#     if (listOfStepObjects[j].weightPlotLeft.count(listOfStepObjects[j].weightPlotLeft[0]) != len(listOfStepObjects[j].weightPlotLeft)):
#         plt.plot(listOfStepObjects[j].weightPlotLeft, label='left weights at step ' + str(j))
#         print 'left weights at step ' + str(j) + ' ' + str(listOfStepObjects[j].weightPlotLeft)
#     if (listOfStepObjects[j].weightPlotJumpRight.count(listOfStepObjects[j].weightPlotJumpRight[0]) != len(listOfStepObjects[j].weightPlotJumpRight)):
#         plt.plot(listOfStepObjects[j].weightPlotJumpRight, label='jump right weights at step ' + str(j))
#         print 'jump right weights at step ' + str(j) + ' ' + str(listOfStepObjects[j].weightPlotJumpRight)
#     if (listOfStepObjects[j].weightPlotJumpLeft.count(listOfStepObjects[j].weightPlotJumpLeft[0]) != len(listOfStepObjects[j].weightPlotJumpLeft)):
#         plt.plot(listOfStepObjects[j].weightPlotJumpLeft, label='jump left weights at step ' + str(j))
#         print 'jump left weights at step ' + str(j) + ' ' + str(listOfStepObjects[j].weightPlotJumpLeft)
#
#
# plt.legend()
# plt.show()

# plot.Figure(
#     plot.Panel(v2, ylabel="Membrane potential (mV)",
#                data_labels=['controls'], yticks=True),
#     plot.Panel(spikes2, yticks=True, markersize=5),
#     title="Simple Example",
#     annotations="Simulated with {}".format(sim.name())
# )
# plt.show()