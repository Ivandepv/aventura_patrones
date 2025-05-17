# game/characters.py
"""
Define las clases base y concretas para los personajes del juego,
incluyendo mecánicas de salud, daño y habilidades especiales.
"""
from abc import ABC, abstractmethod
from typing import Optional # Para strategy opcional en __init__

from game.items import Weapon, Armor
from game.strategies import CombatStrategy, AggressiveStrategy, SpellCastingStrategy
from game.constants import (
    BASE_PLAYER_HEALTH,
    BASE_WARRIOR_HEALTH_BONUS,
    BASE_MAGE_MANA,
    WARRIOR_FURIA_TURNS,
    WARRIOR_FURIA_BONUS_DAMAGE,
    BASE_ROGUE_STEALTH_POINTS,
)

class Character(ABC):
    def __init__(self,
                 name: str,
                 weapon: Weapon,
                 armor: Armor,
                 strategy: CombatStrategy, # Estrategia ahora es requerida por defecto
                 max_health: int = BASE_PLAYER_HEALTH):
        self.name = name
        self.max_health = max_health
        self.health = self.max_health
        self.weapon = weapon
        self.armor = armor
        self.combat_strategy: CombatStrategy = strategy
        self.is_furious: bool = False # Para la Furia del Guerrero
        self.furia_turns_left: int = 0

    def is_alive(self) -> bool:
        return self.health > 0

    @abstractmethod
    def special_ability_name(self) -> str:
        pass

    @abstractmethod
    def use_special_ability(self, target: Optional['Character']) -> str:
        """Ejecuta la habilidad especial. Retorna una descripción de la acción."""
        pass

    def set_combat_strategy(self, strategy: CombatStrategy):
        self.combat_strategy = strategy
        # La retroalimentación al usuario la dará el comando o el bucle del juego

    def perform_combat_action(self, target: 'Character') -> str:
        if not self.is_alive():
            return f"{self.name} está derrotado y no puede actuar."
        if self.combat_strategy:
            return self.combat_strategy.execute_action(self, target)
        return f"{self.name} no sabe cómo actuar en combate (sin estrategia asignada)."

    def take_damage(self, amount: int) -> str:
        if not self.is_alive():
            return f"{self.name} ya está derrotado."

        # La armadura reduce el daño, pero no puede hacer que el daño sea negativo
        damage_reduction = self.armor.defense_bonus()
        actual_damage_taken = max(0, amount - damage_reduction)

        self.health -= actual_damage_taken
        if self.health < 0:
            self.health = 0

        feedback = f"{self.name} recibe {actual_damage_taken} de daño (absorbido {damage_reduction} por armadura)."
        if not self.is_alive():
            feedback += f" ¡{self.name} ha sido derrotado!"
        else:
            feedback += f" Salud restante: {self.health}/{self.max_health}."
        return feedback

    def heal(self, amount: int) -> str:
        if not self.is_alive():
            return f"{self.name} está derrotado y no puede ser curado."
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        return f"{self.name} se cura {amount} puntos de salud. Salud actual: {self.health}/{self.max_health}."

    def get_attack_power(self) -> int:
        """Calcula el poder de ataque total, incluyendo bonus temporales."""
        bonus = 0
        if self.is_furious and self.furia_turns_left > 0:
            bonus += WARRIOR_FURIA_BONUS_DAMAGE
        return self.weapon.attack_bonus() + bonus

    def tick_effects(self):
        """Llamado al final del turno del personaje para actualizar efectos temporales."""
        if self.is_furious:
            self.furia_turns_left -= 1
            if self.furia_turns_left <= 0:
                self.is_furious = False
                # print(f"{self.name} ya no está furioso.") # El juego principal puede manejar este mensaje

    def describe(self) -> str:
        status_lines = [
            f"--- {self.name} ({self.__class__.__name__}) ---",
            f"Salud: {self.health}/{self.max_health} {'(Derrotado)' if not self.is_alive() else ''}",
            f"Arma: {self.weapon.get_name()} (Daño base: {self.weapon.attack_bonus()})",
            f"Armadura: {self.armor.get_name()} (Defensa: {self.armor.defense_bonus()})",
        ]
        if self.is_furious and self.furia_turns_left > 0:
            status_lines.append(f"Estado: ¡Furioso! (+{WARRIOR_FURIA_BONUS_DAMAGE} daño, {self.furia_turns_left} turnos restantes)")

        if hasattr(self, 'mana'):
            status_lines.append(f"Maná: {self.mana}/{getattr(self, 'max_mana', self.mana)}")
        if hasattr(self, 'stealth_points'): # Aún no usado mecánicamente
            status_lines.append(f"Puntos de Sigilo: {self.stealth_points}")

        status_lines.append(f"Habilidad Especial: {self.special_ability_name()}")
        status_lines.append(f"Estrategia de Combate: {self.combat_strategy.__class__.__name__}")
        status_lines.append("--------------------")
        return "\n".join(status_lines)


class Warrior(Character):
    def __init__(self, name: str, weapon: Weapon, armor: Armor, strategy: Optional[CombatStrategy] = None):
        actual_strategy = strategy if strategy is not None else AggressiveStrategy()
        super().__init__(name, weapon, armor, actual_strategy, max_health=BASE_PLAYER_HEALTH + BASE_WARRIOR_HEALTH_BONUS)

    def special_ability_name(self) -> str:
        return "Furia Guerrera"

    def use_special_ability(self, target: Optional['Character']) -> str:
        if not self.is_furious:
            self.is_furious = True
            self.furia_turns_left = WARRIOR_FURIA_TURNS
            return f"¡{self.name} entra en {self.special_ability_name()}! Su daño aumenta por {self.furia_turns_left} turnos."
        else:
            return f"{self.name} ya está furioso."

class Mage(Character):
    def __init__(self, name: str, weapon: Weapon, armor: Armor, strategy: Optional[CombatStrategy] = None):
        actual_strategy = strategy if strategy is not None else SpellCastingStrategy()
        super().__init__(name, weapon, armor, actual_strategy)
        self.max_mana = BASE_MAGE_MANA
        self.mana = self.max_mana

    def special_ability_name(self) -> str:
        return "Meditación Arcana" # Cambiado de Bola de Fuego, que es más una acción de estrategia

    def use_special_ability(self, target: Optional['Character']) -> str:
        mana_recovered = BASE_MAGE_MANA // 4 # Recupera 25% del maná máximo
        self.mana += mana_recovered
        if self.mana > self.max_mana:
            self.mana = self.max_mana
        return f"{self.name} usa {self.special_ability_name()} y recupera {mana_recovered} de maná. Maná actual: {self.mana}/{self.max_mana}."

    def use_mana(self, amount: int) -> bool:
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False

class Rogue(Character):
    def __init__(self, name: str, weapon: Weapon, armor: Armor, strategy: Optional[CombatStrategy] = None):
        actual_strategy = strategy if strategy is not None else AggressiveStrategy()
        super().__init__(name, weapon, armor, actual_strategy)
        self.stealth_points = BASE_ROGUE_STEALTH_POINTS # Aún no se usa mecánicamente

    def special_ability_name(self) -> str:
        return "Ataque Preciso" # Un ataque que ignora parte de la armadura o tiene más chance de crítico (simplificado)

    def use_special_ability(self, target: Optional['Character']) -> str:
        if not target or not target.is_alive():
            return f"{self.name} busca un objetivo para su {self.special_ability_name()}, pero no hay nadie válido."

        # Ataque especial: mayor daño o ignora armadura (simplificado como un ataque más fuerte)
        base_damage = self.get_attack_power() + 5 # Bonus para el ataque preciso
        # Para este ataque especial, podríamos ignorar una porción de la armadura del objetivo
        # damage_reduction = target.armor.defense_bonus() // 2 # Ignora la mitad, por ejemplo
        # actual_damage = max(0, base_damage - damage_reduction)
        actual_damage = base_damage # Simplificado: solo más daño base por ahora

        feedback = f"{self.name} usa {self.special_ability_name()} contra {target.name}!\n"
        feedback += target.take_damage(actual_damage)
        return feedback