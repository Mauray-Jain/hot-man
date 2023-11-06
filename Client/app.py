from socket import *
from Client.page import *
from Middle.api import send, recv


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
        self.phno = 0
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
        # self.createPage(0)
        # self.pages[self.curPage].pack(ipadx=self.width, ipady=self.height)
        self.switch(self.curPage)
        self.sock = s

    @staticmethod
    def getStyle() -> ttk.Style:
        st = ttk.Style()
        st.configure('mainPage.TButton', font=('Times New Roman', 32))
        st.configure('h0.TEntry', font=('Times New Roman', 32))
        st.configure('h0.TLabel', font=('Times New Roman', 32))
        st.configure('h1.TLabel', font=('Times New Roman', 24))
        st.configure('h2.TLabel', font=('Times New Roman', 18))
        st.configure('h1.TButton', font=('Times New Roman', 24))
        st.configure('h2.TButton', font=('Times New Roman', 18))
        return st

    def switch(self,
               pageNo: int,
               popup: bool = False,
               bake: bool = False) -> None:
        if popup:
            print('Popup no :', pageNo)
            self.openPopup(pageNo)
            return
        if not bake:
            self.back.append(self.curPage)
        # self.back.append(self.curPage)
        if not (self.pages[self.curPage] is None):
            self.pages[self.curPage].pack_forget()
        self.curPage = pageNo
        if self.pages[self.curPage] is None:
            self.createPage(pageNo)
        self.pages[self.curPage].pack(ipadx=self.width, ipady=self.height)

    def openPopup(self, popupno: int) -> None:
        pass

    @staticmethod
    def staffLogin():
        print('switch to staff site')

    def validateSignIn(self, number, passwd):
        print('checking credentials ....')
        print(number.get(), '\t:\t', passwd.get())
        print('if fine: switch, else : popup(message)')
        self.phno = number.get()
        self.switch(21)

    def sendOtp(self, number) -> None:
        num: int = number.get()
        print('send otp to', num)
        send(self.sock, {"type": "Otp", "number": num})
        # if recv(self.sock)['type'] == 'error':
        #     raise 'otp not send properly'
        recv(self.sock)

    def addToCart(self, x) -> None:
        print(f'adding {x} to cart')
        send(self.sock, {'type': 'Database', 'query': {"type": "write", "table": 'cart', "user": self.phno, 'content': x}})
        # if recv(self.sock)['type'] == 'error':
        #     raise 'couldn\'t add to cart please try again'
        recv(self.sock)

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
        ttk.Button(master=startPage,
                   text='Sign In',
                   style='mainPage.TButton',
                   command=lambda: self.switch(1)
                   ).pack(
            anchor=tk.CENTER,
            padx=20,
            pady=10)
        ttk.Button(master=startPage,
                   text='Sign Up',
                   style='mainPage.TButton',
                   command=lambda: self.switch(2)
                   ).pack(
            anchor=tk.CENTER,
            padx=20,
            pady=10)
        return startPage

    def makeSignUp(self) -> Page:
        pageObj = Page(self, 'pageObj')
        ttk.Button(
            master=pageObj,
            text='back',
            command=self.goBack).pack()
        name = tk.StringVar()
        ttk.Label(master=pageObj, text='Name').pack()
        ttk.Entry(master=pageObj, textvariable=name).pack()
        phoneNumber = tk.IntVar()
        ttk.Label(master=pageObj, text='phoneNumber').pack()
        ttk.Entry(master=pageObj, textvariable=phoneNumber).pack()
        password = tk.StringVar()
        ttk.Label(master=pageObj, text='Password').pack()
        ttk.Entry(master=pageObj, textvariable=password).pack()
        confirnPassword = tk.StringVar()
        ttk.Label(master=pageObj, text='confirnPassword').pack()
        ttk.Entry(master=pageObj, textvariable=confirnPassword).pack()
        otp = tk.IntVar()
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
        ).pack(
            padx=0,
            pady=0,
            anchor=tk.NW
        )
        ttk.Frame(master=pageObj).pack(pady=40)
        ttk.Label(
            master=pageObj,
            text='Number',
            style='h0.TLabel'
        ).pack(
            pady=(15, 5)
        )
        phoneNumber = tk.StringVar()
        ttk.Entry(master=pageObj, textvariable=phoneNumber, style='h0.TEntry').pack(
            ipady=5,
            ipadx=60,
            pady=15
        )
        ttk.Label(
            master=pageObj,
            text='otp',
            style='h0.TLabel'
        ).pack(
            pady=(15, 5)
        )
        otp = tk.IntVar()
        ttk.Entry(master=pageObj, textvariable=otp, style='h0.TEntry').pack(
            ipady=5,
            ipadx=60,
            pady=15)

        ttk.Frame(master=pageObj).pack(pady=40)
        buttonBox = ttk.Frame(master=pageObj)
        ttk.Button(master=buttonBox,
                   text='send otp',
                   style='mainPage.TButton',
                   command=lambda num=phoneNumber, callable=self: callable.sendOtp(phoneNumber)
                   ).pack(pady=40, padx=20, anchor=tk.S, side=tk.LEFT)
        ttk.Button(master=buttonBox,
                   text='sign in',
                   style='mainPage.TButton',
                   command=lambda _self=self, num=phoneNumber, pwd=otp: _self.validateSignIn(num, pwd)
                   ).pack(
            pady=40,
            padx=20,
            anchor=tk.W)
        buttonBox.pack(
            anchor=tk.CENTER
        )
        return pageObj

    def getMenu(self):
        send(self.sock, {"type": "Database", "query": {"type": "Read", "table": "menu", "content": "Why are we still "
                                                                                                   "here?"}})
        return recv(self.sock)

    def getMenuItemBox(self, menupage, title, itemlst, minsz=220) -> ttk.Frame:
        foodBox = ttk.Frame(master=menupage)
        foodBox.rowconfigure(0, weight=2, uniform='5')
        itemlst[0].append(0)
        for i in range(1, len(itemlst)):
            itemlst[i].append(0)
            foodBox.rowconfigure(i, weight=1, uniform='4')
        foodBox.columnconfigure(0, weight=2)  # name
        foodBox.columnconfigure(1, weight=1)  # price
        foodBox.columnconfigure(2, weight=1)  # add to cart
        ttk.Label(
            master=foodBox,
            text=title,
            style='h1.TLabel'
        ).grid(row=0, column=0, columnspan=3, sticky=tk.W, ipadx=minsz, pady=20)
        curow = 0
        for itm in itemlst:
            curow += 1
            ttk.Label(
                master=foodBox,
                text=itm[0],
                style='h2.TLabel'
            ).grid(row=curow, column=0, pady=10)
            ttk.Label(
                master=foodBox,
                text=itm[1],
                style='h2.TLabel'
            ).grid(row=curow, column=1, pady=10)
            ttk.Button(
                master=foodBox,
                text='AddToCart',
                style='h2.TButton',
                command=lambda _self=self, x=itm[0]: _self.addToCart(x=x)
            ).grid(row=curow, column=2, pady=10)
        return foodBox

    def makeMenu(self) -> Page | FrameWithScrollBar:
        pageparentobj = Page(self, 'Menu')
        pageObj = FrameWithScrollBar(pageparentobj, self)
        pageObj.columnconfigure(0, weight=1)
        pageObj.rowconfigure(0)
        self.getHeader('Menu', pageObj.fr).grid(row=0, column=0, ipadx=227)

        menyou = self.getMenu()
        if not menyou['status'] == 'Success':
            raise 'server error status != \'Success\''
        menyou = menyou['content']

        for i in range(len(menyou)):
            pageObj.rowconfigure(i)
        i: int = 0
        for key in menyou:
            i += 1
            self.getMenuItemBox(pageObj.fr, key, menyou[key], minsz=220).grid(row=i, column=0, ipadx=220, pady=20)
        pageObj.pack(anchor='nw', ipadx=self.width, ipady=self.width, padx=0, pady=0)
        return pageparentobj

    def getHeader(self, text: str, parent: Page | ttk.Frame, canKart=True) -> ttk.Frame:
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
        self.getHeader('yourHonor', pageObj, False).pack(ipadx=self.width, ipady=60)
        return pageObj
