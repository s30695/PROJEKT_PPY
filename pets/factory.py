from .models import Dog, Cat, Rabbit, Hamster

class AnimalFactory:
    _map = {
        "Pies":   Dog,
        "Kot":    Cat,
        "Królik": Rabbit,
        "Chomik": Hamster,
    }

    @classmethod
    def create(cls, species: str, name: str):
        if species not in cls._map:
            raise ValueError(f"Nieznany gatunek: {species}")
        return cls._map[species](name)
