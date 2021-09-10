class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        new_x = self.x + other.x
        new_y = self.y + other.y
        return Vector(new_x, new_y)
    
    def __sub__(self, other):
        new_x = self.x - other.x
        new_y = self.y - other.y
        return Vector(new_x, new_y)

    def dot_product(self, other):
        return (self.x * other.x) + (self.y * other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)