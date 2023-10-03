from Client_Python_Modules.page import *


class App(tk.Tk):
    height = 720
    width = 1080
    iconPath = 'Images/favicon.ico'
    pages = []

    def __init__(self):
        super().__init__()
        self.title('Restaurant management system')
        self.geometry(str(self.width) + 'x' + str(self.height))
        self.resizable(False, False)
        self.iconbitmap(self.iconPath)
        self.createPages()
        self.pages[0].pack()

    def createPages(self):
        startPage = Page(self, 'start page')
        heading = ttk.Label(
            master=startPage,
            text='Name_Of_Restaurant'
        )
        heading.pack()
        signIn = ttk.Button(
            master=startPage,
            text='Sign in',
            command=lambda: self.switch(1)
        )
        signUp = ttk.Button(
            master=startPage,
            text='sign up',
            command=lambda: self.switch(2)
        )
        signIn.pack()
        signUp.pack()
        self.pages.append(startPage)

    def switch(self, pageNo: int):
        print('switching to', pageNo)
        pass
