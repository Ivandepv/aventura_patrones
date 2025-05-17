# game/commands.py
"""
Define la interfaz de Comando y los comandos concretos para las acciones del jugador.
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, Type

from game.strategies import CombatStrategy, AggressiveStrategy, DefensiveStrategy, SpellCastingStrategy
from game.constants import DIRECTIONS, STRATEGY_NAMES
from typing import Optional

if TYPE_CHECKING:
    from game.characters import Character

class Command(ABC):
    @abstractmethod
    def execute(self) -> str:
        """
        Ejecuta el comando.
        Retorna un string describiendo el resultado de la acción.
        """
        pass

class LookCommand(Command):
    def __init__(self, actor: 'Character', target: Optional['Character'] = None):
        self.actor = actor
        self.target = target # Para mirar a un enemigo específico

    def execute(self) -> str:
        if self.target and self.target.is_alive():
            return self.target.describe()
        # Si no hay objetivo o no está vivo, el actor se describe a sí mismo o el entorno
        # Podríamos expandir para mirar la 'sala' actual si tuviéramos ese concepto.
        return self.actor.describe()


class AttackCommand(Command):
    def __init__(self, attacker: 'Character', target: 'Character'):
        self.attacker = attacker
        self.target = target

    def execute(self) -> str:
        if not self.attacker.is_alive():
            return f"{self.attacker.name} no puede atacar, está derrotado."
        if not self.target.is_alive():
            return f"{self.target.name} ya está derrotado. No tiene sentido atacar."
        return self.attacker.perform_combat_action(self.target)


class MoveCommand(Command): # Sin cambios funcionales mayores
    def __init__(self, actor: 'Character', direction: str):
        self.actor = actor
        self.direction = direction.lower()

    def execute(self) -> str:
        if self.direction in DIRECTIONS:
            return f"{self.actor.name} se mueve hacia el {self.direction}. (La exploración del mapa no está implementada)."
        else:
            return f"No se puede mover en la dirección '{self.direction}'. Direcciones válidas: {', '.join(DIRECTIONS)}."


class ChangeStrategyCommand(Command):
    STRATEGY_CLASSES: Dict[str, Type[CombatStrategy]] = {
        STRATEGY_NAMES["agresiva"]: AggressiveStrategy,
        STRATEGY_NAMES["defensiva"]: DefensiveStrategy,
        STRATEGY_NAMES["hechizos"]: SpellCastingStrategy
    }
    def __init__(self, actor: 'Character', new_strategy_name: str):
        self.actor = actor
        self.new_strategy_name = new_strategy_name.lower()

    def execute(self) -> str:
        if not self.actor.is_alive():
            return f"{self.actor.name} no puede cambiar de estrategia, está derrotado."

        strategy_class = self.STRATEGY_CLASSES.get(self.new_strategy_name)
        if strategy_class:
            new_strategy_instance = strategy_class()
            self.actor.set_combat_strategy(new_strategy_instance)
            return f"{self.actor.name} ha cambiado su estrategia de combate a: {self.new_strategy_name.capitalize()}."
        else:
            available_strats = ", ".join(self.STRATEGY_CLASSES.keys())
            return f"Estrategia '{self.new_strategy_name}' desconocida. Disponibles: {available_strats}."


class SpecialAbilityCommand(Command):
    def __init__(self, actor: 'Character', target: Optional['Character'] = None):
        self.actor = actor
        self.target = target

    def execute(self) -> str:
        if not self.actor.is_alive():
            return f"{self.actor.name} no puede usar su habilidad, está derrotado."
        return self.actor.use_special_ability(self.target)


class QuitCommand(Command):
    def execute(self) -> str:
        return "salir_command_signal"