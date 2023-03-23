from random import randint

class GameUser:

    def __init__(self, userid='PC'):
        self.userid = userid
        self.score = 0

    def coordsinput(self, aims, message):
        if self.userid == 'PC':
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



class BattleField(GameUser):
    def __init__(self, field_size, armada_params, userid):
        super().__init__(userid)

        self.field_size = field_size
        self.my_field = [["o" for _ in range(self.field_size)] for _ in range(self.field_size)]
        self.enemy_field = [["o" for _ in range(self.field_size)] for _ in range(self.field_size)]

        self.selfcoords = [(i, j) for j in range(1, field_size + 1) for i in range(1, field_size + 1)]
        self.enemycoords = [(i, j) for j in range(1, field_size + 1) for i in range(1, field_size + 1)]

        self.armada = {}
        for ships, sizes in armada_params.items():
            self.armada[ships] = Ship(ships, sizes)

    def draw_myfield(self, point, status='■'):
        self.my_field[point[0]-1][point[1]-1] = status

    def draw_enemyfield(self, point, status='T'):
        self.enemy_field[point[0]-1][point[1]-1] = status

    def checkcoord(self, point):
        if self.my_field[point[0]-1][point[1]-1] == '■':
            self.draw_myfield(point, 'x')
            print(f'{self.userid}: Попадание по кораблю!')
            return True
        else:
            print(f'{self.userid}: Огонь мимо цели...')
            self.draw_myfield(point, 'T')
            return False

    def show_chess(self, status=True):
        # демонстрация поля вместе с осями координат
        if self.userid == 'PC' and status:
            pass
        else:
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
    def __init__(self, name, size):
        self.name = name
        self.size = size
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
        temp_pos = []

        if len(self.__position) > 1:
            if self.__position[0][0] == self.__position[1][0]:
                s = self.minmax_value(self.__position, 1)
                temp_pos.append((self.__position[0][0], s[0] - 1))
                temp_pos.append((self.__position[0][0], s[1] + 1))
            else:
                s = self.minmax_value(self.__position, 0)
                temp_pos.append((s[0] - 1, self.__position[0][1]))
                temp_pos.append((s[1] + 1 , self.__position[0][1]))
        else:
            temp_pos.append((self.__position[0][0], self.__position[0][1] + 1))
            temp_pos.append((self.__position[0][0], self.__position[0][1] - 1))
            temp_pos.append((self.__position[0][0] + 1, self.__position[0][1]))
            temp_pos.append((self.__position[0][0] - 1, self.__position[0][1]))

        self.final_pos = []
        for _ in temp_pos:
            if _ in field:
                self.final_pos.append(_)
        return self.final_pos

    @classmethod
    def minmax_value(cls, pos, ind):
        l = [i[ind] for i in pos]
        return (min(l), max(l))


class GameRun:
    def __init__(self, field_size, armada_params, users):
        self.userfleets = (BattleField(field_size, armada_params, users[0]), BattleField(field_size, armada_params, users[1]))
        self.maxscore = 0
        for sizes in armada_params.values():
            self.maxscore += sizes


    def gameprocess(self):
        #построение кораблей на пользовательском поле (определение координат)
        for fleet in self.userfleets:
            self.setfleet(fleet)
        # #поочередно стреляем для уничтожения флота противника
        while True:
            self.shipsfire(self.userfleets[0], self.userfleets[1])
            self.checkscore(self.userfleets[0])
            self.shipsfire(self.userfleets[1], self.userfleets[0])
            self.checkscore(self.userfleets[1])

    def checkscore(self, fleet):
        if fleet.score == self.maxscore:
            print(f'ПОБЕДА ЗА {fleet.userid}!!!')
            exit(0)

    @classmethod
    def shipsfire(cls, myfleet, enemyfleet):
        possible_aims = myfleet.enemycoords
        if len(possible_aims) != myfleet.field_size ** 2:
            myfleet.show_chess()
        coords = myfleet.coordsinput(possible_aims, 'Введите координаты через пробел для поражения корабля противника:\n')
        if enemyfleet.checkcoord(coords):
            myfleet.score += 1
            myfleet.draw_enemyfield(coords, 'x')
        else:
            myfleet.draw_enemyfield(coords, 'T')
        myfleet.enemycoords.remove(coords)


    @classmethod
    def setfleet(cls, fleet):
        fleet.show_chess()
        for name, ships in fleet.armada.items():
            possible_aims = fleet.selfcoords
            for ship_point in range(ships.size):
                if len(possible_aims) > 1:
                    msg = f'Введи через пробел номер стоки и колонки для координаты {ship_point + 1} из {ships.size} {name}:\n'
                    if ship_point > 0:
                        msg += f'-список возм-х координат: {possible_aims}\n'
                    # делаем запрос для определения координат (выбор из возможных координат)
                    coords = fleet.coordsinput(possible_aims, msg)
                else:
                    # а смысл запрашивать, если вариант только 1, поэтому присваеваем сразу
                    coords = possible_aims[0]
                    if fleet.userid != 'PC':
                        print(f'Координата {ship_point + 1} из {ships.size} {name} присвоена {coords}')
                ships.position = coords
                fleet.draw_myfield(coords)
                fleet.selfcoords.remove(coords)
                fleet.show_chess()
                # когда координаты корабля уже заданы убираем свободные координаты по периметру вокруг корабля
                if ship_point == ships.size - 1:
                    cl_pos = ships.close_positions(fleet.selfcoords)
                    for _ in cl_pos:
                        fleet.selfcoords.remove(_)
                else:
                    possible_aims = ships.possible_pos(fleet.selfcoords)
        # fleet.show_chess(False)  # для просмотра поля PC-юзера




if __name__ == "__main__":
    # armada_ships = {'Корабль 1': 3, 'Корабль 2': 2, 'Корабль 3': 2, 'Корабль 4': 1,'Корабль 5': 3, 'Корабль 6': 1, 'Корабль 7': 1}
    armada = {'Корабль 1': 3, 'Корабль 2': 2}
    users = ('USER 1', 'PC')
    run = GameRun(3, armada, users)
    run.gameprocess()
