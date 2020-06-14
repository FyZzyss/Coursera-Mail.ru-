from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points,
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Perception": 4,  # восприятие
            "Endurance": 8,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость
            "Luck": 1  # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.name = 'Effect'
        self.point = ['HP', 'MP', 'SP']

    @abstractmethod
    def get_positive_effects(self):
        return self.base.get_positive_effects()

    @abstractmethod
    def get_negative_effects(self):
        return self.base.get_negative_effects()

    @abstractmethod
    def get_stats(self):
        return self.base.get_stats()


class AbstractPositive(AbstractEffect):

    def get_positive_effects(self):
        temp = self.base.get_positive_effects()
        temp.append(self.name)
        return temp

    def get_negative_effects(self):
        return self.base.get_negative_effects()


class Berserk(AbstractPositive):
    def __init__(self, base):
        super().__init__(base)
        self.base = base
        self.positive_stats = ['Strength', 'Agility', 'Luck', 'Endurance']
        self.negative_stats = ['Charisma', 'Intelligence', 'Perception']
        self.name = 'Berserk'

    def get_stats(self):
        temp = self.base.get_stats()
        for i in self.positive_stats:
            temp[i] += 7
        for i in self.negative_stats:
            temp[i] -= 3
        temp['HP'] += 50
        return temp


class Blessing(AbstractPositive):
    def __init__(self, base):
        super().__init__(base)
        self.base = base
        self.name = 'Blessing'

    def get_stats(self):
        temp = self.base.get_stats()
        for i in temp:
            if i not in self.point:
                temp[i] += 2
        return temp


class AbstractNegative(AbstractEffect):
    def __init__(self, base):
        super().__init__(base)
        self.base = base

    def get_positive_effects(self):
        return self.base.get_positive_effects()

    def get_negative_effects(self):
        temp = self.base.get_negative_effects()
        temp.append(self.name)
        return temp


class Weakness(AbstractNegative):
    def __init__(self, base):
        super().__init__(base)
        self.base = base
        self.name = 'Weakness'
        self.negative_stats = ['Strength', 'Agility', 'Endurance']

    def get_stats(self):
        temp = self.base.get_stats()
        for i in self.negative_stats:
            temp[i] -= 4
        return temp


class EvilEye(AbstractNegative):
    def __init__(self, base):
        super().__init__(base)
        self.base = base
        self.name = 'EvilEye'
        self.negative_stats = ['Luck']

    def get_stats(self):
        temp = self.base.get_stats()
        for i in self.negative_stats:
            temp[i] -= 10
        return temp


class Curse(AbstractNegative):
    def __init__(self, base):
        super().__init__(base)
        self.base = base
        self.name = 'Curse'

    def get_stats(self):
        temp = self.base.get_stats()
        for i in temp:
            if i not in self.point:
                temp[i] -= 2
        return temp
