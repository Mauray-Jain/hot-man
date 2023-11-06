import tkinter as tk
from tkinter import ttk


# class UiBlock(ttk.Frame):
#     def __init__(self, master):
#         super().__init__(master=master)
#         self.childs = []
#
#     def addChild(self, obj) -> None:
#         self.childs.append(obj)
#
#     def pack(self) -> None:
#         super().pack()
#         for i in self.childs:
#             i.add()
#         self.onEntry()
#
#
#     def pack_forget(self) -> None:
#         # for i in self.childs:
#         #     i.pack_forget()
#         super().pack_forget()
#
#     def add(self) -> None:
#         raise 'Add(Pack) not overwritten error'
#
#     def onEntry(self) -> None:
#         # for those widgets which need to call some function when done setting up
#         pass

class FrameWithScrollBar(tk.Canvas):

    #ways to make this work
    #https://blog.teclado.com/tkinter-scrollable-frames/
    #https://stackoverflow.com/questions/40526496/vertical-scrollbar-for-frame-in-tkinter-python
    # if they dont work - https://pypi.org/project/tkScrolledFrame/
    def __init__(self, master):
        super().__init__(master)
        self.scroll_y = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        # self.scroll_x = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        self.fr = tk.Frame(self)
        self.fr.bind(
            "<Configure>",
            lambda e:self.configure(
                scrollregion=self.bbox('all')
            )
        )
        self.create_window(0, 0, window=self.fr, anchor='nw')
        self.configure(yscrollcommand=self.scroll_y.set)
        # self.configure(xscrollcommand=self.scroll_x.set)
        self.scroll_y.pack(fill='y', side='right')
        # self.scroll_x.pack(fill='x', side='bottom')


class Page(ttk.Frame):
    pageId = ''

    def __init__(self, widget, pageId):
        super().__init__(master=widget)
        self.pageId = pageId
