# game/strategies.py
from abc import ABC, abstractmethod

# Para evitar la dependencia circular si Character necesita importar Strategy
# y Strategy necesita type hints de Character, usamos una forward declaration.
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.characters import Character # Importación para type hinting

class CombatStrategy(ABC):
    @abstractmethod
    def execute_action(self, actor: 'Character', target: 'Character') -> str:
        """
        Ejecuta una acción de combate.
        Retorna una cadena describiendo la acción realizada.
        """
        pass


class AggressiveStrategy(CombatStrategy):
    def execute_action(self, actor: 'Character', target: 'Character') -> str:
        # Lógica para un ataque agresivo.
        # Por ahora, simulemos un ataque básico usando el arma del actor.
        # En un juego más complejo, aquí podrías calcular daño, verificar si el golpe acierta, etc.
        damage = actor.weapon.attack_bonus() # Simplificado
        # target.health -= damage # (Descomentar cuando tengamos manejo de vida en combate)
        return f"{actor.name} ataca agresivamente a {target.name} con {actor.weapon.get_name()} causando {damage} de daño (simulado)."

class DefensiveStrategy(CombatStrategy):
    def execute_action(self, actor: 'Character', target: 'Character') -> str:
        # Lógica para una acción defensiva.
        # Podría ser aumentar la defensa temporalmente, curarse una pequeña cantidad, etc.
        # actor.defense_points += 5 # Ejemplo
        return f"{actor.name} adopta una postura defensiva, preparándose para el próximo ataque."

class SpellCastingStrategy(CombatStrategy): # Específica para Magos, por ejemplo
    def execute_action(self, actor: 'Character', target: 'Character') -> str:
        # Verificar si el actor tiene 'mana', típico de un Mago
        if hasattr(actor, 'mana') and actor.mana >= 10:
            # actor.mana -= 10 # (Descomentar cuando tengamos manejo de mana)
            spell_damage = 15 # Daño mágico simulado
            # target.health -= spell_damage # (Descomentar)
            return f"{actor.name} lanza un hechizo a {target.name} causando {spell_damage} de daño mágico (simulado)."
        elif hasattr(actor, 'mana') and actor.mana < 10:
            return f"{actor.name} intenta lanzar un hechizo, ¡pero no tiene suficiente maná!"
        else:
            # Si no es un mago o no tiene maná, recurre a un ataque simple (o no hace nada)
            return f"{actor.name} intenta lanzar un hechizo pero no puede. ¡Quizás debería cambiar de estrategia!"
