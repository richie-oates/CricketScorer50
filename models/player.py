class Player:
    def __init__(self, number, name, id=None):
        self.number = number
        self.name = name
        self.id = id

    def __str__(self):
        return (f"{self.number} | {self.name} | {self.id}")
    
    def to_dict(self):
        return {
            "number" : self.number,
            "name" : self.name,
            "id" : self.id
        }
    
    @classmethod
    def from_dict(cls, d):
        return cls(d["number"], d["name"], d["id"])