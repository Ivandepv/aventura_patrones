# main.py
"""
Punto de entrada principal y bucle del juego de aventura basado en texto.
Ahora con mecánicas de juego más funcionales.
"""
import random
from typing import Optional, List, Type # Para listas de tipos de enemigos

from game.factories import WarriorFactory, MageFactory, RogueFactory, CharacterEquipmentFactory
from game.characters import Character, Warrior, Mage, Rogue # Clases de personaje
from game.items import Sword, Staff, Dagger, Chainmail, Robe, LeatherArmor # Ítems base para enemigos
from game.strategies import AggressiveStrategy, DefensiveStrategy, SpellCastingStrategy # Para enemigos
from game.commands import (
    Command, LookCommand, AttackCommand, MoveCommand,
    ChangeStrategyCommand, SpecialAbilityCommand, QuitCommand
)
from game.constants import STRATEGY_NAMES # Para mensajes de ayuda

# --- Configuración de Enemigos ---
ENEMY_TYPES: List[Type[CharacterEquipmentFactory]] = [RogueFactory, WarriorFactory] # Fábricas para tipos de enemigos
ENEMY_NAMES = ["Ladrón Sombrío", "Orco Bruto", "Esqueleto Guardián", "Lobo Feroz", "Bandido Despiadado"]

# --- Funciones Auxiliares ---
def spawn_enemy(player_level: int = 1) -> Optional[Character]:
    """Genera un nuevo enemigo."""
    if not ENEMY_TYPES:
        return None # No hay tipos de enemigos definidos para generar

    enemy_factory_class = random.choice(ENEMY_TYPES)
    enemy_factory = enemy_factory_class()
    enemy_name = random.choice(ENEMY_NAMES)
    
    # Personaliza el enemigo (opcional, podrías ajustar su estrategia o nivel aquí)
    enemy = enemy_factory.create_character(f"{enemy_name} (Nivel {player_level})")
    
    # Los enemigos podrían tener estrategias diferentes por defecto o aleatorias
    # Por ahora, la estrategia por defecto de su clase (ej. Rogue -> Aggressive) se aplica.
    # Opcional: enemy.set_combat_strategy(random.choice([AggressiveStrategy(), DefensiveStrategy()])())

    print(f"\n¡Un {enemy.name} ({enemy.__class__.__name__}) aparece rugiendo!")
    return enemy

def parse_input(input_str: str, player: Character, current_enemy: Optional[Character]) -> Optional[Command]:
    """
    Parsea la entrada del usuario y la convierte en un objeto Comando.
    Retorna un Comando o None si la entrada no es válida.
    """
    parts = input_str.lower().strip().split()
    if not parts:
        print("Por favor, introduce un comando.")
        return None

    action = parts[0]
    target_enemy = current_enemy if current_enemy and current_enemy.is_alive() else None

    if action == "mirar":
        if len(parts) > 1 and parts[1] == "enemigo":
            return LookCommand(player, target_enemy if target_enemy else None)
        return LookCommand(player)
    elif action == "atacar":
        if target_enemy:
            return AttackCommand(player, target_enemy)
        else:
            print("No hay un enemigo válido a quien atacar aquí.")
            return None
    elif action == "mover": # La funcionalidad de 'mover' sigue siendo simbólica
        if len(parts) > 1:
            return MoveCommand(player, parts[1])
        else:
            print("Mover ¿hacia dónde? (ej: mover norte)")
            return None
    elif action == "estrategia":
        if len(parts) > 1:
            return ChangeStrategyCommand(player, parts[1])
        else:
            available_strats = ", ".join(STRATEGY_NAMES.values())
            print(f"Cambiar a qué estrategia? (ej: estrategia agresiva). Disponibles: {available_strats}.")
            return None
    elif action == "habilidad":
        return SpecialAbilityCommand(player, target_enemy) # Habilidad puede requerir un objetivo
    elif action == "salir":
        return QuitCommand()
    else:
        print(f"Comando desconocido: '{action}'. Comandos: mirar (enemigo), atacar, mover, estrategia, habilidad, salir.")
        return None

def game_loop(player: Character):
    """Bucle principal del juego con mecánicas funcionales."""
    print("\n" + "="*40)
    print("--- ¡LA AVENTURA COMIENZA DE VERDAD! ---")
    print("Comandos: mirar (o mirar enemigo), atacar, mover [dir], estrategia [nombre], habilidad, salir.")
    print("="*40 + "\n")

    player_level = 1 # Nivel del jugador, podría usarse para escalar enemigos
    enemies_defeated_count = 0
    current_enemy = spawn_enemy(player_level)

    while True:
        print("\n" + "-"*10 + " TU TURNO " + "-"*10)
        if current_enemy:
            print(current_enemy.describe()) # Muestra estado del enemigo al inicio del turno del jugador
        print(player.describe()) # Muestra estado del jugador

        if not player.is_alive():
            print(f"\nGAME OVER: ¡{player.name} ha sido derrotado!")
            print(f"Enemigos derrotados: {enemies_defeated_count}")
            break
        
        user_input = input(f"\n{player.name} (Salud: {player.health})> ")
        command = parse_input(user_input, player, current_enemy)

        player_action_feedback = ""
        if isinstance(command, Command):
            player_action_feedback = command.execute()

            if player_action_feedback == "salir_command_signal":
                print("\n¡Gracias por jugar! ¡Hasta la próxima aventura!")
                print(f"Enemigos derrotados: {enemies_defeated_count}")
                break
            
            if player_action_feedback: # Imprime el resultado de la acción del jugador
                 print(f"\n{player_action_feedback}")
            
            player.tick_effects() # Actualizar efectos como Furia

        # Verificar si el enemigo fue derrotado por la acción del jugador
        if current_enemy and not current_enemy.is_alive():
            print(f"\n¡Has derrotado a {current_enemy.name}!")
            current_enemy = None
            enemies_defeated_count += 1
            player_level +=1 # El jugador sube de nivel simbólicamente
            print(f"Has derrotado {enemies_defeated_count} enemigos.")
            # Pequeña recompensa o preparación para el siguiente
            player.heal(player.max_health // 4) # Jugador se cura un 25%
            print("Te sientes revitalizado para el próximo combate...")
            current_enemy = spawn_enemy(player_level) # Nuevo enemigo aparece

        # Turno del Enemigo (si sigue vivo y el jugador también)
        if current_enemy and current_enemy.is_alive() and player.is_alive():
            # El enemigo actúa si el jugador no está simplemente mirando o cambiando estrategia sin atacar
            # O si el jugador no acaba de derrotar al enemigo en este mismo turno.
            should_enemy_act = True
            if isinstance(command, (LookCommand, ChangeStrategyCommand, QuitCommand)): # Acciones no ofensivas directas
                 if not (isinstance(command, LookCommand) and command.target == current_enemy) : # Si mira al enemigo, el enemigo podría reaccionar
                    should_enemy_act = False # Simplificación: enemigo no actúa en acciones pasivas
            
            if player_action_feedback and "derrotado" in player_action_feedback and current_enemy.name in player_action_feedback: # Si el jugador derrotó al enemigo en su acción
                should_enemy_act = False

            if should_enemy_act:
                print("\n" + "-"*10 + f" TURNO DE {current_enemy.name.upper()} " + "-"*10)
                enemy_action_result = current_enemy.perform_combat_action(player)
                print(enemy_action_result)
                current_enemy.tick_effects() # Enemigos también podrían tener efectos

                if not player.is_alive(): # Comprobar si el jugador fue derrotado por el enemigo
                    print(player.describe()) # Mostrar estado final del jugador
                    print(f"\nGAME OVER: ¡{player.name} ha sido derrotado por {current_enemy.name}!")
                    print(f"Enemigos derrotados: {enemies_defeated_count}")
                    break # Fin del juego

        elif not current_enemy and player.is_alive(): # Si no hay enemigo y el jugador está vivo
            print("\nNo hay enemigos cerca. El camino está despejado... por ahora.")
            # Podrías tener un breve respiro o generar uno nuevo si el bucle está diseñado para combate continuo
            if input("¿Avanzar en busca de más aventuras? (s/n): ").lower() == 's':
                current_enemy = spawn_enemy(player_level)
            else:
                print("\nDecides descansar. ¡Gracias por jugar!")
                print(f"Enemigos derrotados: {enemies_defeated_count}")
                break


def main():
    """Función principal para iniciar el juego."""
    print("="*50)
    print("  Bienvenido al Juego de Aventura con Patrones de Diseño  ")
    print("             -- Edición Funcional --                 ")
    print("="*50)
    player_name = input("Ingresa el nombre de tu personaje: ")

    print("\nElige tu clase:")
    class_options = {"1": "Guerrero", "2": "Mago", "3": "Pícaro"}
    for key, value in class_options.items():
        print(f"{key}. {value}")

    choice = ""
    player_factory: Optional[CharacterEquipmentFactory] = None

    while not player_factory: # Bucle hasta que se elija una fábrica válida
        choice = input(f"Selecciona una opción ({', '.join(class_options.keys())}): ")
        if choice == "1":
            player_factory = WarriorFactory()
        elif choice == "2":
            player_factory = MageFactory()
        elif choice == "3":
            player_factory = RogueFactory()
        else:
            print("Opción no válida. Intenta de nuevo.")

    player = player_factory.create_character(player_name) # type: ignore # Sabemos que player_factory no será None aquí

    game_loop(player)

if __name__ == "__main__":
    main()