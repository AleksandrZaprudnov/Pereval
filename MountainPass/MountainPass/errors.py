from fastapi.responses import JSONResponse


def ReJSONResponse(status_code: int, message: str):
    return JSONResponse(
        status_code=status_code,
        content={'status': status_code, 'message': message, 'id': None}
    )


class ErrorNumberDetails(Exception):
    def __init__(self, name: str):
        self.name = name


class ErrorCreatingRecord(Exception):
    def __init__(self, name: str):
        self.name = name


class ErrorConnectionServer(Exception):
    def __init__(self, name: str):
        self.name = name

