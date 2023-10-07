from Client_Python_Modules.page import *


class App(tk.Tk):
    height = 720
    width = 1080
    # iconPath = 'Images/favicon.ico'
    pages = []

    def __init__(self):
        super().__init__()
        self.title('Restaurant management system')
        self.geometry(str(self.width) + 'x' + str(self.height))
        self.resizable(False, False)
        # self.iconbitmap(self.iconPath)
        self.createPages()
        self.pages[0].pack()

    def createPages(self):
        startPage = Page(self, 'start page')
        ui_obj = ttk.Label(
            master=startPage,
            text='Name_Of_Restaurant'
        )
        ui_obj.add = lambda me=ui_obj: me.pack()
        startPage.addChild(ui_obj)
        ui_obj = ttk.Button(
            master=startPage,
            text='Sign in',
            command=lambda: self.switch(1)
        )
        ui_obj.add = lambda me=ui_obj: me.pack()
        startPage.addChild(ui_obj)
        ui_obj = ttk.Button(
            master=startPage,
            text='sign up',
            command=lambda: self.switch(2)
        )
        ui_obj.add = lambda me=ui_obj: me.pack()
        startPage.addChild(ui_obj)
        ui_obj = ttk.Button(
            master=startPage,
            text='Staff',
            command=self.staffLogin
        )
        ui_obj.add = lambda me=ui_obj: me.pack()
        startPage.addChild(ui_obj)
        ui_obj = ttk.Button(
            master=startPage,
            text='guest',
            command=lambda: self.switch(1, True)
        )
        ui_obj.add = lambda me=ui_obj: me.pack()
        startPage.addChild(ui_obj)
        self.pages.append(startPage)


    def switch(self, pageNo: int, popup: bool = False):
        if popup:
            print('Popup no :', pageNo)
        else:
            print('switching to', pageNo)

    def staffLogin(self):
        print('switch to staff site')
