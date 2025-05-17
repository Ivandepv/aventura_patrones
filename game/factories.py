# game/factories.py
from abc import ABC, abstractmethod
from game.characters import Character, Warrior, Mage, Rogue # Clases de personajes
from game.items import Weapon, Armor, Sword, Staff, Dagger, Chainmail, Robe, LeatherArmor # Clases de items

# --- Interfaz de la Fábrica Abstracta ---
class CharacterEquipmentFactory(ABC):
    @abstractmethod
    def create_character(self, name: str) -> Character:
        pass

    @abstractmethod
    def equip_weapon(self) -> Weapon:
        pass

    @abstractmethod
    def equip_armor(self) -> Armor:
        pass

# --- Fábricas Concretas ---

class WarriorFactory(CharacterEquipmentFactory):
    def create_character(self, name: str) -> Character:
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