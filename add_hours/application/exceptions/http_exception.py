class HTTPException(Exception):
    status_code: int = 400
    message: str = None
    code: str = None

    def __init__(self, *args: str):
        super().__init__(*args)
        if args:
            self.message = args[0]
