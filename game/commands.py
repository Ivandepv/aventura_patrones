# game/commands.py
"""
Define la interfaz de Comando y los comandos concretos para las acciones del jugador.
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, Type # Para el strategy_map

# Importaciones de estrategias movidas al inicio del archivo
from game.strategies import CombatStrategy, AggressiveStrategy, DefensiveStrategy, SpellCastingStrategy
from game.constants import DIRECTIONS, STRATEGY_NAMES # Usando el archivo de constantes

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
    def __init__(self, actor: 'Character'):
        self.actor = actor

    def execute(self) -> str:
        # Character.describe() ahora retorna un string.
        return self.actor.describe()

class AttackCommand(Command):
    def __init__(self, attacker: 'Character', target: 'Character'):
        self.attacker = attacker
        self.target = target

    def execute(self) -> str:
        if self.attacker and self.target:
            if self.target.health <= 0: # Chequeo adicional
                return f"{self.target.name} ya está derrotado."
            return self.attacker.perform_combat_action(self.target)
        return "No se puede atacar (objetivo no especificado o no válido)."

class MoveCommand(Command):
    def __init__(self, actor: 'Character', direction: str):
        self.actor = actor
        self.direction = direction.lower()

    def execute(self) -> str:
        if self.direction in DIRECTIONS:
            # Lógica de movimiento real iría aquí (ej. actualizar posición en un mapa)
            return f"{self.actor.name} se mueve hacia el {self.direction}."
        else:
            return f"No se puede mover en la dirección '{self.direction}'. Direcciones válidas: {', '.join(DIRECTIONS)}."

class ChangeStrategyCommand(Command):
    # El mapa ahora referencia los nombres de estrategia de constants.py
    # y usa tipos para las clases de estrategia.
    STRATEGY_CLASSES: Dict[str, Type[CombatStrategy]] = {
        STRATEGY_NAMES["agresiva"]: AggressiveStrategy,
        STRATEGY_NAMES["defensiva"]: DefensiveStrategy,
        STRATEGY_NAMES["hechizos"]: SpellCastingStrategy
    }
    def __init__(self, actor: 'Character', new_strategy_name: str):
        self.actor = actor
        self.new_strategy_name = new_strategy_name.lower()

    def execute(self) -> str:
        strategy_class = self.STRATEGY_CLASSES.get(self.new_strategy_name)
        if strategy_class:
            new_strategy_instance = strategy_class() # Creamos nueva instancia
            self.actor.set_combat_strategy(new_strategy_instance)
            return f"{self.actor.name} ha cambiado su estrategia de combate a: {self.new_strategy_name.capitalize()}."
        else:
            available_strats = ", ".join(self.STRATEGY_CLASSES.keys())
            return f"Estrategia '{self.new_strategy_name}' desconocida. Disponibles: {available_strats}."

class QuitCommand(Command):
    def execute(self) -> str:
        return "salir_command_signal" # Señal especial para el bucle de juego