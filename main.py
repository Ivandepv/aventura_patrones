# main.py
"""
Punto de entrada principal y bucle del juego de aventura basado en texto.
Demuestra el uso de patrones de diseño para crear personajes, ítems y gestionar acciones.
"""
from game.factories import WarriorFactory, MageFactory, RogueFactory, CharacterEquipmentFactory
from game.characters import Character, Warrior, Mage, Rogue # Importaciones consolidadas
# game.items y game.strategies no necesitan importarse aquí si no se usan directamente.
from game.commands import Command, LookCommand, AttackCommand, MoveCommand, ChangeStrategyCommand, QuitCommand
from game.constants import STRATEGY_NAMES # Para el mensaje de ayuda de estrategias

def parse_input(input_str: str, player: Character, current_enemy: Character = None) -> Command | None:
    """
    Parsea la entrada del usuario y la convierte en un objeto Comando.
    Retorna un Comando o None si la entrada no es válida.
    """
    parts = input_str.lower().strip().split()
    if not parts:
        print("Por favor, introduce un comando.")
        return None

    action = parts[0]

    if action == "mirar":
        return LookCommand(player)
    elif action == "atacar":
        if current_enemy and current_enemy.health > 0:
            return AttackCommand(player, current_enemy)
        elif current_enemy and current_enemy.health <= 0:
            print(f"{current_enemy.name} ya ha sido derrotado.")
            return None
        else:
            print("No hay nadie a quien atacar aquí.")
            return None
    elif action == "mover":
        if len(parts) > 1:
            direction = parts[1]
            return MoveCommand(player, direction)
        else:
            print("Mover ¿hacia dónde? (ej: mover norte)")
            return None
    elif action == "estrategia":
        if len(parts) > 1:
            strategy_name_input = parts[1]
            return ChangeStrategyCommand(player, strategy_name_input)
        else:
            available_strats = ", ".join(STRATEGY_NAMES.values())
            print(f"Cambiar a qué estrategia? (ej: estrategia agresiva). Disponibles: {available_strats}.")
            return None
    elif action == "salir":
        return QuitCommand()
    else:
        print(f"Comando desconocido: '{action}'. Comandos comunes: mirar, mover, atacar, estrategia, salir.")
        return None

def game_loop(player: Character):
    """Bucle principal del juego."""
    print("\n" + "="*30)
    print("--- ¡Comienza la Aventura! ---")
    print("Escribe 'mirar', 'mover [direccion]', 'atacar', 'estrategia [nombre]', o 'salir'.")
    print("="*30 + "\n")


    # Creamos un enemigo de ejemplo para interactuar
    # TODO: La creación de enemigos podría ser más dinámica o basada en la 'sala' actual.
    enemy_factory = RogueFactory() # Podría ser aleatorio o específico de una zona
    current_enemy: Character | None = enemy_factory.create_character("Orco Grunon")
    # current_enemy.set_combat_strategy(AggressiveStrategy()) # Ya tiene una por defecto
    print(f"¡Un {current_enemy.name} ({current_enemy.__class__.__name__}) aparece rugiendo!")
    print(current_enemy.describe())

    while True:
        if player.health <= 0:
            print(f"\nGAME OVER: ¡{player.name} ha sido derrotado!")
            break
        
        user_input = input(f"\n{player.name} (Salud: {player.health})> ")
        command = parse_input(user_input, player, current_enemy)

        if isinstance(command, Command):
            result = command.execute()

            if result == "salir_command_signal": # Señal de QuitCommand
                print("¡Hasta la próxima aventura!")
                break
            
            print(f"\n{result}") # Imprime el resultado de la acción del jugador

            # Lógica del turno del enemigo si el jugador realizó una acción y hay un enemigo
            if current_enemy and current_enemy.health > 0:
                # El enemigo solo actúa si el jugador no acaba de salir o mirar (o alguna otra acción no agresiva)
                # Esto es una simplificación, podrías tener una lógica más compleja para el turno del enemigo.
                if not isinstance(command, (LookCommand, QuitCommand, ChangeStrategyCommand, MoveCommand)):
                    print(f"\n--- Turno de {current_enemy.name} (Salud: {current_enemy.health}) ---")
                    enemy_action_result = current_enemy.perform_combat_action(player)
                    print(enemy_action_result)
            
            # Comprobar si el enemigo fue derrotado después del turno del jugador o del enemigo
            if current_enemy and current_enemy.health <= 0:
                print(f"\n¡Has derrotado a {current_enemy.name}!")
                current_enemy = None # Eliminar al enemigo actual
                # TODO: Podrías generar un nuevo enemigo o dar alguna recompensa.

def main():
    """Función principal para iniciar el juego."""
    print("="*30)
    print("  Bienvenido al Juego de Aventura con Patrones de Diseño  ")
    print("="*30)
    player_name = input("Ingresa el nombre de tu personaje: ")

    print("\nElige tu clase:")
    class_options = {"1": "Guerrero", "2": "Mago", "3": "Pícaro"}
    for key, value in class_options.items():
        print(f"{key}. {value}")

    choice = ""
    player_factory: CharacterEquipmentFactory | None = None # Type hint para claridad

    while choice not in class_options:
        choice = input(f"Selecciona una opción ({', '.join(class_options.keys())}): ")
        if choice == "1":
            player_factory = WarriorFactory()
        elif choice == "2":
            player_factory = MageFactory()
        elif choice == "3":
            player_factory = RogueFactory()
        else:
            print("Opción no válida. Intenta de nuevo.")

    player = player_factory.create_character(player_name)
    print(f"\n¡{player_name}, tu aventura como {player.__class__.__name__} comienza!")
    print(player.describe()) # Imprime la descripción inicial del jugador

    game_loop(player)

if __name__ == "__main__":
    main()