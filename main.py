from model import Model
from view import View
from controller import Controller
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Acoustics Program')
        self.resizable(True, True)
        self.geometry('650x350')

        # create a model
        model = Model()

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()
