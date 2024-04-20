import scipy.fft
    def plot_graph(self):
        global sampling_rate
        global samples
        sampling_rate, samples = scipy.io.wavfile.read(data)
        self.graph_before_2.clear()
        peak_value = np.amax(samples)
        normalized_data = samples / peak_value
        length = samples.shape[0] / sampling_rate
        time = list(np.linspace(0, length, samples.shape[0]))
        drawing_pen = pg.mkPen(color=(255, 0, 0), width=0.5)
        self.graph_before_2.plotItem.setLabel(axis='left', text='Amplitude')
        self.graph_before_2.plotItem.setLabel(axis='bottom', text='time [s]')
        # self.graph_before_2.plotItem.getViewBox().setLimits(xMin=0, xMax=np.max(time), yMin=-1.1, yMax=1.1)
        self.graph_before_2.setXRange(0, 0.1)
        self.graph_before_2.plot(time, normalized_data, pen=drawing_pen)
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

    def plot_spectogram(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.tick_params(axis="x", colors="red")
        self.MplWidget.canvas.axes.tick_params(axis="y", colors="red")
        self.MplWidget.canvas.axes.specgram(samples, Fs=sampling_rate)
        self.MplWidget.canvas.draw()
        logging.info('User is ploting the original specgram')

    def plot_spectogram2(self):
        self.MplWidget2.canvas.axes.clear()
        self.MplWidget2.canvas.axes.tick_params(axis="x", colors="blue")
        self.MplWidget2.canvas.axes.tick_params(axis="y", colors="blue")
        self.MplWidget2.canvas.axes.specgram(samples2, Fs=sampling_rate2)
        self.MplWidget2.canvas.draw()
        logging.info('User is ploting the equilized specgram')

        