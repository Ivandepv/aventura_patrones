# game/items.py
from abc import ABC, abstractmethod

# --- Interfaces para los Productos (Componentes) ---

class ItemEnhancement(ABC): # Interfaz común para cualquier tipo de item que pueda ser decorado
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

class Weapon(ItemEnhancement): # Weapon ahora hereda de ItemEnhancement
    @abstractmethod
    def attack_bonus(self) -> int:
        pass

    # get_name y get_description vendrán de los decoradores o de la implementación base
    # pero necesitamos que Weapon sea un ItemEnhancement para que los decoradores genéricos funcionen

class Armor(ItemEnhancement): # Armor ahora hereda de ItemEnhancement
    @abstractmethod
    def defense_bonus(self) -> int:
        pass

    # get_name y get_description vendrán de los decoradores o de la implementación base

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
        return "Una vara de madera nudosa, canaliza energías."

class Dagger(Weapon):
    def get_name(self) -> str:
        return "Daga"

    def attack_bonus(self) -> int:
        return 2

    def get_description(self) -> str:
        return "Una daga corta y sigilosa."

# --- Productos Concretos: Armaduras ---

class Chainmail(Armor):
    def get_name(self) -> str:
        return "Cota de Mallas"

    def defense_bonus(self) -> int:
        return 10

    def get_description(self) -> str:
        return "Una cota de mallas resistente."

class Robe(Armor):
    def get_name(self) -> str:
        return "Túnica"

    def defense_bonus(self) -> int:
        return 3

    def get_description(self) -> str:
        return "Una túnica ligera, ofrece poca protección física."

class LeatherArmor(Armor):
    def get_name(self) -> str:
        return "Armadura de Cuero"

    def defense_bonus(self) -> int:
        return 6

    def get_description(self) -> str:
        return "Una armadura de cuero curtido."


# --- Clase Decoradora Base Abstracta ---
# Haremos un decorador para Weapon y otro para Armor, o uno más genérico si es posible.
# Empecemos con decoradores específicos para Weapon por simplicidad.

class WeaponDecorator(Weapon, ABC): # Hereda de Weapon para ser un tipo de Weapon
    _decorated_weapon: Weapon

    def __init__(self, weapon: Weapon):
        self._decorated_weapon = weapon

    @abstractmethod # Forzamos a las subclases a implementar cómo modifican el nombre
    def get_name(self) -> str:
        pass

    @abstractmethod # Forzamos a las subclases a implementar cómo modifican la descripción
    def get_description(self) -> str:
        pass
    
    @abstractmethod # Forzamos a las subclases a implementar cómo modifican el bonus de ataque
    def attack_bonus(self) -> int:
        pass



# --- Decoradores Concretos para Armas ---

class FireEnchantment(WeaponDecorator):
    def get_name(self) -> str:
        return f"{self._decorated_weapon.get_name()} de Fuego"

    def attack_bonus(self) -> int:
        return self._decorated_weapon.attack_bonus() + 3 # El fuego añade 3 de daño

    def get_description(self) -> str:
        return f"{self._decorated_weapon.get_description()} Ahora emite un calor abrasador y añade daño de fuego."

class PoisonEnchantment(WeaponDecorator):
    def get_name(self) -> str:
        return f"{self._decorated_weapon.get_name()} Venenosa"

    def attack_bonus(self) -> int:
        # El veneno podría no añadir daño directo, sino un efecto.
        # En el futuro, esto podría interactuar con un sistema de estado.
        return self._decorated_weapon.attack_bonus() + 1

    def get_description(self) -> str:
        return f"{self._decorated_weapon.get_description()} Está cubierta de una sustancia tóxica que puede envenenar."

class VorpalEnchantment(WeaponDecorator): # Un encantamiento más poderoso
    def get_name(self) -> str:
        return f"{self._decorated_weapon.get_name()} Aniquiladora (Vorpal)"

    def attack_bonus(self) -> int:
        return self._decorated_weapon.attack_bonus() + 10 # Gran aumento de daño

    def get_description(self) -> str:
        return f"{self._decorated_weapon.get_description()} Susurros de poder emanan de esta hoja, ¡capaz de decapitar con un golpe de suerte!"