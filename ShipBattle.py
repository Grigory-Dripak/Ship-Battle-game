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
                    if self.coords not in aims:
                        raise ValueError('Ошибочная координата, необходимо повторить ввод')
                except ValueError as e:
                    print(e)
                else:
                    repeate = False
        return self.coords



class Field:
    def __init__(self, field_size=6):
        self.field_size = field_size
        self.my_field = [["-" for _ in range(self.field_size)] for _ in range(self.field_size)]
        self.enemy_field = [["-" for _ in range(self.field_size)] for _ in range(self.field_size)]

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
    def __init__(self, name, ship_size, status=1):
        self.name = name
        self.ship_size = ship_size
        self.status = status
        self.__position = []

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, coords):
        self.__position.append(coords)

    def close_positions(self, field):
        self.cl_pos = []
        for point in self.__position:
            p = lambda i, j: (point[0]+i, point[1]+j)
            some_points = [p(i, j) for i in range(-1, 2) for j in range(-1, 2)]
            for sp in some_points:
                if sp in field and sp not in self.cl_pos:
                    self.cl_pos.append(sp)
        return self.cl_pos

    def possible_pos(self, field):
        self.ps_pos = []

        if len(self.__position) > 1:
            if self.__position[0][0] == self.__position[1][0]:
                s = self.minmax_value(self.__position, 1)
                self.ps_pos.append((self.__position[0][0], s[0]-1))
                self.ps_pos.append((self.__position[0][0], s[1]+1))
            else:
                s = self.minmax_value(self.__position, 0)
                self.ps_pos.append((s[0] - 1, self.__position[0][1]))
                self.ps_pos.append((s[1] + 1 , self.__position[0][1]))
        else:
            self.ps_pos.append((self.__position[0][0], self.__position[0][1] + 1))
            self.ps_pos.append((self.__position[0][0], self.__position[0][1] - 1))
            self.ps_pos.append((self.__position[0][0] + 1, self.__position[0][1]))
            self.ps_pos.append((self.__position[0][0] - 1, self.__position[0][1]))

        for _ in self.ps_pos:
            if _ not in field:
                self.ps_pos.remove(_)

        return self.ps_pos


    @classmethod
    def minmax_value(cls, pos, ind):
        l = [i[ind] for i in pos]
        return (min(l), max(l))


class UserFleet(Field):
    """'Корабль 1': 3,
                        'Корабль 2': 2,
                        'Корабль 3': 2,
                        'Корабль 4': 1,"""
    def __init__(self, field_size):
        super().__init__(field_size)
        self.armada = {'Корабль 5': 3,
                        'Корабль 6': 1}
        for ships, sizes in self.armada.items():
            self.armada[ships] = Ship(ships, sizes)
    #
    # def set_fleetposition(self, user):
    #     for names, ships in self.armada.items():
    #         ships.position = user
    #         # print(ships.position)



class GameRun:
    def __init__(self, field_size, user1, user2):
        self.user1 = GameUser(user1)
        self.user2 = GameUser(user2)
        self.fleet1 = UserFleet(field_size)
        self.fleet2 = UserFleet(field_size)
        self.user1_coords = [(i, j) for j in range(1, field_size + 1) for i in range(1, field_size + 1)]
        self.user2_coords = [(i, j) for j in range(1, field_size + 1) for i in range(1, field_size + 1)]


    def gameprocess(self):
        self.fleet1.show_chess()
        for name, ships in self.fleet1.armada.items():
            possible_aims = self.user1_coords
            for point in range(ships.ship_size):
                if len(possible_aims) > 1:
                    msg = f'Введи через пробел номер стоки и колонки для координаты {point + 1} из {ships.ship_size} {name}:\n'
                    if point > 0:
                        msg += f'-список возм-х координат: {possible_aims}\n'
                    coords = self.user1.coordsinput(possible_aims, msg)
                else:
                    coords = possible_aims[0]
                    print(f'Координата {point + 1} из {ships.ship_size} {name} присвоена {coords}')
                ships.position = coords
                self.fleet1.draw_myfield(coords)
                self.user1_coords.remove(coords)
                self.fleet1.show_chess()
                if point == ships.ship_size - 1:
                    cl_pos = ships.close_positions(self.user1_coords)
                    for _ in cl_pos:
                        self.user1_coords.remove(_)
                else:
                    possible_aims = ships.possible_pos(self.user1_coords)



if __name__ == "__main__":
    run = GameRun(6, 'USER 1', 'PC')
    run.gameprocess()
