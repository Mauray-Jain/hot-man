import tkinter
from socket import *
from Client.page import *
from Middle.api import send, recv

class Scrollable(tk.Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame,
       call the update() method to refresh the scrollable area.
    """
    #                       repurposed from https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter
    #                       comment by user tarqez on feb 7 at 20:32 from a windows machine at ip: 151.0.144.83::2030
    def __init__(self, frame, width=16):

        scrollbar = tk.Scrollbar(frame, width=width)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        tk.Frame.__init__(self, frame)

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tk.NW)


    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas width"

        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width = canvas_width)

    def update(self):
        "Update the canvas and the scrollregion"

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))


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
            print('Opening ', pageNo)
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
        phoneNumber = tkinter.StringVar()
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
        otp = tkinter.IntVar()
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

    @staticmethod
    def getMenuItemBox(menupage, title, itemlst) -> ttk.Frame:
        foodBox = ttk.Frame(master=menupage)
        foodBox.rowconfigure(0, weight=2)
        for i in range(1, len(itemlst)):
            foodBox.rowconfigure(i, weight=1)
        foodBox.columnconfigure(0, weight=3)  # name
        foodBox.columnconfigure(1, weight=1)  # price
        foodBox.columnconfigure(2, weight=1)  # add to cart
        ttk.Label(
            master=foodBox,
            text=title,
            style='h1.TLabel'
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W)
        curow = 0
        for itm in itemlst:
            curow += 1
            ttk.Label(
                master=foodBox,
                text=itm[0],
                style='h2.TLabel'
            ).grid(row=curow, column=0)
            ttk.Label(
                master=foodBox,
                text=itm[1],
                style='h2.TLabel'
            ).grid(row=curow, column=1)
        return foodBox

    def makeMenu(self) -> Page:
        pageObj = Page(self, 'Menu')
        self.getHeader('Menu', pageObj).pack(ipadx=self.width)
        menyou = self.getMenu()
        if not menyou['status'] == 'Success':
            raise 'server error status != \'Success\''
        menyou = menyou['content']
        for key in menyou:
            self.getMenuItemBox(pageObj, key, menyou[key]).pack(ipadx=self.width)
        Scrollable(pageObj, width=20)
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
        self.getHeader('yourHonor', pageObj, False).pack(ipadx=self.width, ipady=60)
        return pageObj
