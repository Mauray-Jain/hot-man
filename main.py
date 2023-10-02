import tkinter as tk
from tkinter import ttk


class Page(tk.Frame):
    pageId = ''

    def __init__(self, widget, pageId):
        super().__init__(self, widget)
        self.pageId = pageId


class App(tk.Tk):
    height = 720
    width = 1080

    def __init__(self):
        super().__init__()

        self.title('Restaurant management system')
        self.geometry(str(self.width) + 'x' + str(self.height))
        self.resizable(False, False)


if __name__ == '__main__':
    app = App()
    app.mainloop()
