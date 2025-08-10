from components.game import CardGame

def start_game():
    game = CardGame.create()
    game.loop()

if __name__ == "__main__":
    start_game()
