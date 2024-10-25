class ThreadMakerException(Exception):
    def __init__(self, arg=""):
        self.arg = arg


class ThreadAlreadyExists(ThreadMakerException):
    def __str__(self):
        return f"this thread is already exists: {self.arg}"
