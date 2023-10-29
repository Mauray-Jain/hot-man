def handle(req: dict, db = None):
    x = req["type"]
    if x == "Otp":
        return handleOtp(req["number"])
    elif x == "Database":
        return handleDB(db, req["query"])
    else:
        return -1

def handleDB(db, req: dict):
    x =  req["type"]
    if x:
        pass
    else:
        return -1

def handleOtp(number: int):
    pass

def dbCreate(db, req: dict):
    pass

def dbRead(db, req: dict):
    pass

def dbUpdate(db, req: dict):
    pass

def dbDelete(db, req: dict):
    pass
