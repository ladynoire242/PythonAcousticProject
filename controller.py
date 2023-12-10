from tkinter import filedialog as fd
from pydub import AudioSegment
import os
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

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
        return _filename

    def filetype_checker(self, filepath):
        ext = os.path.splitext(filepath)[-1].lower()
        if ext == ".wav":
            self.view.is_wav_fileformat("Selected file is already in .wav format")
            self.view.set_button_state('disabled')
        elif ext == ".mp3" or ext == '.m4a':
            self.view.wrong_audio_format("Selected audio file is not in .wav format")
            self.view.set_button_state('enabled')
        else:
            self.view.not_audio_format("Selected file is not an audio file")
            self.view.set_button_state('disabled')

    def converter(self, filepath):
        # List of everything in file separated with /'s
        var1 = filepath.split(sep='/')

        # Returns just the file name and type as 1 string
        file = var1[len(var1) - 1]

        # Gets extension
        ext = os.path.splitext(filepath)[-1].lower()

        # Gives Directory of where original sound file is by removing file name and type from 'file'
        dir = filepath.replace(file, "")

        # only gives file type without the '.'
        filetype = ext.replace(".", "")

        # Creates variable of same file name but with wav file type and removes all spaces
        spacehold = file.replace(" ", "_")
        new_file_dir = spacehold.replace(ext, ".wav")

        # Changes current directory to dir
        os.chdir(dir)

        # Exports selected audio to wav
        new_file = AudioSegment.from_file(filepath, format=f'{filetype}')
        new_file.export(new_file_dir, format='wav')