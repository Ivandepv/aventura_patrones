# main.py
from game.factories import WarriorFactory, MageFactory, RogueFactory, CharacterEquipmentFactory
from game.characters import Character

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

    # Aquí iría el bucle principal del juego
    # game_loop()

if __name__ == "__main__":
    main()