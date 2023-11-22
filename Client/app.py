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
            # 2: self.makeSignUp,                     # bhap
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
        st.configure('mainPage.TButton', font=('Times New Roman', 28))
        st.configure('h-1.TLabel', font=('Times New Roman', 38))
        st.configure('h0.TEntry', font=('Times New Roman', 28))
        st.configure('h0.TLabel', font=('Times New Roman', 28))
        st.configure('h0.TButton', font=('Times New Roman', 38))
        st.configure('h1.TLabel', font=('Times New Roman', 22))
        st.configure('h2.TLabel', font=('Times New Roman', 18))
        st.configure('h1.TButton', font=('Times New Roman', 22))
        st.configure('h2.TButton', font=('Times New Roman', 18))
        return st

    def switch(self, pageNo: int, bake: bool = False) -> None:
        if not bake:
            self.back.append(self.curPage)
        # self.back.append(self.curPage)
        if not (self.pages[self.curPage] is None):
            self.pages[self.curPage].pack_forget()
        self.curPage = pageNo
        if pageNo == 22 and not self.pages[22] is None:
            self.pages[22].destroy()
            del self.pages[22]
            self.pages[22] = None
        if self.pages[self.curPage] is None:
            self.createPage(pageNo)
        self.pages[self.curPage].pack(ipadx=self.width, ipady=self.height)

    def updateCart(self):
        self.pages[22].destroy()
        del self.pages[22]
        self.pages[22] = None
        self.switch(22, True)

    def validateSignIn(self, number):
        self.phno = number.get()
        n = len(str(self.phno))
        if n == 10:
            self.switch(21)

    def addToCart(self, x, remove=False) -> None:
        print(f'adding {x} to cart')
        query = {"type": "Database", "query": {"type": "Update", "table": "cart",
                                               "content": {'name': x, 'user': self.phno, 'quantity': (1, -1)[remove]}}}
        send(self.sock, query)
        if recv(self.sock)['status'] == 'Invalid':
            raise 'couldn\'t add to cart please try again'

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
        ttk.Frame(master=startPage).pack(ipady=60)
        ttk.Button(master=startPage,
                   text='Sign In',
                   style='h0.TButton',
                   command=lambda: self.switch(1)
                   ).pack(
            anchor=tk.CENTER,
            padx=20,
            pady=10)
        return startPage

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                int(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

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
            text='Enter 10 Digit Phone Number',
            style='h1.TLabel'
        ).pack(
            pady=(15, 5)
        )
        phoneNumber = tk.IntVar()
        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        ttk.Entry(master=pageObj, textvariable=phoneNumber, style='h0.TEntry', validate='key',
                  validatecommand=vcmd).pack(
            ipady=5,
            ipadx=60,
            pady=15
        )
        ttk.Frame(master=pageObj).pack(pady=40)
        buttonBox = ttk.Frame(master=pageObj)
        ttk.Button(master=buttonBox,
                   text='sign in',
                   style='mainPage.TButton',
                   command=lambda _self=self, num=phoneNumber: _self.validateSignIn(num)
                   ).pack(
            pady=40,
            padx=20,
            anchor=tk.W)
        buttonBox.pack(
            anchor=tk.CENTER
        )
        return pageObj

    def getMenu(self):
        send(self.sock, {"type": "Database", "query": {"type": "Read", "table": "menu", "content": ""}})
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
        self.getHeader('Menu', pageObj.fr).grid(row=0, column=0, ipadx=267)

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
        pageObj.pack(anchor=tk.NW, ipadx=self.width, ipady=self.width, padx=0, pady=0)
        return pageparentobj

    def getHeader(self, text: str, parent: Page | ttk.Frame | FrameWithScrollBar, canKart=True,
                  removePlaceOrder=False) -> ttk.Frame:
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
        elif not removePlaceOrder:
            ttk.Button(
                master=pageObj,
                text='Place Order',
                style='mainPage.TButton',
                command=lambda: self.placeOrder()
            ).pack(anchor=tk.NE)
        return pageObj

    def makeCart(self) -> Page:
        pageObj = Page(self, 'yourHonor')
        send(self.sock, {"type": "Database", "query": {"type": "Read", "table": "cart",
                                                       "content": {"user": self.phno}}})
        try:
            rawData = recv(self.sock)['content']
        except:
            rawData: dict = {'Total': 0}
        data: list = []
        totalCost: int = 0
        for i in rawData:
            if i == 'Total':
                totalCost = rawData[i]
            else:
                data += rawData[i]
            # data += i
        if len(rawData) == 1:
            self.getHeader('Cart', pageObj, False, removePlaceOrder=True).place(x=0, y=0, width=1080)
            ttk.Label(master=pageObj,
                      text='Your Cart is Empty',
                      style='h-1.TLabel'
                      ).place(x=350, y=300)
            return pageObj
        cartTable = ttk.Frame(pageObj)
        self.getHeader('Cart', cartTable, False).grid(row=0, column=0, columnspan=5, sticky='w', ipadx=288)
        cartTable.columnconfigure(0, weight=3, uniform='0')  # name
        cartTable.columnconfigure(1, weight=1, uniform='1')  # price
        cartTable.columnconfigure(2, weight=1, uniform='2')  # decrease
        cartTable.columnconfigure(3, weight=1, uniform='3')  # quantity
        cartTable.columnconfigure(4, weight=1, uniform='4')  # increase
        cartTable.rowconfigure(0, weight=2)  # title
        cartTable.rowconfigure(1, weight=2)  # title
        for i in range(len(data) + 1):
            cartTable.rowconfigure(i + 2, weight=1)
        ttk.Label(
            master=cartTable,
            text='Name',
            style='h1.TLabel'
        ).grid(row=1, column=0, padx=0, pady=20, ipadx=0, ipady=20)
        ttk.Label(
            master=cartTable,
            text='Price',
            style='h1.TLabel'
        ).grid(row=1, column=1, padx=0, pady=20, ipadx=0, ipady=20)
        ttk.Label(
            master=cartTable,
            text='Quantity',
            style='h1.TLabel'
        ).grid(row=1, column=2, columnspan=3, padx=0, pady=20, ipadx=0, ipady=20)
        rowno: int = 1
        for rowdt in data:
            rowno += 1
            ttk.Label(
                master=cartTable,
                text=rowdt[0],
                style='h2.TLabel'
            ).grid(row=rowno, column=0, padx=0, pady=0, ipadx=0, ipady=20)
            ttk.Label(
                master=cartTable,
                text=rowdt[1],
                style='h2.TLabel'
            ).grid(row=rowno, column=1, padx=0, pady=0, ipadx=0, ipady=20)
            ttk.Button(
                master=cartTable,
                text='less',
                style='h2.TButton',
                command=lambda _self=self, x=rowdt: _self.addToCart(x=x[0], remove=True) or _self.updateCart()
                #  jank hack that works
            ).grid(row=rowno, column=2, pady=10, ipady=20)
            ttk.Label(
                master=cartTable,
                text=rowdt[2],
                style='h2.TLabel'
            ).grid(row=rowno, column=3, padx=0, pady=0, ipadx=0, ipady=20)
            ttk.Button(
                master=cartTable,
                text='more',
                style='h2.TButton',
                command=lambda _self=self, x=rowdt: _self.addToCart(x=x[0]) or _self.updateCart()
                #                                                              |^| jank hack that works
            ).grid(row=rowno, column=4, pady=10, ipady=20)
        rowno += 1
        ttk.Label(
            master=cartTable,
            text='total',
            style='h2.TLabel'
        ).grid(row=rowno, column=0, columnspan=2, padx=0, pady=0, ipadx=0, ipady=20)
        ttk.Label(
            master=cartTable,
            text=totalCost,
            style='h2.TLabel'
        ).grid(row=rowno, column=2, columnspan=3, padx=0, pady=0, ipadx=0, ipady=20)
        cartTable.pack(ipadx=self.width, fill='both', anchor=tk.NW)
        return pageObj

    def placeOrder(self):
        req = {"type": "Database", "query": {"type": "Update", "table": "orders", "content": {'user': self.phno}}}
        send(self.sock, req)
        if recv(self.sock)['status'] == 'Invalid':
            raise 'Connection error cannot add to order'
        self.updateCart()
