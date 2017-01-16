class Error(Exception):
    pass


class Warning(Exception):
    pass


class EndOfSessionException(Error):
    def __init__(self):
        self.message = "init session has ended"


class NewSessionWarning(Warning):
    def __init__(self):
        self.message = "a new init session has been initialized"
