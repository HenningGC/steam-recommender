def formatter(game):
    
    game = game.replace("'","").replace("-"," ").replace(",","").replace(".","").lower()
    
    words = game.split()

    return "-".join(words)
