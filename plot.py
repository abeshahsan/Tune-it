import scipy.fft
def plot_graph(self):
    global sampling_rate
    global samples
    sampling_rate, samples = scipy.io.wavfile.read(data)
    self.InputAudioAmplitude.clear()
    peak_value = np.amax(samples)
    normalized_data = samples / peak_value
    length = samples.shape[0] / sampling_rate
    time = list(np.linspace(0, length, samples.shape[0]))
    drawing_pen = pg.mkPen(color=(255, 0, 0), width=0.5)
    self.InputAudioAmplitude.plotItem.setLabel(axis='left', text='Amplitude')
    self.InputAudioAmplitude.plotItem.setLabel(axis='bottom', text='time [s]')
    # self.InputAudioAmplitude.plotItem.getViewBox().setLimits(xMin=0, xMax=np.max(time), yMin=-1.1, yMax=1.1)
    self.InputAudioAmplitude.setXRange(0, 0.1)
    self.InputAudioAmplitude.plot(time, normalized_data, pen=drawing_pen)
    logging.info('User is ploting the original signal')

def plot_graph2(self):
    global sampling_rate2
    global samples2
    sampling_rate2, samples2 = scipy.io.wavfile.read(f'{self.now}Output.wav')
    self.graph_after_2.clear()
    peak_value = np.amax(samples2)
    normalized_data2 = samples2 / peak_value
    length = samples2.shape[0] / sampling_rate2
    time2 = list(np.linspace(0, length, samples2.shape[0]))
    drawing_pen = pg.mkPen(color=(0, 0, 255), width=0.5)
    self.graph_after_2.plotItem.setLabel(axis='left', text='Amplitude')
    self.graph_after_2.plotItem.setLabel(axis='bottom', text='time [s]')
    self.graph_after_2.plotItem.getViewBox().setLimits(xMin=0, xMax=np.max(time2), yMin=-1.1, yMax=1.1)
    self.graph_after_2.plot(time2, normalized_data2, pen=drawing_pen)
    logging.info('User is ploting the equilized signal')


        