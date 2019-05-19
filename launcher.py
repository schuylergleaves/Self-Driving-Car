from core.game import game
from core.game.mode import Mode
import sys

arg = sys.argv[1]
mode = None
if arg == "USER_CONTROLLED":
    mode = Mode.USER
elif arg == "AI_CONTROLLED":
    mode = Mode.AI

game = game.Game(mode)
game.run()