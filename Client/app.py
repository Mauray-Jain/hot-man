import tkinter
from socket import socket
from Client.page import *
from Middle.api import send

class App(tk.Tk):
    height: int = 720
    width: int = 1080
    curPage: int = 0
    # iconPath = 'Images/favicon.ico'
    pages: list
    pageCreatorPrototypes: dict
    sock: socket

    def __init__(self, s):
        super().__init__()
        self.pageCreatorPrototypes = {
            0: self.makeStartPage,
            1: self.makeSignIn,
            2: self.makeSignUp
        }
        self.title('Restaurant management system')
        self.geometry(str(self.width) + 'x' + str(self.height))
        self.resizable(False, False)
        self.pages = [None] * 100
        # self.iconbitmap(self.iconPath)
        self.createPage(0)
        self.pages[self.curPage].pack()
        self.sock = s

    def switch(self, pageNo: int, popup: bool = False) -> None:
        if popup:
            print('Popup no :', pageNo)
            self.openPopup(pageNo)
            return
        else:
            print('switching to', pageNo)
        self.pages[self.curPage].pack_forget()
        self.curPage = pageNo
        if self.pages[self.curPage] != None:
            self.pages[self.curPage].pack() #this is in try
        else:
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

    def sendOtp(self, number):
        num: int  = number.get()
        print('send otp to', num)
        send(self.sock, {"type": "otp", "num": num})

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
        ttk.Button(
            master=signIn,
            text='use otp',
            command=lambda: self.switch(4)
        ).pack()
        return signIn

    def makeSignUp(self) -> Page:
        signUp = Page(self, 'signUp')
        ttk.Button(
            master=signUp,
            text='back',
            command=lambda: self.switch(0)
        ).pack()
        name = tkinter.StringVar()
        ttk.Label(
            master=signUp,
            text='Name'
        ).pack()
        ttk.Entry(
            master=signUp,
            textvariable=name
        ).pack()
        phoneNumber = tkinter.IntVar()
        ttk.Label(
            master=signUp,
            text='phoneNumber'
        ).pack()
        ttk.Entry(
            master=signUp,
            textvariable=phoneNumber
        ).pack()
        password = tkinter.StringVar()
        ttk.Label(
            master=signUp,
            text='Password'
        ).pack()
        ttk.Entry(
            master=signUp,
            textvariable=password
        ).pack()
        confirnPassword = tkinter.StringVar()
        ttk.Label(
            master=signUp,
            text='confirnPassword'
        ).pack()
        ttk.Entry(
            master=signUp,
            textvariable=confirnPassword
        ).pack()
        otp = tkinter.IntVar()
        ttk.Button(
            master=signUp,
            text='(re)send otp',
            command=lambda num=phoneNumber,calable=self: calable.sendOtp(num)
        ).pack()
        ttk.Label(
            master=signUp,
            text='otp'
        ).pack()
        ttk.Entry(
            master=signUp,
            textvariable=otp
        ).pack()
        return signUp
