from tkinter import filedialog as fd
from pydub import AudioSegment
import os
import mutagen


shell = True
def select_file():
    filetypes = (
        ('mp3 files', '*.mp3'),
        ('m4a files', '*.m4a'),
        ('wav files', '*.wav')
    )
    _filename = fd.askopenfilename(
        title='Choose Sound File',
        initialdir='/',
        filetypes=filetypes)
    return _filename


def converter(filepath):
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

    # Takes exported file to metadata editing function to remove possible metadata
    metadata_editing(new_file_dir)

    print(mutagen.File(filepath))

def filetype_checker(filepath):
    ext = os.path.splitext(filepath)[-1].lower()
    if ext != ".wav":
        return "File type is not a wav, please convert", "enabled"
    else:
        # Is a wav file
        return "File type is a wav, no need to convert", "disabled"

def metadata_editing(filepath):
    print(filepath)
    file = mutagen.File(filepath)
    print(file)