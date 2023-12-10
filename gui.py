import tkinter as tk
from tkinter import *
from tkinter import ttk
import gui_backend

# Creating GUI Window (View)
_root = tk.Tk()
_root.title('Acoustics Program')
_root.resizable(True, True)
_root.geometry('650x350')

# Setting aside space for file choosing frame
_choosing_frame = ttk.Frame(_root, padding='5 5 5 5')
_choosing_frame.grid(row=0, column=0, sticky='NSWE')

# Open File Button
open_button = ttk.Button(
    _choosing_frame,
    text='Open Sound File',
    command=lambda: update_gui())
open_button.grid(row=0, column=1)

# Chosen File Label
_snd_file = ' '
_snd_file_label = Label(_choosing_frame, height=1, width=75, text=_snd_file)
_snd_file_label.grid(row=0, column=0)

def update_gui():
    global _snd_file
    _snd_file = gui_backend.select_file()
    _snd_file_label.config(text=_snd_file)
    _conversion_msg = gui_backend.filetype_checker(_snd_file)
    _conversion_label.config(text=f"{_conversion_msg[0]}")
    _conversion_button.config(state=f'{_conversion_msg[1]}')


# Separator 1 & Adding Converter Frame
separator_1 = ttk.Separator(_root, orient='horizontal')
separator_1.grid(sticky='NEWS', row=1)

_converting_frame = ttk.Frame(_root, padding='5 5 5 5')
_converting_frame.grid(row=2, column=0, sticky='NSWE')


# Converter button
_conversion_button = ttk.Button(
    _converting_frame,
    text='Convert',
    command=lambda: gui_backend.converter(_snd_file)
)
_conversion_button.grid(row=0, column=1)

# Conversion Label
_conversion_msg = ' '
_conversion_label = Label(_converting_frame, height=1, width=75, text=_conversion_msg)
_conversion_label.grid(row=0, column=0)


# Run Application
_root.mainloop()