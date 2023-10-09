def handle(req: dict, db = None) -> None | int:
    match req["type"]:
        case "Otp":
            return handleOtp(req["number"])
        case "Database":
            return handleDB(db, req["query"])
        case _:
            return -1

def handleOtp(number: int):
    pass

def handleDB(db, req: dict):
    match req["type"]:
        case _:
            return -1

def dbCreate(db, req: dict):
    pass

def dbRead(db, req: dict):
    pass

def dbUpdate(db, req: dict):
    pass

def dbDelete(db, req: dict):
    pass