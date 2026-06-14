from models.person import Person

class User(Person):

    def __init__(self, name, userid):
        super().__init__(name)
        self.userid = userid

    def check_balance(self, balance):
        return balance