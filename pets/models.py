import random
from dataclasses import dataclass

@dataclass
class AnimalState:
    hunger: int = random.randint(40, 100)
    bored: int = random.randint(40, 100)
    clean: int = random.randint(40, 100)
    energy: int = random.randint(40, 100)

    def clamp(self):
        self.hunger      = max(0, min(100, self.hunger))
        self.bored     = max(0, min(100, self.bored))
        self.clean = max(0, min(100, self.clean))
        self.energy      = max(0, min(100, self.energy))


class Animal:
    def __init__(self, name: str, icon_filename: str):
        self.name          = name
        self.icon_filename = icon_filename
        self.state         = AnimalState()

    def feed(self, amount: int):
        raise NotImplementedError

    def play(self, duration: int):
        raise NotImplementedError


class Dog(Animal):
    def __init__(self, name: str):
        super().__init__(name, 'dog.png')
    def feed(self, amount: int):
        self.state.hunger -= int(amount * 1.2)
        self.state.clamp()
    def play(self, duration: int):
        self.state.bored -= duration * 2
        self.state.clamp()


class Cat(Animal):
    def __init__(self, name: str):
        super().__init__(name, 'cat.png')
    def feed(self, amount: int):
        self.state.hunger -= int(amount * 1.0)
        self.state.clamp()
    def play(self, duration: int):
        self.state.bored -= duration * 1
        self.state.clamp()


class Rabbit(Animal):
    def __init__(self, name: str):
        super().__init__(name, 'rabbit.png')
    def feed(self, amount: int):
        self.state.hunger -= int(amount * 0.8)
        self.state.clamp()
    def play(self, duration: int):
        self.state.bored -= int(duration * 1.5)
        self.state.clamp()


class Hamster(Animal):
    def __init__(self, name: str):
        super().__init__(name, 'hamster.png')
    def feed(self, amount: int):
        self.state.hunger -= int(amount * 0.5)
        self.state.clamp()
    def play(self, duration: int):
        self.state.bored -= duration * 3
        self.state.clamp()
