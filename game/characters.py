# game/characters.py
from abc import ABC, abstractmethod
from game.items import Weapon, Armor # Importamos nuestras definiciones de items

class Character(ABC):
    def __init__(self, name: str, weapon: Weapon, armor: Armor):
        self.name = name
        self.health = 100 # Vida base
        self.weapon = weapon
        self.armor = armor

    @abstractmethod
    def special_ability(self) -> str:
        pass

    def describe(self):
        print(f"--- {self.name} ---")
        print(f"Salud: {self.health}")
        # Línea CORREGIDA para el arma:
        print(f"Arma: {self.weapon.get_description()} (Bono Ataque: {self.weapon.attack_bonus()})")

        # Línea CORREGIDA para la armadura:
        print(f"Armadura: {self.armor.get_description()} (Bono Defensa: {self.armor.defense_bonus()})")

        print(f"Habilidad Especial: {self.special_ability()}")
        print("--------------------")

# --- Productos Concretos: Personajes ---

class Warrior(Character):
    def __init__(self, name: str, weapon: Weapon, armor: Armor):
        super().__init__(name, weapon, armor)
        self.health += 20 # Los guerreros tienen más vida

    def special_ability(self) -> str:
        return "Furia Guerrera: ¡Aumenta el daño en el próximo golpe!"

class Mage(Character):
    def __init__(self, name: str, weapon: Weapon, armor: Armor):
        super().__init__(name, weapon, armor)
        self.mana = 100 # Los magos tienen maná

    def special_ability(self) -> str:
        return "Bola de Fuego: ¡Lanza una bola de fuego al enemigo!"

    def describe(self): # Sobrescribimos para incluir el maná
        super().describe()
        print(f"Maná: {self.mana}")
        print("--------------------")

class Rogue(Character):
    def __init__(self, name: str, weapon: Weapon, armor: Armor):
        super().__init__(name, weapon, armor)
        self.stealth_points = 50 # Los pícaros tienen puntos de sigilo

    def special_ability(self) -> str:
        return "Ataque Furtivo: ¡Si no te detectan, el daño es mayor!"

    def describe(self): # Sobrescribimos para incluir el sigilo
        super().describe()
        print(f"Puntos de Sigilo: {self.stealth_points}")
        print("--------------------")