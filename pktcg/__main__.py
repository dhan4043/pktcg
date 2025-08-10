from components.game import CardGame

def start_game():
    game = CardGame.create()
    game.start()

if __name__ == "__main__":
    start_game()
