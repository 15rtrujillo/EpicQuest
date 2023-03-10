from log_manager import LogManager
from player import Player

import game_data_loader
import save_manager


def main():
    """Initialize the game"""
    game_data_loader.load_all()