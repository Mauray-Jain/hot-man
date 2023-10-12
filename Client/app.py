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
    back: list = [0]

    def __init__(self, s):
        super().__init__()
        self.pageCreatorPrototypes = {
            0: self.makeStartPage,
            1: self.makeSignIn,
            2: self.makeSignUp,
            11: self.makeSignInOtp,
            21: self.makeMenu,
            22: self.makeCart
        }
        self.title('Restaurant management system')
        self.geometry(str(self.width) + 'x' + str(self.height))
        self.resizable(False, False)
        self.pages = [None] * 100
        # self.iconbitmap(self.iconPath)
        self.createPage(0)
        self.pages[self.curPage].pack()
        # self.sock = s

    def switch(self,
               pageNo: int,
               popup: bool = False,
               bake: bool = False) -> None:
        if popup:
            print('Popup no :', pageNo)
            self.openPopup(pageNo)
            return
        else:
            print('switching to', pageNo)
        if not bake:
            self.back.append(self.curPage)
        # self.back.append(self.curPage)
        self.pages[self.curPage].pack_forget()
        self.curPage = pageNo
        if self.pages[self.curPage] != None:
            self.pages[self.curPage].pack()  #this is in try
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
        self.switch(21)

    def sendOtp(self, number):
        num: int = number.get()
        print('send otp to', num)
        send(self.sock, {"type": "Otp", "number": num})

    def createPage(self, pageNo: int = 0):
        self.pages[pageNo] = self.pageCreatorPrototypes[pageNo]()

    def goBack(self) -> None:
        self.switch(self.back.pop(), bake=True)

    def makeStartPage(self) -> Page:
        startPage = Page(self, 'start page')
        ttk.Label(master=startPage, text='Name_Of_Restaurant').pack()
        ttk.Button(master=startPage,
                   text='signInOtpDirect',
                   command=lambda: self.switch(11)).pack()
        ttk.Button(master=startPage,
                   text='Sign in',
                   command=lambda: self.switch(1)).pack()
        ttk.Button(master=startPage,
                   text='sign up',
                   command=lambda: self.switch(2)).pack()
        ttk.Button(master=startPage, text='Staff',
                   command=self.staffLogin).pack()
        ttk.Button(master=startPage,
                   text='guest',
                   command=lambda: self.switch(1, True)).pack()
        return startPage

    def makeSignIn(self) -> Page:
        pageObj = Page(self, 'sign in')
        ttk.Button(master=pageObj, text='back', command=self.goBack).pack()
        ttk.Label(master=pageObj, text='Number').pack()
        phoneNumber = tkinter.StringVar()
        ttk.Entry(master=pageObj, textvariable=phoneNumber).pack()
        ttk.Label(master=pageObj, text='Password').pack()
        password = tkinter.StringVar()
        ttk.Entry(master=pageObj, textvariable=password, show='*').pack()
        ttk.Button(master=pageObj,
                   text='sign in',
                   command=lambda self=self, num=phoneNumber, pwd=password:
                   self.validateSignIn(num, pwd)).pack()
        ttk.Button(master=pageObj,
                   text='use otp',
                   command=lambda: self.switch(4)).pack()
        return pageObj

    def makeSignUp(self) -> Page:
        pageObj = Page(self, 'pageObj')
        ttk.Button(master=pageObj, text='back', command=self.goBack).pack()
        name = tkinter.StringVar()
        ttk.Label(master=pageObj, text='Name').pack()
        ttk.Entry(master=pageObj, textvariable=name).pack()
        phoneNumber = tkinter.IntVar()
        ttk.Label(master=pageObj, text='phoneNumber').pack()
        ttk.Entry(master=pageObj, textvariable=phoneNumber).pack()
        password = tkinter.StringVar()
        ttk.Label(master=pageObj, text='Password').pack()
        ttk.Entry(master=pageObj, textvariable=password).pack()
        confirnPassword = tkinter.StringVar()
        ttk.Label(master=pageObj, text='confirnPassword').pack()
        ttk.Entry(master=pageObj, textvariable=confirnPassword).pack()
        otp = tkinter.IntVar()
        ttk.Button(master=pageObj,
                   text='(re)send otp',
                   command=lambda num=phoneNumber, calable=self: calable.
                   sendOtp(num)).pack()
        ttk.Label(master=pageObj, text='otp').pack()
        ttk.Entry(master=pageObj, textvariable=otp).pack()
        return pageObj

    def makeSignInOtp(self) -> Page:
        pageObj = Page(self, 'sign in')
        ttk.Button(master=pageObj, text='back', command=self.goBack).pack()
        ttk.Label(master=pageObj, text='Number').pack()
        phoneNumber = tkinter.StringVar()
        ttk.Entry(master=pageObj, textvariable=phoneNumber).pack()
        ttk.Label(master=pageObj, text='otp').pack()
        otp = tkinter.IntVar()
        ttk.Entry(master=pageObj, textvariable=otp).pack()
        ttk.Button(master=pageObj,
                   text='sign in',
                   command=lambda self=self, num=phoneNumber, pwd=otp: self.
                   validateSignIn(num, pwd)).pack()
        return pageObj

    def makeMenu(self) -> Page:
        pageObj = Page(self, 'Menu')
        self.getHeader('Menu', pageObj).pack()
        return pageObj

    def getHeader(self, text: str, parent: Page, canKart=True) -> ttk.Frame:
        pageObj = ttk.Frame(master=parent)
        ttk.Button(master=pageObj, text='back',
                   command=self.goBack).pack(anchor=tk.W, side=tk.LEFT)
        ttk.Label(master=pageObj, text=text).pack(anchor=tk.CENTER,
                                                  side=tk.LEFT)
        if canKart:
            ttk.Button(master=pageObj,
                       text='cart',
                       command=lambda: self.switch(22)).pack(anchor=tk.E)
        return pageObj

    def makeCart(self) -> Page:
        pageObj = Page(self, 'yourHonor')
        self.getHeader('yourHonor', pageObj, False).pack()
        return pageObj
