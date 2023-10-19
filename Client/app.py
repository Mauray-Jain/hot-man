import tkinter
from socket import socket
from Client.page import *
from Middle.api import send


class App(tk.Tk):
    height: int = 720
    width: int = 1080
    curPage: int = 0
    # iconPath = './../Images/favicon.ico'
    pages: list
    pageCreatorPrototypes: dict
    sock: socket
    back: list = [0]

    def __init__(self, s):
        super().__init__()
        self.pageCreatorPrototypes = {
            0: self.makeStartPage,
            # 11: self.makeSignIn,                    # depreciated
            2: self.makeSignUp,
            1: self.makeSignInOtp,
            21: self.makeMenu,
            22: self.makeCart
        }
        self.title('Restaurant management system')
        self.geometry(str(self.width) + 'x' + str(self.height))
        self.resizable(False, False)
        self.getStyle()
        self.pages = [None] * 100
        # self.iconbitmap(self.iconPath)
        self.createPage(0)
        self.pages[self.curPage].pack(ipadx=self.width,ipady=self.height)
        self.sock = s

    def getStyle(self)->ttk.Style:
        st = ttk.Style()
        st.configure('mainPage.TButton', font=('Times New Roman', 24))
        st.configure('h0.TEntry', font=('Times New Roman', 24))
        st.configure('h0.TLabel', font=('Times New Roman', 24))
        return st

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
        if self.pages[self.curPage] == None:
            self.createPage(pageNo)
        self.pages[self.curPage].pack(ipadx=self.width,ipady=self.height)

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
        restName = ttk.Label(master=startPage, text='Name_Of_Restaurant')
        restName.config(font=('Comic Sans MS', 64, 'italic'))
        restName.pack(
                   anchor=tk.CENTER,
                   padx=20,
                   pady=80)
        button_font = ('Comic Sans MS', 32, 'bold')
        but1 = ttk.Button(master=startPage,
                   text='Sign In',
                   style='mainPage.TButton',
                   command=lambda: self.switch(1)
                ).pack(
                   anchor=tk.CENTER,
                   padx=20,
                   pady=10)
        but2 = ttk.Button(master=startPage,
                   text='Sign Up',
                   style='mainPage.TButton',
                   command=lambda: self.switch(2)
                ).pack(
                   anchor=tk.CENTER,
                   padx=20,
                   pady=10)
        return startPage

    # def makeSignIn(self) -> Page:
    #     pageObj = Page(self, 'sign in')
    #     ttk.Button(master=pageObj, text='back', command=self.goBack).pack()
    #     ttk.Label(master=pageObj, text='Number').pack()
    #     phoneNumber = tkinter.StringVar()
    #     ttk.Entry(master=pageObj, textvariable=phoneNumber).pack()                                REMOVED
    #     ttk.Label(master=pageObj, text='Password').pack()
    #     password = tkinter.StringVar()
    #     ttk.Entry(master=pageObj, textvariable=password, show='*').pack()
    #     ttk.Button(master=pageObj,
    #                text='sign in',
    #                command=lambda self=self, num=phoneNumber, pwd=password:
    #                self.validateSignIn(num, pwd)).pack()
    #     ttk.Button(master=pageObj,
    #                text='use otp',
    #                command=lambda: self.switch(4)).pack()
    #     return pageObj

    def makeSignUp(self) -> Page:
        pageObj = Page(self, 'pageObj')
        ttk.Button(
            master=pageObj,
            text='back',
            command=self.goBack).pack()
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
        ttk.Button(
                   master=pageObj,
                   text='back',
                   command=self.goBack,
                   style='mainPage.TButton'
##        ).pack(
##                   padx=0,
##                   pady=0,
##                   anchor=tk.W,
##                   expand=True)
          ).place(x=0,y=0)
        ttk.Frame(master=pageObj).pack(pady=40,padx=720)
        ttk.Label(
                   master=pageObj,
                   text='Number',
                   style='h0.TLabel'
        ).pack(
               padx=20,
               pady=15,
               expand=True
        )
        phoneNumber = tkinter.StringVar()
        ttk.Entry(master=pageObj, textvariable=phoneNumber, style='h0.TEntry').pack(
               ipady=5,
               ipadx=60,
               padx=20,
               pady=15,
               expand=True)
        ttk.Label(
                   master=pageObj,
                   text='otp',
                   style='h0.TLabel'
        ).pack(
               padx=60,
               pady=15,
               expand=True
        )
        otp = tkinter.IntVar()
        ttk.Entry(master=pageObj, textvariable=otp, style='h0.TEntry').pack(
               ipady=5,
               ipadx=60,
               padx=60,
               pady=15,
               expand=True)
        
        ttk.Frame(master=pageObj).pack(pady=40)
        ttk.Button(master=pageObj,
                   text='send otp',
                   style='mainPage.TButton',
                   command=lambda self=self, num=phoneNumber, calable=self: calable.sendOtp(phoneNumber)
        ).pack(pady = 40, padx = (360,20), anchor=tk.S, side=tk.LEFT)
        ttk.Button(master=pageObj,
                   text='sign in',
                   style='mainPage.TButton',
                   command=lambda self=self, num=phoneNumber, pwd=otp: self.
                   validateSignIn(num, pwd)).pack(pady = 40, padx = 40, anchor=tk.W)
        return pageObj

    def makeMenu(self) -> Page:
        pageObj = Page(self, 'Menu')
        self.getHeader('Menu', pageObj).pack(ipadx=self.width,ipady=60)
        return pageObj

    def getHeader(self, text: str, parent: Page, canKart=True) -> ttk.Frame:
        pageObj = ttk.Frame(master=parent)
        ttk.Button(
                   master=pageObj,
                   text='back',
                   style='mainPage.TButton',
                   command=self.goBack
                   ).pack(
                       anchor=tk.NW,
                       side=tk.LEFT
                       )
        ttk.Label(
                  master=pageObj,
                  text=text,
                  style='h0.TLabel'
                  ).pack(
                         anchor=tk.N,
                         expand=True,
                         side=tk.LEFT)
        if canKart:
            ttk.Button(
                       master=pageObj,
                       text='cart',
                       style='mainPage.TButton',
                       command=lambda: self.switch(22)
                       ).pack(anchor=tk.NE)
        return pageObj

    def makeCart(self) -> Page:
        pageObj = Page(self, 'yourHonor')
        self.getHeader('yourHonor', pageObj, False).pack(ipadx=self.width,ipady=60)
        return pageObj
