from random import randint

class GameUser:

    def __init__(self, userid='PC'):
        self.userid = userid
        self.score = 0

    def coordsinput(self, aims, message):
        if self.userid == 'PC':
            #для компьютера рандомно выбираем координату из имеющихся целей
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


class Ship:
    def __init__(self, name='No name', size=1):
        self.name = name
        self.size = size
        self.__position = []

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, coords):
        self.__position.append(coords)

    def resetposition(self):
        self.__position.clear()


class BattleField(GameUser):
    def __init__(self, field_size, armada_params, userid):
        super().__init__(userid)
        self.field_size = field_size
        self.my_field = [["o" for _ in range(field_size)] for _ in range(field_size)]
        self.enemy_field = [["o" for _ in range(field_size)] for _ in range(field_size)]
        self.fieldcoords = [(i, j) for j in range(1, field_size + 1) for i in range(1, field_size + 1)]
        self.armada = {}
        for ships, sizes in armada_params.items():
            self.armada[ships] = Ship(ships, sizes)
        self.enemyship = []
        self.aims = []

    def renew_fieldcoords(self):
        self.fieldcoords = [(i, j) for j in range(1, self.field_size + 1) for i in range(1, self.field_size + 1)]

    def resetfleetsettings(self):
        self.fieldcoords = [(i, j) for j in range(1, self.field_size + 1) for i in range(1, self.field_size + 1)]
        self.my_field = [["o" for _ in range(self.field_size)] for _ in range(self.field_size)]
        for ships in self.armada.values():
            ships.resetposition()

    def draw_myfield(self, point, status='■'):
        self.my_field[point[0]-1][point[1]-1] = status

    def draw_enemyfield(self, point, status='T'):
        self.enemy_field[point[0]-1][point[1]-1] = status

    def markenemyship(self, point, status):
        """составляем список кораблей противника с их позициями
        для определения возможных координат для следующего выстрела"""
        if len(self.enemyship) == 0 or self.enemyship[-1].status == 'Убил':
            self.enemyship.append(Ship())
            self.enemyship[-1].status = status
        self.enemyship[-1].position = point
        if status == 'Попадание':
            self.aims = self.possible_pos(self.enemyship[-1].position)
        elif status == 'Убил':
            self.enemyship[-1].status = status
            self.aims = self.close_positions(self.enemyship[-1].position)
            for _ in self.aims:
                if _ in self.fieldcoords:
                    self.fieldcoords.remove(_)
            self.aims = self.fieldcoords

    def checkcoord(self, point):
        """проверка выстрела противника на попадание в цель"""
        if self.my_field[point[0]-1][point[1]-1] == '■':
            self.draw_myfield(point, 'x')
            print(f'{self.userid}: Попадание по кораблю!')
            for ships in self.armada.values():
                if point in ships.position:
                    ships.position.remove(point)
                    if len(ships.position) == 0:
                        print(f'{self.userid}: Убил!')
                        return 'Убил'
                    else:
                        return 'Попадание'
        else:
            print(f'{self.userid}: Мимо цели...')
            self.draw_myfield(point, 'T')
            return 'Мимо'

    def close_positions(self, positionpoints):
        """определяем координаты по периметру позиции корабля"""
        self.closepoints = []
        for point in positionpoints:
            p = lambda i, j: (point[0] + i, point[1] + j)
            temppoints = [p(i, j) for i in range(-1, 2) for j in range(-1, 2)]
            for tpoint in temppoints:
                if tpoint in self.fieldcoords and tpoint not in self.closepoints:
                    self.closepoints.append(tpoint)
        return self.closepoints

    def possible_pos(self, positionpoints):
        """определяем возможные цели координат исходя из заданной позиции и текущего поля"""
        temp_points = []
        if len(positionpoints) > 1:
            if positionpoints[0][0] == positionpoints[1][0]:
                minmax = self.minmax_value(positionpoints, 1)
                temp_points.append((positionpoints[0][0], minmax[0] - 1))
                temp_points.append((positionpoints[0][0], minmax[1] + 1))
            else:
                minmax = self.minmax_value(positionpoints, 0)
                temp_points.append((minmax[0] - 1, positionpoints[0][1]))
                temp_points.append((minmax[1] + 1, positionpoints[0][1]))
        else:
            temp_points.append((positionpoints[0][0], positionpoints[0][1] + 1))
            temp_points.append((positionpoints[0][0], positionpoints[0][1] - 1))
            temp_points.append((positionpoints[0][0] + 1, positionpoints[0][1]))
            temp_points.append((positionpoints[0][0] - 1, positionpoints[0][1]))

        self.final_points = []
        for _ in temp_points:
            if _ in self.fieldcoords:
                self.final_points.append(_)
        return self.final_points

    @classmethod
    def minmax_value(cls, pos, ind):
        """Вспомогательный метод для метода possible_pos"""
        l = [i[ind] for i in pos]
        return (min(l), max(l))

    def show_chess(self, status=True):
       """вывод поля играка и противника с осями координат"""
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


class GameRun:
    def __init__(self, field_size, armada_params, users):
        self.userfleets = (BattleField(field_size, armada_params, users[0]), BattleField(field_size, armada_params, users[1]))
        self.maxscore = 0
        for sizes in armada_params.values():
            self.maxscore += sizes


    def gameprocess(self):
        # Фаза 1: построение кораблей на пользовательском поле
        for fleet in self.userfleets:
            while True:
                if self.setfleet(fleet):
                    break
                else:
                    if fleet.userid != 'PC':
                        print('Все корабли на поле не поместились, необходимо разместить корабли заново')
                    fleet.resetfleetsettings()

        #подготовка к следующей фазе игры: заново генерируем целевой список координат
        for fleet in self.userfleets:
            fleet.renew_fieldcoords()

        # Фаза 2: поочередно стреляем для уничтожения флота противника
        while True:
            self.shipsfire(self.userfleets[0], self.userfleets[1])
            self.checkscore(self.userfleets[0])
            self.shipsfire(self.userfleets[1], self.userfleets[0])
            self.checkscore(self.userfleets[1])

    def checkscore(self, fleet):
        if fleet.score == self.maxscore:
            fleet.show_chess(False)
            print(f'ПОБЕДА ЗА {fleet.userid}!!!')
            exit(0)

    @classmethod
    def shipsfire(cls, myfleet, enemyfleet):
        if len(myfleet.aims) == 0:
            myfleet.aims = myfleet.fieldcoords
        if len(myfleet.aims) != myfleet.field_size ** 2:
            myfleet.show_chess()
        coords = myfleet.coordsinput(myfleet.aims, 'Введите координаты через пробел для поражения корабля противника:\n')
        myfleet.fieldcoords.remove(coords)
        if myfleet.aims is not myfleet.fieldcoords:
            myfleet.aims.remove(coords)
        fireresult = enemyfleet.checkcoord(coords)
        if fireresult == 'Попадание' or fireresult == 'Убил':
            myfleet.score += 1
            myfleet.draw_enemyfield(coords, 'x')
            if myfleet.userid == 'PC':
                myfleet.markenemyship(coords, fireresult)
        elif fireresult == 'Мимо':
            myfleet.draw_enemyfield(coords, 'T')

    @classmethod
    def setfleet(cls, fleet):
        fleet.show_chess()
        for name, ships in fleet.armada.items():
            possible_aims = fleet.fieldcoords
            for ship_point in range(ships.size):
                if len(possible_aims) > 1:
                    msg = f'Введи через пробел номер стоки и колонки для координаты {ship_point + 1} из {ships.size} {name}:\n'
                    if ship_point > 0:
                        msg += f'-список возм-х координат: {possible_aims}\n'
                    # делаем запрос для определения координат (выбор из возможных координат)
                    coords = fleet.coordsinput(possible_aims, msg)
                #для случая, когда корабль не вмещается
                elif len(possible_aims) == 0:
                    return False
                else:
                    # а смысл запрашивать, если вариант только 1, поэтому присваеваем сразу
                    coords = possible_aims[0]
                    if fleet.userid != 'PC':
                        print(f'Координата {ship_point + 1} из {ships.size} {name} присвоена {coords}')
                ships.position = coords
                fleet.draw_myfield(coords)
                fleet.fieldcoords.remove(coords)
                fleet.show_chess()
                # когда координаты корабля уже заданы убираем свободные координаты по периметру вокруг корабля
                if ship_point == ships.size - 1:
                    close_points = fleet.close_positions(ships.position)
                    for _ in close_points:
                        fleet.fieldcoords.remove(_)
                else:
                    possible_aims = fleet.possible_pos(ships.position)
        return True
        #fleet.show_chess(False)  # для просмотра поля PC-юзера


if __name__ == "__main__":
    armada = {'Корабль 1': 3, 'Корабль 2': 2, 'Корабль 3': 2, 'Корабль 4': 1,'Корабль 5': 1, 'Корабль 6': 1, 'Корабль 7': 1}
    users = ('USER1', 'PC')
    run = GameRun(6, armada, users)
    run.gameprocess()
