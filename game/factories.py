# game/factories.py
"""
Define las fábricas abstractas y concretas para la creación de personajes y su equipo.
"""
from abc import ABC, abstractmethod
from typing import Type # Para type hinting de clases de estrategia

from game.characters import Character, Warrior, Mage, Rogue
from game.items import Weapon, Armor, Sword, Staff, Dagger, Chainmail, Robe, LeatherArmor
from game.strategies import CombatStrategy, AggressiveStrategy, SpellCastingStrategy, DefensiveStrategy

# --- Interfaz de la Fábrica Abstracta ---
class CharacterEquipmentFactory(ABC):
    @abstractmethod
    def create_character(self, name: str) -> Character:
        pass

    # Estos métodos podrían ser protegidos (_equip_weapon) si solo la fábrica los usa internamente
    @abstractmethod
    def equip_weapon(self) -> Weapon:
        pass

    @abstractmethod
    def equip_armor(self) -> Armor:
        pass

    # Opcional: podríamos definir una estrategia por defecto para los personajes creados por esta fábrica
    def get_default_strategy(self) -> Type[CombatStrategy]:
        return AggressiveStrategy # Por defecto, todos son agresivos

# --- Fábricas Concretas ---
class WarriorFactory(CharacterEquipmentFactory):
    def create_character(self, name: str) -> Character:
        # Warrior ya tiene AggressiveStrategy por defecto en su __init__ si no se pasa otra
        return Warrior(name=name, weapon=self.equip_weapon(), armor=self.equip_armor())

    def equip_weapon(self) -> Weapon:
        return Sword()

    def equip_armor(self) -> Armor:
        return Chainmail()
    
    def get_default_strategy(self) -> Type[CombatStrategy]:
        return AggressiveStrategy

class MageFactory(CharacterEquipmentFactory):
    def create_character(self, name: str) -> Character:
        # Mage ya tiene SpellCastingStrategy por defecto
        return Mage(name=name, weapon=self.equip_weapon(), armor=self.equip_armor())

    def equip_weapon(self) -> Weapon:
        return Staff()

    def equip_armor(self) -> Armor:
        return Robe()

    def get_default_strategy(self) -> Type[CombatStrategy]:
        return SpellCastingStrategy

class RogueFactory(CharacterEquipmentFactory):
    def create_character(self, name: str) -> Character:
        # Rogue ya tiene AggressiveStrategy por defecto
        return Rogue(name=name, weapon=self.equip_weapon(), armor=self.equip_armor())

    def equip_weapon(self) -> Weapon:
        return Dagger()

    def equip_armor(self) -> Armor:
        return LeatherArmor()
        
    def get_default_strategy(self) -> Type[CombatStrategy]:
        return AggressiveStrategy

# Podríamos tener una fábrica para enemigos genéricos
class GenericEnemyFactory(CharacterEquipmentFactory):
    def __init__(self, enemy_class: Type[Character], weapon: Weapon, armor: Armor, strategy_class: Type[CombatStrategy]):
        self._enemy_class = enemy_class
        self._weapon = weapon
        self._armor = armor
        self._strategy_class = strategy_class

    def create_character(self, name: str) -> Character:
        return self._enemy_class(name=name,
                                 weapon=self.equip_weapon(),
                                 armor=self.equip_armor(),
                                 strategy=self._strategy_class())
    def equip_weapon(self) -> Weapon:
        return self._weapon

    def equip_armor(self) -> Armor:
        return self._armor