from scipy.io import wavfile as wav
from scipy.fftpack import fft
from scipy.signal import correlate
import numpy as np
import matplotlib.pyplot as plot

correctAnswers = [
    3.6,
    5.0,
    0.5,
    4.2
]

def signalAverage(signal):
    sum = 0
    for i in range(len(signal)):
        sum += np.absolute(signal[i])
    return sum / len(signal)

def sameness(signal1, signal2):
    return np.absolute(signalAverage(signal1) - signalAverage(signal2))

def sameness_new(signal1, signal2):
    mid = int(len(signal1) / 2)
    return np.absolute(
        signalAverage(signal1[0:mid]) - signalAverage(signal2[0:mid]) +
        signalAverage(signal1[mid:]) - signalAverage(signal2[mid:])
    )

def getMinimumIndex(signal):
    minVal = 10000000
    minIndex = 0
    for i in range(len(signal)):
        if signal[i] < minVal:
            minVal = signal[i]
            minIndex = i
    return minIndex

def getMaximumIndex(signal):
    maxVal = 0
    maxIndex = 0
    for i in range(len(signal)):
        if signal[i] > maxVal:
            maxVal = signal[i]
            maxIndex = i
    return maxIndex

results = []
for index in range(1, 5):
    INPUT_SOURCE = "testcases/{}/source.wav".format(index)
    INPUT_TARGET = "testcases/{}/target.wav".format(index)

    print("{} & {}".format(INPUT_SOURCE, INPUT_TARGET))

    input_source_rate, input_source_data = wav.read(INPUT_SOURCE)
    input_target_rate, input_target_data = wav.read(INPUT_TARGET)

    fft_sameness = []
    date_sameness = []
    seconds = []
    SEGMENT_SECOND = 0.1
    for i in range(0, len(input_source_data) - len(input_target_data), int(SEGMENT_SECOND * input_source_rate)):
        segmented_signal = input_source_data[i:i + len(input_target_data)]

        source_fft = np.fft.fft(segmented_signal)
        target_fft = np.fft.fft(input_target_data)

        source_fft = source_fft[1:4000]
        target_fft = target_fft[1:4000]

        fft_sameness.append(sameness(source_fft, target_fft))
        date_sameness.append(sameness(segmented_signal, input_target_data)*100)
        seconds.append((i / input_source_rate))


    # plot.plot(fft_sameness)
    # plot.show()
    foundSecond = seconds[getMinimumIndex(fft_sameness)]
    results.append(foundSecond)
    print("{} -> The target found in source file in time {} seconds...".format(index, foundSecond))

count = 0
for i in range(len(correctAnswers)):
    if (correctAnswers[i] == results[i]):
        count += 1
print("Algorithm accuracy: {}".format(count / len(correctAnswers) * 100))
