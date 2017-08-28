class player:
    def __init__(self, name, chip):
        self.name = name
        self.chip = chip
        
    def __str__(self):
        return 'Play %s has %s chips.' % (self.name, str(self.chip))

  
def join_game(players):
    join = True
    while len(players)<6 and join == True:
        name_tmp = input("New players name:")
        chip_tmp = input('Chips that %s has:' % name_tmp)
        try:
            int(chip_tmp)
        except:
            print('Chips number is invalid!\n')
            continue
        else:
            players.append(player(name_tmp, chip_tmp))
            join = (input('More players(Y/N)? ')[0].upper() == 'Y')
        finally:
            print('\nPlayers in the game now:')
            for i in players:
                print(i)

                
                
players = []
join_game(players)
