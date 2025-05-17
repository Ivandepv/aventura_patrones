# game/factories.py
"""
Define las fábricas abstractas y concretas para la creación de personajes y su equipo.
"""
from abc import ABC, abstractmethod
from game.characters import Character, Warrior, Mage, Rogue
from game.items import Weapon, Armor, Sword, Staff, Dagger, Chainmail, Robe, LeatherArmor
from game.strategies import AggressiveStrategy, SpellCastingStrategy # Necesario si las clases las usan por defecto

class CharacterEquipmentFactory(ABC):
    @abstractmethod
    def create_character(self, name: str) -> Character:
        pass

    @abstractmethod
    def equip_weapon(self) -> Weapon: # Podrían ser métodos protegidos si solo la fábrica los usa
        pass

    @abstractmethod
    def equip_armor(self) -> Armor: # Podrían ser métodos protegidos
        pass

class WarriorFactory(CharacterEquipmentFactory):
    def create_character(self, name: str) -> Character:
        # La estrategia por defecto ya se maneja en el constructor de Warrior
        return Warrior(name, self.equip_weapon(), self.equip_armor())

    def equip_weapon(self) -> Weapon:
        return Sword()

    def equip_armor(self) -> Armor:
        return Chainmail()

class MageFactory(CharacterEquipmentFactory):
    def create_character(self, name: str) -> Character:
        return Mage(name, self.equip_weapon(), self.equip_armor())

    def equip_weapon(self) -> Weapon:
        return Staff()

    def equip_armor(self) -> Armor:
        return Robe()

class RogueFactory(CharacterEquipmentFactory):
    def create_character(self, name: str) -> Character:
        return Rogue(name, self.equip_weapon(), self.equip_armor())

    def equip_weapon(self) -> Weapon:
        return Dagger()

    def equip_armor(self) -> Armor:
        return LeatherArmor()