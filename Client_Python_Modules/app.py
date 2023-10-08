import tkinter

from Client_Python_Modules.page import *


class App(tk.Tk):
    height: int = 720
    width: int = 1080
    curPage: int = 0
    # iconPath = 'Images/favicon.ico'
    pages: list
    pageCreatorPrototypes: dict

    def __init__(self):
        super().__init__()
        self.pageCreatorPrototypes = {
            0: self.makeStartPage,
            1: self.makeSignIn
        }
        self.title('Restaurant management system')
        self.geometry(str(self.width) + 'x' + str(self.height))
        self.resizable(False, False)
        self.pages = [None] * 100
        # self.iconbitmap(self.iconPath)
        self.createPage(0)
        self.pages[self.curPage].pack()

    def switch(self, pageNo: int, popup: bool = False) -> None:
        if popup:
            print('Popup no :', pageNo)
            self.openPopup(pageNo)
            return
        else:
            print('switching to', pageNo)
        self.pages[self.curPage].pack_forget()
        self.curPage = pageNo
        try:
            self.pages[self.curPage].pack()
        except AttributeError:
            self.createPage(pageNo)
            self.pages[self.curPage].pack()

    def openPopup(self, popupno: int) -> None:
        pass

    def staffLogin(self):
        print('switch to staff site')

    def validateSignIn(self, number, passwd):
        print('checking credentials ....')
        print(number.get(), '\t:\t', passwd.get())
        print('if fine: switch, else : popup(message)')

    def createPage(self, pageNo: int = 0):
        self.pages[pageNo] = self.pageCreatorPrototypes[pageNo]()

    def makeStartPage(self) -> Page:
        startPage = Page(self, 'start page')
        ttk.Label(
            master=startPage,
            text='Name_Of_Restaurant'
        ).pack()
        ttk.Button(
            master=startPage,
            text='Sign in',
            command=lambda: self.switch(1)
        ).pack()
        ttk.Button(
            master=startPage,
            text='sign up',
            command=lambda: self.switch(2)
        ).pack()
        ttk.Button(
            master=startPage,
            text='Staff',
            command=self.staffLogin
        ).pack()
        ttk.Button(
            master=startPage,
            text='guest',
            command=lambda: self.switch(1, True)
        ).pack()
        return startPage

    def makeSignIn(self) -> Page:
        signIn = Page(self, 'sign in')
        ttk.Button(
            master=signIn,
            text='back',
            command=lambda: self.switch(0)
        ).pack()
        ttk.Label(
            master=signIn,
            text='Number'
        ).pack()
        phoneNumber = tkinter.StringVar()
        ttk.Entry(
            master=signIn,
            textvariable=phoneNumber
        ).pack()
        ttk.Label(
            master=signIn,
            text='Password'
        ).pack()
        password = tkinter.StringVar()
        ttk.Entry(
            master=signIn,
            textvariable=password,
            show='*'
        ).pack()
        ttk.Button(
            master=signIn,
            text='sign in',
            command=lambda self=self, num=phoneNumber, pwd=password: self.validateSignIn(num, pwd)
        ).pack()
        return signIn
