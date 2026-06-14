from models.person import Person

class Admin(Person):

    def __init__(self, name, empid):
        super().__init__(name)
        self.empid = empid