def read_wave(filename='sound.wav'):
    """Reads a wave file.

    filename: string

    returns: Wave
    """
    fp = open_wave(filename, 'r')   #To Read the Audio File

    nchannels = fp.getnchannels()   #Returns number of audio channels

    nframes = fp.getnframes()       #Returns number of audio frames

    sampwidth = fp.getsampwidth()   #Returns sample width in byte

    framerate = fp.getframerate()   #Returns sampling frequency


    z_str = fp.readframes(nframes)   #Reads and returns at most n frames of audio

    fp.close()

    dtype_map = {1: np.int8, 2: np.int16, 3: 'special', 4: np.int32}        #subtract the average value from the signal to remove the offset.
    if sampwidth not in dtype_map:
        raise ValueError('sampwidth %d unknown' % sampwidth)

    if sampwidth == 3:
        xs = np.fromstring(z_str, dtype=np.int8).astype(np.int32)           #A new 1-D array initialized from text data in a string Copy of the array, cast to a specified type.
                                                                            #srt:A string containing the data.
                                                                            #dtype:The data type of the array; default: float. For binary input data, the data must be in exactly this format.
        ys = (xs[2::3] * 256 + xs[1::3]) * 256 + xs[0::3]
    else:
        ys = np.fromstring(z_str, dtype=dtype_map[sampwidth])

    # if it's in stereo, just pull out the first channel
    if nchannels == 2:
        ys = ys[::2]
     # ts = np.arange(len(ys)) / framerate
    wave = Wave(ys, framerate=framerate)
    wave.normalize()
    return wave
 def make_spectrogram(self, seg_length, win_flag=True):                     #Computes the spectrogram of the wave.
                                                                            #seg_length: number of samples in each segment
                                                                            #win_flag: boolean, whether to apply hamming window to each segment
                                                                            #returns: Spectrogram

        if win_flag:
            window = np.hamming(seg_length)                                 #Return the Hamming window
        i, j = 0, seg_length
        step = seg_length // 2


        spec_map = {}                                                       # map from time to Spectrum

        while j < len(self.ys):
            segment = self.slice(i, j)
            if win_flag:
                segment.window(window)

            # the nominal time for this segment is the midpoint
            t = (segment.start + segment.end) // 2
            spec_map[t] = segment.make_spectrum()

            i += step
            j += step

        return Spectrogram(spec_map, seg_length)
