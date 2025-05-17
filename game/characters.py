# game/characters.py
"""
Define las clases base y concretas para los personajes del juego.
"""
from abc import ABC, abstractmethod
from game.items import Weapon, Armor
from game.strategies import CombatStrategy, AggressiveStrategy, SpellCastingStrategy # Importaciones combinadas

class Character(ABC):
    def __init__(self, name: str, weapon: Weapon, armor: Armor, strategy: CombatStrategy):
        self.name = name
        self.base_health = 100 # Salud base antes de modificadores de clase
        self.health = self.base_health
        self.weapon = weapon
        self.armor = armor
        self.combat_strategy: CombatStrategy = strategy # La estrategia se asigna directamente

    @abstractmethod
    def special_ability(self) -> str: # Podría retornar una descripción o ejecutar una lógica.
        pass

    def set_combat_strategy(self, strategy: CombatStrategy):
        self.combat_strategy = strategy
        # No imprimimos desde aquí, el comando que lo llama puede hacerlo.
        # print(f"{self.name} ha cambiado su estrategia de combate a: {strategy.__class__.__name__}")

    def perform_combat_action(self, target: 'Character') -> str:
        if self.health <= 0:
            return f"{self.name} está derrotado y no puede actuar."
        if self.combat_strategy:
            return self.combat_strategy.execute_action(self, target)
        return f"{self.name} no sabe cómo actuar en combate (sin estrategia)."

    def take_damage(self, amount: int):
        # Podríamos considerar la armadura aquí para reducir el daño
        actual_damage_taken = amount - self.armor.defense_bonus() # Ejemplo simple
        if actual_damage_taken < 0:
            actual_damage_taken = 0
        
        self.health -= actual_damage_taken
        if self.health < 0:
            self.health = 0
        # No imprimimos desde aquí, la estrategia o el bucle de juego lo harán.

    def describe(self) -> str: # Método describe ahora retorna un string
        description_lines = [
            f"--- {self.name} ({self.__class__.__name__}) ---",
            f"Salud: {self.health}/{self.base_health}",
            f"Arma: {self.weapon.get_name()} - {self.weapon.get_description()} (Bono Ataque: {self.weapon.attack_bonus()})",
            f"Armadura: {self.armor.get_name()} - {self.armor.get_description()} (Bono Defensa: {self.armor.defense_bonus()})",
        ]
        if hasattr(self, 'mana'):
            description_lines.append(f"Maná: {self.mana}") # Asumimos que 'mana' es un atributo en Mage
        if hasattr(self, 'stealth_points'):
            description_lines.append(f"Puntos de Sigilo: {self.stealth_points}")

        description_lines.append(f"Habilidad Especial: {self.special_ability()}")
        description_lines.append(f"Estrategia de Combate: {self.combat_strategy.__class__.__name__}")
        description_lines.append("--------------------")
        return "\n".join(description_lines)

class Warrior(Character):
    def __init__(self, name: str, weapon: Weapon, armor: Armor, strategy: CombatStrategy = None):
        actual_strategy = strategy if strategy is not None else AggressiveStrategy()
        super().__init__(name, weapon, armor, actual_strategy)
        self.base_health += 20 # Los guerreros tienen más vida base
        self.health = self.base_health # Actualizar salud actual

    def special_ability(self) -> str:
        return "Furia Guerrera: ¡Aumenta el daño en el próximo golpe!"

class Mage(Character):
    def __init__(self, name: str, weapon: Weapon, armor: Armor, strategy: CombatStrategy = None):
        actual_strategy = strategy if strategy is not None else SpellCastingStrategy()
        super().__init__(name, weapon, armor, actual_strategy)
        self.mana = 100 # Los magos tienen maná

    def special_ability(self) -> str:
        return "Bola de Fuego: ¡Lanza una bola de fuego al enemigo!"

class Rogue(Character):
    def __init__(self, name: str, weapon: Weapon, armor: Armor, strategy: CombatStrategy = None):
        actual_strategy = strategy if strategy is not None else AggressiveStrategy()
        super().__init__(name, weapon, armor, actual_strategy)
        self.stealth_points = 50 # Los pícaros tienen puntos de sigilo

    def special_ability(self) -> str:
        return "Ataque Furtivo: ¡Si no te detectan, el daño es mayor!"