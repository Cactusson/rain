from . import prepare, tools
from .states import game, menu, high_score


def main():
    run_it = tools.Control(prepare.ORIGINAL_CAPTION)
    state_dict = {'GAME': game.Game(),
                  'MENU': menu.Menu(),
                  'HIGH_SCORE': high_score.HighScore()}
    run_it.setup_states(state_dict, 'MENU')
    run_it.main()
