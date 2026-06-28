class WrongPasswordException(BaseException):
    def __init__(self, *args):
        super().__init__(*args) # custom Exception (just for semantics)