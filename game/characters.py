# game/characters.py
from abc import ABC, abstractmethod
from game.items import Weapon, Armor # Importamos nuestras definiciones de items
from game.strategies import CombatStrategy, AggressiveStrategy # Importamos la estrategia base y una por defecto
from game.strategies import SpellCastingStrategy # Importamos la estrategia de lanzamiento de hechizos
class Character(ABC):
    def __init__(self, name: str, weapon: Weapon, armor: Armor, strategy: CombatStrategy = None): # Añadido strategy
        self.name = name
        self.health = 100 # Vida base
        self.weapon = weapon
        self.armor = armor
        # Asignamos una estrategia por defecto si no se proporciona una
        self.combat_strategy = strategy if strategy else AggressiveStrategy()

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

    def set_combat_strategy(self, strategy: CombatStrategy):
        self.combat_strategy = strategy
        print(f"{self.name} ha cambiado su estrategia de combate a: {strategy.__class__.__name__}")

    def perform_combat_action(self, target: 'Character') -> str:
        if self.combat_strategy:
            return self.combat_strategy.execute_action(self, target)
        return f"{self.name} no sabe cómo actuar en combate (sin estrategia)."

    def describe(self):
        print(f"--- {self.name} ({self.__class__.__name__}) ---") # Añadido el nombre de la clase
        print(f"Salud: {self.health}")
        print(f"Arma: {self.weapon.get_name()} - {self.weapon.get_description()} (Bono Ataque: {self.weapon.attack_bonus()})")
        print(f"Armadura: {self.armor.get_name()} - {self.armor.get_description()} (Bono Defensa: {self.armor.defense_bonus()})")
        if hasattr(self, 'mana'): # Si es un Mago u otra clase con mana
             print(f"Maná: {self.mana}")
        if hasattr(self, 'stealth_points'): # Si es un Pícaro u otra clase con sigilo
             print(f"Puntos de Sigilo: {self.stealth_points}")
        print(f"Habilidad Especial: {self.special_ability()}")
        print(f"Estrategia de Combate: {self.combat_strategy.__class__.__name__}") # Mostramos la estrategia actual
        print("--------------------")


# --- Productos Concretos: Personajes ---
# Modificamos los constructores para aceptar una estrategia opcional.
# Si no se pasa, Character usará AggressiveStrategy por defecto.

class Warrior(Character):
    def __init__(self, name: str, weapon: Weapon, armor: Armor, strategy: CombatStrategy = None):
        super().__init__(name, weapon, armor, strategy if strategy else AggressiveStrategy()) # Puede tener su propia estrategia por defecto
        self.health += 20

    def special_ability(self) -> str:
        return "Furia Guerrera: ¡Aumenta el daño en el próximo golpe!"

class Mage(Character):
    def __init__(self, name: str, weapon: Weapon, armor: Armor, strategy: CombatStrategy = None):
        super().__init__(name, weapon, armor, strategy if strategy else SpellCastingStrategy()) # Mago por defecto usa SpellCasting
        self.mana = 100

    def special_ability(self) -> str:
        return "Bola de Fuego: ¡Lanza una bola de fuego al enemigo!"

    # describe() ya no es necesario sobreescribirlo aquí si la clase base maneja el maná

class Rogue(Character):
    def __init__(self, name: str, weapon: Weapon, armor: Armor, strategy: CombatStrategy = None):
        super().__init__(name, weapon, armor, strategy if strategy else AggressiveStrategy()) # Pícaro puede ser agresivo por defecto
        self.stealth_points = 50

    def special_ability(self) -> str:
        return "Ataque Furtivo: ¡Si no te detectan, el daño es mayor!"