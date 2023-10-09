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


class Page(ttk.Frame):
    pageId = ''

    def __init__(self, widget, pageId):
        super().__init__(master=widget)
        self.pageId = pageId
