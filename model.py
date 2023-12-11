import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.io.wavfile as wav
from scipy.fft import fft, fftfreq
import os
from scipy.signal import freqs


class Model:
    def __init__(self):
        self.file_path = None
        self.file_name = None
        self.data = None
        self.samplerate = None
        self.channels = None
        self.length = None
        self.histogram = None
        self.scatter = None
        self.graph_folder = f'{os.getcwd()}\\graph_folder'
        self.rt60_freq_min = None
        self.rt60_freq_max = None
        self.data_low = None
        self.data_med = None
        self.data_high = None
        self.t = None

        self.return_data = []
        # 0[samplerate], 1[length], 2[histogram_dir], 3[scatter_directory]


    def main_functionality(self, filepath, filename):
        self.data_setting(filepath, filename)
        self.graphing_func()
        return self.return_data

    def data_setting(self, filepath, filename):
        self.file_name = filename
        self.file_path = filepath
        self.samplerate, self.data = wav.read(self.file_path)
        self.length = len(self.data) / self.samplerate

        self.return_data.append(self.samplerate)
        self.return_data.append(self.length)

    def graphing_func(self):
        self.return_data.append(f'{self.graph_folder}\\{self.graph_histogram()}')
        self.return_data.append(f'{self.graph_folder}\\{self.graph_waveform()}')
        self.return_data.append(f'{self.graph_folder}\\{self.graph_scatter()}')
        self.rt60_graph(60, 250, "low")
        self.rt60_graph(900, 1000, "med")
        self.rt60_graph(6000, 7000, "high")
        self.combined_graph()

    def graph_histogram(self):
        plt.hist(self.file_path)
        plt.title('Histogram of Wav File')
        plt.xlabel('x')
        plt.ylabel('y')
        os.chdir(self.graph_folder)
        graph_filename = f'{self.file_name}_histogram.png'
        plt.savefig(graph_filename)
        return graph_filename

    def graph_waveform(self):
        if len(self.data.shape) > 1:
            self.data = np.mean(self.data, axis=1)

        plt.plot(self.data[:int(self.samplerate)])
        plt.title("Scatter Plot of Data")
        plt.xlabel("Sample")
        plt.ylabel("Amplitude")
        #plt.show()
        os.chdir(self.graph_folder)
        graph_filename = f'{self.file_name}_waveform.png'
        plt.savefig(graph_filename)
        return graph_filename

    def graph_scatter(self):
        fft_data = fft(self.data)
        freqs = fftfreq(len(fft_data), 1 / self.samplerate)
        spectrum = np.abs(fft_data)

        freq_df = pd.DataFrame(data={'frequency': freqs, 'amplitude': spectrum})
        plt.scatter(freq_df['frequency'], freq_df['amplitude'], s=2)
        plt.title("Scatter Plot (Frequency Spectrum)")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")
        os.chdir(self.graph_folder)
        graph_filename = f'{self.file_name}_scatter.png'
        plt.savefig(graph_filename)
        return graph_filename

    def find_target_frequency(self, freqs):
        for x in freqs:
            if self.rt60_freq_min < x < self.rt60_freq_max:
                return x

    def rt60_graph(self, freq_min, freq_max, title):
        self.rt60_freq_min = freq_min
        self.rt60_freq_max = freq_max
        self.calculate_rt60(title)

    def frequency_check(self, freqs, spectrum, title):
        target_frequency = self.find_target_frequency(freqs)
        index_of_frequency = np.where(freqs == target_frequency)[0][0]

        data_for_frequency = spectrum[index_of_frequency]
        data_in_db_fun = 10 * np.log10(data_for_frequency)
        if title == "low":
            self.data_low = data_in_db_fun
        if title == "med":
            self.data_med = data_in_db_fun
        if title == "high":
            self.data_high = data_in_db_fun
        return data_in_db_fun

    def find_nearest_value(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array-value)).argmin()
        return array[idx]

    def calculate_rt60(self, title):
        spectrum, freqs, self.t, im = plt.specgram(self.data, Fs=self.samplerate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        data_in_db = self.frequency_check(freqs, spectrum, title)
        plt.figure()
        # plot reverb time on grid
        plt.plot(self.t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (dB)')
        # find a index of a max value
        index_of_max = np.argmax(data_in_db)
        value_of_max = data_in_db[index_of_max]
        plt.plot(self.t[index_of_max], data_in_db[index_of_max], 'go')
        # slice array from a max value
        sliced_array = data_in_db[index_of_max:]
        value_of_max_less_5 = value_of_max - 5
        value_of_max_less_5 = self.find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
        plt.plot(self.t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')
        # slice array from a max -5dB
        value_of_max_less_25 = value_of_max - 25
        value_of_max_less_25 = self.find_nearest_value(sliced_array, value_of_max_less_25)
        index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
        plt.plot(self.t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')
        rt20 = (self.t[index_of_max_less_5] - self.t[index_of_max_less_25])[0]
        # extrapolate rt20 to rt60
        rt60 = 3 * rt20
        # optional set limits on plot
        # plt.xlim(0, ((round(abs(rt60), 2)) * 1.5))
        plt.grid()  # show grid
        os.chdir(self.graph_folder)
        graph_name = f'{self.file_name}_rt60_{title}.png'
        plt.savefig(graph_name)
        self.return_data.append(f'{self.graph_folder}\\{graph_name}')
        self.return_data.append(f'The RT60 reverb time at freq between {self.rt60_freq_min}Hz and {self.rt60_freq_max}Hz is {round(abs(int(rt60)), 2)} seconds')

    def combined_graph(self):
        plt.plot(self.t, self.data_low, color='r', label='low')
        plt.plot(self.t, self.data_med, color='g', label='med')
        plt.plot(self.t, self.data_high, color='b', label='high')
        graph_name = f'{self.file_name}_rt60_combined.png'
        plt.savefig(graph_name)
        self.return_data.append(f'{self.graph_folder}\\{graph_name}')