# game/strategies.py
"""
Define las estrategias de combate que los personajes pueden utilizar.
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.characters import Character # Importación para type hinting

class CombatStrategy(ABC):
    @abstractmethod
    def execute_action(self, actor: 'Character', target: 'Character') -> str:
        """
        Ejecuta una acción de combate.
        Retorna una cadena describiendo la acción realizada y su resultado.
        """
        pass

class AggressiveStrategy(CombatStrategy):
    def execute_action(self, actor: 'Character', target: 'Character') -> str:
        base_damage = actor.weapon.attack_bonus()
        # Podrías añadir una pequeña varianza o bonus de fuerza del actor
        actual_damage = base_damage 
        
        if target.health > 0: # Solo atacar si el objetivo está vivo
            target.take_damage(actual_damage)
            return (f"{actor.name} ataca agresivamente a {target.name} con {actor.weapon.get_name()} "
                    f"causando {actual_damage} de daño. ¡{target.name} tiene {target.health} de salud restante!")
        else:
            return f"{actor.name} intenta atacar a {target.name}, pero ya está derrotado."


class DefensiveStrategy(CombatStrategy):
    def execute_action(self, actor: 'Character', target: 'Character') -> str:
        # En lugar de atacar, el actor podría, por ejemplo, reducir el próximo daño que reciba
        # o curarse una pequeña cantidad si tuviera esa habilidad.
        # Por ahora, solo una acción defensiva simple.
        # actor.temporary_defense_bonus += 2 # Ejemplo de mecánica posible
        return f"{actor.name} adopta una postura defensiva, preparándose para el próximo ataque."

class SpellCastingStrategy(CombatStrategy):
    SPELL_COST = 10
    SPELL_DAMAGE = 15

    def execute_action(self, actor: 'Character', target: 'Character') -> str:
        if hasattr(actor, 'mana'):
            if actor.mana >= self.SPELL_COST:
                actor.mana -= self.SPELL_COST
                if target.health > 0:
                    target.take_damage(self.SPELL_DAMAGE)
                    return (f"{actor.name} lanza un hechizo a {target.name} "
                            f"causando {self.SPELL_DAMAGE} de daño mágico. ¡{target.name} tiene {target.health} de salud restante! "
                            f"{actor.name} tiene {actor.mana} de maná restante.")
                else:
                    return f"{actor.name} lanza un hechizo a {target.name}, pero ya está derrotado. ({actor.mana} maná restante)"
            else:
                return f"{actor.name} intenta lanzar un hechizo, ¡pero no tiene suficiente maná ({actor.mana})!"
        else:
            return f"{actor.name} intenta lanzar un hechizo pero no es un lanzador de conjuros."