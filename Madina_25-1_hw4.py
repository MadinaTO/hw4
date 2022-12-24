from random import randint, choice
from enum import Enum


class SuperAbility(Enum):
    CRITICAL_DAMAGE = 1
    BOOST = 2
    HEALTH = 3
    SAVE_DAMAGE_AND_REVERT = 4
    INCREASE_OR_DECREASE = 5
    REVIVAL = 6
    GET_PET = 7

    """CRITICAL_DAMAGE - крит. удар"""
    """BOOST -  увеличивает атаку"""
    """HEALTH - лечит """
    """SAVE_DAMAGE_AND_REVERT - сохраняет урон и возвращает """
    """INCREASE_OR_DECREASE = уменьшение или увеличение"""
    """REVIVAL = возрождение"""
    """GET_PET = вызов фамильяра"""


class GameEntity:

    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.__health} damage: {self.__damage}'


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None

    """defence - защита"""

    @property
    def defence(self):
        return self.__defence

    def choose_defence(self, heroes):
        hero = choice(heroes)
        if hero.health <= 0:
            self.choose_defence(heroes)
        else:
            self.__defence = hero.super_ability

    """hit - наносимый урон"""

    def hit(self, heroes):
        for hero in heroes:
            if hero.health > 0:
                hero.health = hero.health - self.damage

    def __str__(self):
        return f'BOSS ' + super(Boss, self).__str__() + f' defence: {self.__defence}'


class Hero(GameEntity):
    def __init__(self, name, health, damage, super_ability):
        super().__init__(name, health, damage)
        if not isinstance(super_ability, SuperAbility):
            raise ValueError('Ability must be of type SuperAbility')
        else:
            self.__super_ability = super_ability

    def hit(self, boss):
        boss.health = boss.health - self.damage

    @property
    def super_ability(self):
        return self.__super_ability

    """apply_super_power - примените суперсилу"""

    def apply_super_power(self, boss, heroes):
        pass


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.CRITICAL_DAMAGE)

    """randint - возвращает случайное число в промежутке между значениями (min, max)"""

    def apply_super_power(self, boss, heroes):
        coefficient = randint(2, 5)
        boss.health = boss.health - self.damage * coefficient
        print(f'Warrior hits critically: {self.damage * coefficient}')


class Magic(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.BOOST)

    def apply_super_power(self, boss, heroes):
        boost = randint(5, 16)
        for hero in heroes:
            if hero.health > 0:
                hero.damage += boost
        print(f'Mag boost: {boost}')


class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, SuperAbility.HEALTH)
        self.__heal_points = heal_points

    @property
    def heal_points(self):
        return self.__heal_points

    @heal_points.setter
    def heal_points(self, value):
        self.__heal_points = value

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health > 0 and self != hero:
                hero.health = hero.health + self.__heal_points


"""смотреть отсюда и исправть ошибку, склф.дмг = 0"""


class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.SAVE_DAMAGE_AND_REVERT)
        self.__saved_damaged = 0

    def apply_super_power(self, boss, heroes):
        self.__saved_damaged = boss.damage * 0.1
        self.health += self.__saved_damaged
        self.damage += self.__saved_damaged
        print(f'Berserk damage: {self.damage}')


class Witch(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.REVIVAL)

    def apply_super_power(self, boss, heroes):
        self.damage = 0
        for hero in heroes:
            if hero.health == 0 and self != hero:
                hero.health = self.health
                self.health = 0
                print(f'The witch character sacrificed himself')


class Druid(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.GET_PET)
    '''8. Druid, который имеет способность рандомно призывать помощника ангела героям или
    же ворона боссу на 1 раунд за всю игру. "Ангел" увеличивает способность медика лечить героев на n кол-во
    А ворон прибавляет агрессию (увеличивается урон на 50%), боссу если его жизнь менее 50%.¬'''

    def apply_super_power(self, boss, heroes):
        pet = choice(['angel', 'raven'])
        if pet == 'angel':
            boost = randint(5, 15)
            for hero in heroes:
                hero.health += boost
            print(f'The druid summoned an angel for the heroes {boost}')
        elif pet == 'raven':
            if boss.health <= boss.health / 2:
                boss.damage += boss.damage / 2
                print(f'The druid summoned a raven for the boss')


class AntMan(Hero):
    def __init__(self, name, health, damage):
        super(AntMan, self).__init__(name, health, damage, SuperAbility.INCREASE_OR_DECREASE)
        self.flag = 0
        self.f = 0

    def apply_super_power(self, boss, heroes):
        size = randint(1, 3)
        if self.flag == 1:
            self.health -= self.f
            self.damage -= self.f
        elif self.flag == 2:
            self.health += self.f
            self.damage += self.f

        N = randint(2, 6)
        self.f = N
        if size == 1:
            print(f"Ant_man: + {N}")
            self.health += N
            self.damage += N
            self.flag = 1
        else:
            print(f"Ant_man: - {N}")
            self.health -= N
            self.damage -= N
            self.flag = 2


round_counter = 0

"""print statistics - ф-я для выявления всех персонажей"""


def print_statistics(boss, heroes):
    print('ROUND ' + str(round_counter) + ' --------------')
    print(boss)
    for hero in heroes:
        print(hero)


"""is game finished - по какой логике закончится игра"""


def is_game_finished(boss, heroes):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
    return all_heroes_dead


"""play round - начало нового раунда """


def play_round(boss, heroes):
    global round_counter
    round_counter += 1
    boss.choose_defence(heroes)
    boss.hit(heroes)
    for hero in heroes:
        if boss.defence != hero.super_ability and hero.health > 0 and boss.health > 0:
            hero.hit(boss)
            hero.apply_super_power(boss, heroes)

    print_statistics(boss, heroes)


"""start_game - начало игры (задаем объекты героев)"""


def start_game():
    boss = Boss('Boss', 2500, 50)
    warrior = Warrior('Warrior', 280, 10)
    doc = Medic('Doc', 250, 5, 15)
    berserk = Berserk('Berserk', 260, 15)
    magic = Magic('Mag', 270, 20)
    assistant = Medic('Assis', 290, 5, 5)
    witch = Witch('Witch', 400, 0)
    druid = Druid('Druid', 280, 15)
    antman = AntMan('AntMan', 200, 20)

    heroes = [warrior, berserk, doc, magic, assistant, witch, druid, antman]

    print_statistics(boss, heroes)

    while not is_game_finished(boss, heroes):
        play_round(boss, heroes)


start_game()
