# game/constants.py
"""
Constantes del juego.
"""

DIRECTIONS = ["norte", "sur", "este", "oeste"]
STRATEGY_NAMES = {
    "agresiva": "agresiva",
    "defensiva": "defensiva",
    "hechizos": "hechizos"
}

# Nuevas constantes para mecánicas de juego
BASE_PLAYER_HEALTH = 100
BASE_WARRIOR_HEALTH_BONUS = 20
BASE_MAGE_MANA = 100
BASE_ROGUE_STEALTH_POINTS = 50 # Aún no lo usaremos mecánicamente, pero está para el futuro

DEFENSIVE_STRATEGY_HEAL = 10
WARRIOR_FURIA_TURNS = 2 # Duración del buff de Furia
WARRIOR_FURIA_BONUS_DAMAGE = 5