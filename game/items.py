# game/items.py
from abc import ABC, abstractmethod

# --- Interfaces para los Productos ---

class Weapon(ABC):
    @abstractmethod
    def attack_bonus(self) -> int:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

class Armor(ABC):
    @abstractmethod
    def defense_bonus(self) -> int:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

# --- Productos Concretos: Armas ---

class Sword(Weapon):
    def attack_bonus(self) -> int:
        return 5

    def description(self) -> str:
        return "Una espada afilada y confiable."

class Staff(Weapon):
    def attack_bonus(self) -> int:
        return 3 # Menor ataque físico, quizás luego añade bonus mágico

    def description(self) -> str:
        return "Una vara de madera nudosa, canaliza energías."

class Dagger(Weapon):
    def attack_bonus(self) -> int:
        return 2

    def description(self) -> str:
        return "Una daga corta y sigilosa."

# --- Productos Concretos: Armaduras ---

class Chainmail(Armor):
    def defense_bonus(self) -> int:
        return 10

    def description(self) -> str:
        return "Una cota de mallas resistente."

class Robe(Armor):
    def defense_bonus(self) -> int:
        return 3 # Menor defensa física, quizás luego añade bonus mágico

    def description(self) -> str:
        return "Una túnica ligera, ofrece poca protección física."

class LeatherArmor(Armor):
    def defense_bonus(self) -> int:
        return 6

    def description(self) -> str:
        return "Una armadura de cuero curtido."