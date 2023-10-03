import tkinter as tk
from tkinter import ttk


class Page(ttk.Frame):
    pageId = ''

    def __init__(self, widget, pageId):
        super().__init__(master=widget)
        self.pageId = pageId
