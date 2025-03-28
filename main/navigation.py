class RobotNavigator:
    def __init__(self, map_matrix):
        self.map_matrix = map_matrix
        self.map_height = len(map_matrix)
        self.map_width = len(map_matrix[0]) if self.map_height > 0 else 0
        self.x = 0
        self.y = 0
        self.facing = 'N'  # 'N', 'E', 'S', 'W'
        self.encoder_distance = 0  # distance since last line crossing

    def update_position_on_line_crossing(self):
        if self.facing == 'N':
            self.y += 1
        elif self.facing == 'S':
            self.y -= 1
        elif self.facing == 'E':
            self.x += 1
        elif self.facing == 'W':
            self.x -= 1
        self.encoder_distance = 0  # reset distance

    def rotate(self, direction):
        directions = ['N', 'E', 'S', 'W']
        idx = directions.index(self.facing)
        if direction == 'left':
            self.facing = directions[(idx - 1) % 4]
        elif direction == 'right':
            self.facing = directions[(idx + 1) % 4]

    def add_encoder_distance(self, distance):
        self.encoder_distance += distance

    def get_closest_sensor_to_wall(self):
        distances = {
            'N': self.map_height - 1 - self.y,
            'S': self.y,
            'E': self.map_width - 1 - self.x,
            'W': self.x
        }

        if self.facing == 'N':
            front_dir = 'N'
            left_dir = 'W'
        elif self.facing == 'S':
            front_dir = 'S'
            left_dir = 'E'
        elif self.facing == 'E':
            front_dir = 'E'
            left_dir = 'N'
        elif self.facing == 'W':
            front_dir = 'W'
            left_dir = 'S'

        return 'front' if distances[front_dir] <= distances[left_dir] else 'left'

    def get_position(self):
        return self.x, self.y

    def get_facing(self):
        return self.facing

    def get_current_square(self):
        return self.map_matrix[self.y][self.x]
