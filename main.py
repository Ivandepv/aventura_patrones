# main.py
from game.factories import WarriorFactory, MageFactory, RogueFactory, CharacterEquipmentFactory
from game.characters import Character
from game.items import Sword, FireEnchantment, PoisonEnchantment, VorpalEnchantment # Nuevas importaciones

def create_player(factory: CharacterEquipmentFactory, player_name: str) -> Character:
    """Crea un personaje usando la fábrica proporcionada."""
    player = factory.create_character(player_name)
    return player

def main():
    print("¡Bienvenido al Juego de Aventura!")
    player_name = input("Ingresa el nombre de tu personaje: ")

    print("\nElige tu clase:")
    print("1. Guerrero")
    print("2. Mago")
    print("3. Pícaro")

    choice = ""
    player_factory = None

    while choice not in ["1", "2", "3"]:
        choice = input("Selecciona una opción (1, 2, o 3): ")
        if choice == "1":
            player_factory = WarriorFactory()
        elif choice == "2":
            player_factory = MageFactory()
        elif choice == "3":
            player_factory = RogueFactory()
        else:
            print("Opción no válida. Intenta de nuevo.")

    player = create_player(player_factory, player_name)

    print(f"\n¡{player_name}, tu aventura como {player.__class__.__name__} comienza!")
    player.describe()

    print("\n--- Probando Decoradores de Armas ---")
    # Supongamos que el jugador tiene una espada simple (esto podría venir de la fábrica)
    # o la encuentra.
    if isinstance(player.weapon, Sword): # Solo para el ejemplo, si el jugador tiene una espada
        current_weapon = player.weapon
        print(f"Arma actual: {current_weapon.get_name()}, Bonus: {current_weapon.attack_bonus()}")
        print(f"Descripción: {current_weapon.get_description()}")

        # El jugador encuentra un pergamino de encantamiento de fuego
        print("\n¡Has encontrado un Pergamino de Encantamiento de Fuego!")
        current_weapon = FireEnchantment(current_weapon)
        player.weapon = current_weapon # Actualizamos el arma del jugador
        print(f"Arma encantada: {current_weapon.get_name()}, Bonus: {current_weapon.attack_bonus()}")
        print(f"Descripción: {current_weapon.get_description()}")

        # Luego, encuentra uno de veneno ¡y lo aplica sobre el arma ya encantada con fuego!
        print("\n¡Has encontrado Esencia de Veneno!")
        current_weapon = PoisonEnchantment(current_weapon)
        player.weapon = current_weapon # Actualizamos el arma del jugador
        print(f"Arma doblemente encantada: {current_weapon.get_name()}, Bonus: {current_weapon.attack_bonus()}")
        print(f"Descripción: {current_weapon.get_description()}")
        
        # Y finalmente, un encantamiento legendario
        print("\n¡Un antiguo poder imbuye tu arma!")
        current_weapon = VorpalEnchantment(current_weapon)
        player.weapon = current_weapon # Actualizamos el arma del jugador
        print(f"Arma legendaria: {current_weapon.get_name()}, Bonus: {current_weapon.attack_bonus()}")
        print(f"Descripción: {current_weapon.get_description()}")

    # Actualizamos la descripción del jugador para ver el arma nueva
    print("\n--- Estado del Jugador Actualizado ---")
    player.describe()


    # Aquí iría el bucle principal del juego
    # game_loop()

if __name__ == "__main__":
    main()