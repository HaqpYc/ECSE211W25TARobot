class Square:
    def __init__(self, square_type: str):
        self.type = square_type  # 'H', 'M', or 'R'
        self.has_furniture = False  # Only relevant for main room ('M')

    def is_accessible(self):
        return self.type in ('H', 'M') and not (self.type == 'M' and self.has_furniture)

    def __repr__(self):
        if self.type == 'M' and self.has_furniture:
            return "F"  # Furniture in main room
        return self.type
