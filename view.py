import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.file = None

        # create widgets
        # text Variables
        self.snd_file = tk.StringVar()
        self.button_status = 'disabled'

        # Creating Sub-Frame
        self.choosing_frame = ttk.Frame(self, padding='5 5 5 5')
        self.choosing_frame.grid(row=0, column=0, sticky='NSWE')
        # open button
        self.open_button = ttk.Button(
            self.choosing_frame,
            text='Open Sound File',
            command=lambda: self.snd_file.set(self.select_file()))
        self.open_button.grid(row=0, column=3, padx=10)


        # file label
        self.file_label = ttk.Label(
            self.choosing_frame,
            width=75, textvariable=self.snd_file)
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

        # message
        self.message_label = ttk.Label(
            self.converting_frame,
            width=75, text='')
        self.message_label.grid(row=0, column=1, sticky=tk.W)

        # set the controller
        self.controller = None


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
        self.message_label.after(3000, self.hide_message)

    def is_wav_fileformat(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.message_label.after(3000, self.hide_message)
        # reset the form
        self.snd_file.set('')

    def hide_message(self):
        self.message_label['text'] = ''

    def set_button_state(self, state):
        self.button_status = state
        self.conversion_button.config(state=self.button_status)
