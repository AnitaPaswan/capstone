import enum

class Gender(enum.Enum):
    Male ='Male'
    Female= 'Female'
    Other= 'Other'

    @classmethod
    def choices(cls):
        return[(choice.name, choice.value) for choice in cls]
        
