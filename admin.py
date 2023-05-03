class Admin:
    def __init__(self):
        self.users = {}

    def add_user(self, name, encoding):
        self.users[name] = encoding

    def remove_user(self, name):
        if name in self.users:
            del self.users[name]
