from random import randint

class GameUser:
    def __init__(self, id='PC'):
        self.id = id

    def coordsinput(self, aims, message='Введи координаты через пробел:\n'):
        if self.id == 'PC':
            self.coords = aims[randint(0, len(aims)-1)]
        else:
            repeate = True
            while repeate:
                try:
                    self.coords = tuple(map(int, input(message).split()))
                except ValueError as e:
                    print(e)
                else:
                    repeate = False
        return self.coords



class Field:
    def __init__(self, field_size=6):
        self.field_size = field_size
        self.my_field = [["-" for j in range(self.field_size)] for i in range(self.field_size)]
        self.myfield_coords = [(i, j) for j in range(1, self.field_size + 1) for i in range(1, self.field_size + 1)]
        self.enemy_field = [["-" for j in range(self.field_size)] for i in range(self.field_size)]

    def draw_myfield(self, point, status='+'):
        self.my_field[point[0]-1][point[1]-1] = status

    def draw_enemyfield(self, point, status='+'):
        self.my_field[point[0]-1][point[1]-1] = status

    def show_chess(self):
        # демонстрация поля вместе с осями координат
        print(' ', end='')
        for _ in range(1, self.field_size + 1):
            print(f' | {_}', end='')
        print(' |    ||   ', end='')
        for _ in range(1, self.field_size + 1):
            print(f' | {_}', end='')
        print(' |')

        for i in range(1, self.field_size + 1):
            print(f"{i} | {' | '.join(self.my_field[i - 1])} |    ||    | {' | '.join(self.enemy_field[i - 1])} | {i}")




class Ship:
    def __init__(self, name, ship_size, position=[], status=1):
        self.name = name
        self.ship_size = ship_size
        self.status = status
        self.__position = position

    @property
    def position(self):
        return self.position

    @position.setter
    def position(self, coords):
        self.__position.append(coords)

class UserFleet(Field):
    """'Корабль 1': 3,
                        'Корабль 2': 2,
                        'Корабль 3': 2,
                        'Корабль 4': 1,"""
    def __init__(self, field_size):
        super().__init__(field_size)
        self.infleet = {'Корабль 5': 1,
                        'Корабль 6': 1}
        for ships, sizes in self.infleet.items():
            self.infleet[ships] = Ship(ships, sizes)

    def set_fleetposition(self, user):
        for names, ships in self.infleet.items():
            ships.position = user
            # print(ships.position)



class GameRun:
    def __init__(self, field_size, user1, user2):
        self.user1 = user1
        self.user2 = user2
        self.field_size = field_size


    def gameprocess(self):
        self.user1_fleet = UserFleet(self.field_size)
        self.user1_fleet.show_chess()
        print(self.user1_fleet.myfield_coords)
        self.user1_fleet.set_fleetposition(self.user1)




if __name__ == "__main__":
    run = GameRun(6, 'USER 1', 'PC')
    run.gameprocess()
