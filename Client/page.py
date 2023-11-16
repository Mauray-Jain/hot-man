import tkinter as tk
from tkinter import ttk

class FrameWithScrollBar(tk.Canvas):

    def __init__(self, master, rtwin4bind):
        super().__init__(master)
        self.scroll_y = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        # self.scroll_x = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        self.fr = tk.Frame(self)
        self.fr.bind(
            "<Configure>",
            lambda e: self.configure(
                scrollregion=self.bbox('all')
            )
        )
        self.create_window(0, 0, window=self.fr, anchor='nw')
        self.configure(yscrollcommand=self.scroll_y.set)
        rtwin4bind.bind("<MouseWheel>", self._on_mousewheel, add='+')
        # self.configure(xscrollcommand=self.scroll_x.set)
        self.scroll_y.pack(fill='y', side='right')
        # self.scroll_x.pack(fill='x', side='bottom')

    def _on_mousewheel(self, event):
        self.yview_scroll(int(-1 * (event.delta / 120)), "units")


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class Page(ttk.Frame):
    pageId = ''

    def __init__(self, widget, pageId):
        super().__init__(master=widget)
        self.pageId = pageId
