import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import ImageTk, Image

class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.file = None
        self.file_data = [0, 0]
        self.snd_file = ''
        self.button_status = 'disabled'
        self.graph_window = ''
        self.img = None
        self.label = None
        self.img_frame = None
        self.text_frame = None
        self.text_label = None

        # create widgets
        # Creating Sub-Frame
        self.choosing_frame = ttk.Frame(self, padding='5 5 5 5')
        self.choosing_frame.grid(row=0, column=0, sticky='NSWE')
        # open button
        self.open_button = ttk.Button(
            self.choosing_frame,
            text='Open Sound File',
            command=lambda: self.setting_variable())
        self.open_button.grid(row=0, column=3, padx=10)


        # file label
        self.file_label = ttk.Label(
            self.choosing_frame,
            width=75, text=self.snd_file)
        self.file_label.grid(row=0, column=1, sticky=tk.W)

        # Separator 1
        self.separator_1 = ttk.Separator(self, orient='horizontal')
        self.separator_1.grid(sticky='NEWS', row=1)

        # Creating Sub Frame 2
        self.converting_frame = ttk.Frame(self, padding='5 5 5 5')
        self.converting_frame.grid(row=2, column=0, sticky='NSWE')

        # Converter Button
        self.conversion_button = ttk.Button(
            self.converting_frame,
            text='Convert',
            state=self.button_status,
            command=lambda: self.controller.converter(self.snd_file))
        self.conversion_button.grid(row=0, column=3, padx=10)

        #  success message
        self.message_label = ttk.Label(
            self.converting_frame,
            width=75, text='')
        self.message_label.grid(row=0, column=1, sticky=tk.W)

        # Separator 2
        self.separator_2 = ttk.Separator(self, orient='horizontal')
        self.separator_2.grid(sticky='NEWS', row=3)

        # Creating Sub-Frame 3
        self.graphing_frame = ttk.Frame(self, padding='5 5 5 5')
        self.graphing_frame.grid(row=4, column=0, sticky='NSWE')

        # Time label
        self.minutes = int('0')
        self.seconds = int('0')
        self.file_length = ttk.Label(
            self.graphing_frame,
            width=75,
            text='')
        self.file_length.grid(row=0, column=0, sticky=tk.W)

        # Frequency Label
        self.file_freq = ttk.Label(
            self.graphing_frame,
            width=75,
            text=''
        )
        self.file_freq.grid(row=1, column=0, sticky=tk.W)

        # Graphing button
        self.graph_button = ttk.Button(
            self.graphing_frame,
            text='Plot the graphs',
            command=lambda: self.plotting_graphs()
        )
        self.graph_button.grid(row=0, column=3, sticky=tk.W)

        # set the controller
        self.controller = None

    def setting_variable(self):
        self.snd_file = self.select_file()
        self.file_label.config(text=f'{self.snd_file}')

    def plotting_graphs(self):
        self.file_data = self.controller.graph_data()
        self.minutes = int(self.file_data[1]/60)
        self.seconds = round(self.file_data[1]-(self.minutes*60), 2)
        self.file_length.config(text=f'Length of file is {self.minutes} minute(s) and {self.seconds} seconds')
        self.file_freq.config(text=f'Frequency of {self.file_data[0]} Hz')
        self.graph_window_func()

    def select_file(self):
        filetypes = (
            ('mp3 files', '*.mp3'),
            ('m4a files', '*.m4a'),
            ('wav files', '*.wav'),
            ('All files', '*')
        )
        _filename = fd.askopenfilename(
            title='Choose Sound File',
            initialdir='/',
            filetypes=filetypes)
        self.file = _filename
        self.controller.filetype_checker(self.file)
        return _filename

    def set_controller(self, controller):
        self.controller = controller

    def wrong_audio_format(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'orange'
        self.message_label.after(3000, self.hide_message)

    def not_audio_format(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        self.message_label.after(30000, self.hide_message)

    def is_wav_fileformat(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.message_label.after(30000, self.hide_message)
        # reset the form
        self.snd_file = ''

    def hide_message(self):
        self.message_label['text'] = ''

    def set_button_state(self, state):
        self.button_status = state
        self.conversion_button.config(state=self.button_status)

    def graph_window_func(self):
        self.graph_window = Toplevel(self)
        self.graph_window.title('Graph Window')
        self.graph_window.geometry('750x600')

        #image Frame
        self.img_frame = ttk.Frame(self.graph_window, width=600, height=500)
        self.img_frame.grid(row=0, column=0)

        self.img = ImageTk.PhotoImage(Image.open(f'{self.file_data[2]}'))
        self.label = tk.Label(self.img_frame, image=self.img)
        self.label.image = self.img
        self.label.place(x=0, y=0)

        #text frame
        text_frame = ttk.Frame(self.graph_window, padding='5 5 5 5')
        text_frame.grid(row=1, column=0)

        self.text_label = Label(text_frame, text='')
        self.text_label.grid(row=0, column=0)

        #button frame
        button_frame = ttk.Frame(self.graph_window, padding='5 5 5 5')
        button_frame.grid(row=2, column=0)

        #Button Creation
        #RT60 Graphs
        rt60_low_button = ttk.Button(button_frame, text='RT60 Low', command=lambda: self.rt60_low_graph())
        rt60_low_button.grid(row=1, column=0)
        rt60_med_button = ttk.Button(button_frame, text='RT60 Med', command=lambda: self.rt60_med_graph())
        rt60_med_button.grid(row=1, column=1)
        rt60_high_button = ttk.Button(button_frame, text='RT60 High', command=lambda: self.rt60_high_graph())
        rt60_high_button.grid(row=1, column=2)
        combined_button = ttk.Button(button_frame, text='Combined', command=lambda: self.rt60_combined_graph())
        combined_button.grid(row=1, column=3)

        #Other Graphs
        waveform_button = ttk.Button(button_frame, text='Waveform', command=lambda: self.waveform_graph())
        waveform_button.grid(row=0, column=0)
        histogram_button = ttk.Button(button_frame, text='Histogram', command=lambda:self.histogram_graph())
        histogram_button.grid(row=0, column=1)
        scatter_button = ttk.Button(button_frame, text='Scatter', command=lambda:self.scatter_graph())
        scatter_button.grid(row=0, column=2)



    def histogram_graph(self):
        self.img = ImageTk.PhotoImage(Image.open(f'{self.file_data[2]}'))
        self.label.config(image=self.img)

    def waveform_graph(self):
        self.img = ImageTk.PhotoImage(Image.open(f'{self.file_data[3]}'))
        self.label.config(image=self.img)

    def scatter_graph(self):
        self.img = ImageTk.PhotoImage(Image.open(f'{self.file_data[4]}'))
        self.label.config(image=self.img)

    def rt60_low_graph(self):
        self.img = ImageTk.PhotoImage(Image.open(f'{self.file_data[5]}'))
        self.label.config(image=self.img)
        self.text_label.config(text=f'{self.file_data[6]}')

    def rt60_med_graph(self):
        self.img = ImageTk.PhotoImage(Image.open(f'{self.file_data[7]}'))
        self.label.config(image=self.img)
        self.text_label.config(text=f'{self.file_data[8]}')

    def rt60_high_graph(self):
        self.img = ImageTk.PhotoImage(Image.open(f'{self.file_data[9]}'))
        self.label.config(image=self.img)
        self.text_label.config(text=f'{self.file_data[10]}')

    def rt60_combined_graph(self):
        self.img = ImageTk.PhotoImage(Image.open(f'{self.file_data[11]}'))
        self.label.config(image=self.img)
        self.text_label.config(text='')