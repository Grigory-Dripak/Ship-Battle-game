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
                    if not self.coords in aims:
                        raise ValueError('Ошибочная координата, необходимо повторить ввод')
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
        self.armada = {'Корабль 5': 1,
                        'Корабль 6': 1}
        for ships, sizes in self.armada.items():
            self.armada[ships] = Ship(ships, sizes)

    def set_fleetposition(self, user):
        for names, ships in self.armada.items():
            ships.position = user
            # print(ships.position)



class GameRun:
    def __init__(self, field_size, user1, user2):
        self.user1 = GameUser(user1)
        self.user2 = GameUser(user2)
        self.fleet1 = UserFleet(field_size)
        self.fleet2 = UserFleet(field_size)


    def gameprocess(self):
        self.fleet1.show_chess()
        print(self.fleet1.myfield_coords)
        for name, ships in self.fleet1.armada.items():
            for point in range(ships.ship_size):
                msg = f'Введи через пробел номер стоки и колонки для координаты {point + 1} из {ships.ship_size} {name}:\n'
                coords = self.user1.coordsinput(self.fleet1.myfield_coords, msg)
                ships.position = coords
                self.fleet1.draw_myfield(coords)
                self.fleet1.show_chess()





if __name__ == "__main__":
    run = GameRun(6, 'USER 1', 'PC')
    run.gameprocess()
