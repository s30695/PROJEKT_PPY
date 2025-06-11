import random
from .factory import AnimalFactory

class PetController:
    def __init__(self):
        self.pet = None

    def select_pet(self, species: str, name: str):
        self.pet = AnimalFactory.create(species, name)

    def feed_pet(self, amount: int):
        self.pet.feed(amount)

    def play_pet(self, duration: int):
        self.pet.play(duration)

    def clean_pet(self):
        # mycie
        self.pet.state.clean = 100

    def sleep_pet(self, duration: int = 30):
        # spanie
        self.pet.state.energy += duration
        self.pet.state.clamp()

    def tick(self):
        s = self.pet.state
        s.hunger      -= 1
        s.bored       -= 1
        s.clean       -= 1
        s.energy      -= 1
        s.clamp()


    def get_state(self):
        return self.pet.state
