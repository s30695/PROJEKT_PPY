"""
pet_simulator — pakiet gry Symulator Zwierzaka.

Zawiera modele zwierząt, fabrykę, kontroler i GUI.
"""

__version__ = "0.1.0"

# eksportujemy najważniejsze klasy i funkcję startującą
from .models      import Animal, Dog, Cat, Rabbit, Hamster, AnimalState
from .factory     import AnimalFactory
from .controllers import PetController
from .gui         import main

__all__ = [
    "Animal", "Dog", "Cat", "Rabbit", "Hamster", "AnimalState",
    "AnimalFactory", "PetController", "main"
]
