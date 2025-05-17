# game/items.py
"""
Define los ítems del juego, incluyendo armas, armaduras y el sistema de decoración para encantamientos.
"""
from abc import ABC, abstractmethod

# --- Interfaz Común para Ítems Decorables ---
class ItemEnhancement(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

# --- Interfaces para los Productos (Componentes) ---
class Weapon(ItemEnhancement):
    @abstractmethod
    def attack_bonus(self) -> int:
        pass

class Armor(ItemEnhancement):
    @abstractmethod
    def defense_bonus(self) -> int:
        pass

# --- Productos Concretos: Armas ---
class Sword(Weapon):
    def get_name(self) -> str:
        return "Espada"

    def attack_bonus(self) -> int:
        return 5

    def get_description(self) -> str:
        return "Una espada afilada y confiable."

class Staff(Weapon):
    def get_name(self) -> str:
        return "Vara"

    def attack_bonus(self) -> int:
        return 3

    def get_description(self) -> str:
        return "Una vara de madera nudosa, ideal para canalizar energías."

class Dagger(Weapon):
    def get_name(self) -> str:
        return "Daga"

    def attack_bonus(self) -> int:
        return 2

    def get_description(self) -> str:
        return "Una daga corta y sigilosa, perfecta para ataques rápidos."

# --- Productos Concretos: Armaduras ---
class Chainmail(Armor):
    def get_name(self) -> str:
        return "Cota de Mallas"

    def defense_bonus(self) -> int:
        return 10

    def get_description(self) -> str:
        return "Una cota de mallas resistente que ofrece buena protección."

class Robe(Armor):
    def get_name(self) -> str:
        return "Túnica"

    def defense_bonus(self) -> int:
        return 3

    def get_description(self) -> str:
        return "Una túnica ligera, ofrece poca protección física pero no estorba."

class LeatherArmor(Armor):
    def get_name(self) -> str:
        return "Armadura de Cuero"

    def defense_bonus(self) -> int:
        return 6

    def get_description(self) -> str:
        return "Una armadura de cuero curtido, balance entre movilidad y protección."

# --- Clase Decoradora Base Abstracta para Armas ---
class WeaponDecorator(Weapon, ABC):
    _decorated_weapon: Weapon

    def __init__(self, weapon: Weapon):
        self._decorated_weapon = weapon

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass
    
    @abstractmethod
    def attack_bonus(self) -> int:
        pass

# --- Decoradores Concretos para Armas ---
class FireEnchantment(WeaponDecorator):
    def get_name(self) -> str:
        return f"{self._decorated_weapon.get_name()} de Fuego"

    def attack_bonus(self) -> int:
        return self._decorated_weapon.attack_bonus() + 3

    def get_description(self) -> str:
        return f"{self._decorated_weapon.get_description()} Ahora emite un calor abrasador y añade daño de fuego."

class PoisonEnchantment(WeaponDecorator):
    def get_name(self) -> str:
        return f"{self._decorated_weapon.get_name()} Venenosa"

    def attack_bonus(self) -> int:
        return self._decorated_weapon.attack_bonus() + 1 # Podría aplicar un estado "envenenado" en un futuro.

    def get_description(self) -> str:
        return f"{self._decorated_weapon.get_description()} Está cubierta de una sustancia tóxica."

class VorpalEnchantment(WeaponDecorator):
    def get_name(self) -> str:
        return f"{self._decorated_weapon.get_name()} Aniquiladora (Vorpal)"

    def attack_bonus(self) -> int:
        return self._decorated_weapon.attack_bonus() + 10

    def get_description(self) -> str:
        return f"{self._decorated_weapon.get_description()} Susurros de poder emanan de esta hoja, ¡capaz de decapitar con un golpe de suerte!"