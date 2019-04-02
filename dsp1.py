from __future__ import print_function, division
%matplotlib inline
import thinkdsp1
import thinkplot
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft, fftshift
from ipywidgets import interact, interactive, fixed
import ipywidgets as widgets


wave = thinkdsp.read_wave('72475__rockwehrmann__glissup02.wav')
wave.plot()

wave.make_audio()

wave.make_spectrogram(512).plot(high=5000)