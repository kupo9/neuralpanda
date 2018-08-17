## -*- coding: utf-8 -*-
#"""
#Created on Tue Nov 24 19:45:06 2015
#
#@author: Pomesh
#"""
#import os
#import numpy as np
#import h5py 
#import Utils.nlxio as nl
#
#os.chdir("D:/CSCStim3")
#
#f = h5py.File("nld4.hdf5", 'w')
#
#numfiles = 10
#
#samples=len(nl.loadNcs('CSC1.ncs')[0])
#        
#_nldtype = np.dtype([('ts', np.uint64), 
#                          ('csc', np.int16, (numfiles, ))])
#                          
#timestamps =f.create_dataset("ts", shape=(samples,), dtype=np.uint64)
#csc = f.create_dataset("csc", shape=(numfiles+1, samples), dtype=np.int16,chunks=True)
#
#timestamps[:] = nl.loadNcs('CSC1.ncs')[1]
#        
#for i in range(1, numfiles + 1):
#    try:
#        print("Extracting CSC" + str(i))
#        #self._data.append(nl.loadNcs('CSC' + str(i) + '.ncs')[0])
#        csc[i] = nl.loadNcs('CSC' + str(i) + '.ncs')[0] #add blank check
#        #self.mmapFile.flush()                
#        print("Done/Flush: CSC" + str(i)) 
#    except IOError as e:
#        print "File not found: CSC" + str(i)
#        print(os.strerror(e.errno))       
#print "\nAll files extracted..."
#
#f.close()
#

from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandstop')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def run():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.signal import freqz

    # Sample rate and desired cutoff frequencies (in Hz).
    fs = 5000.0
    lowcut = 1250.0
    highcut = 500.0

    # Plot the frequency response for a few different orders.
    plt.figure(1)
    plt.clf()
    for order in [3, 6, 9]:
        b, a = butter_bandpass(lowcut, highcut, fs, order=order)
        w, h = freqz(b, a, worN=2000)
        plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)

    plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)],
             '--', label='sqrt(0.5)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.grid(True)
    plt.legend(loc='best')

    # Filter a noisy signal.
    T = 0.05
    nsamples = T * fs
    t = np.linspace(0, T, nsamples, endpoint=False)
    a = 0.02
    f0 = 600.0
    x = 0.1 * np.sin(2 * np.pi * 1.2 * np.sqrt(t))
    x += 0.01 * np.cos(2 * np.pi * 312 * t + 0.1)
    x += a * np.cos(2 * np.pi * f0 * t + .11)
    x += 0.03 * np.cos(2 * np.pi * 2000 * t)
    plt.figure(2)
    plt.clf()
    plt.plot(t, x, label='Noisy signal')

    y = butter_bandpass_filter(x, lowcut, highcut, fs, order=6)
    plt.plot(t, y, label='Filtered signal (%g Hz)' % f0)
    plt.xlabel('time (seconds)')
    plt.hlines([-a, a], 0, T, linestyles='--')
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc='upper left')

    plt.show()


run()