from qlearning_model import model
from qlearning import simulate_game

# Init algorithm
game = model()

# Compute equilibrium
game_equilibrium = simulate_game(game)
