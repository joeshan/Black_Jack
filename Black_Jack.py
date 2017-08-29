class player:
    def __init__(self, name, chip):
        self.name = name
        self.chip = chip
        
    def __str__(self):
        return 'Play %s has %s chips.' % (self.name, str(self.chip))

    
class card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.suit + self.rank
    
    
class decks:
    suits = ['Heart ', 'Diamond ','Club ','Spade ']
    ranks = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    
    def __init__(self, deck_num):
        self.card_pool = []
        self.deck_num = deck_num
        
        for i in decks.suits:
            for j in decks.ranks:
                self.card_pool.append(card(i,j))
        self.card_pool *= self.deck_num 
    
    def __str__(self):
        return '%d decks shuffled together. %d cards left.' % (self.deck_num, len(self.card_pool)) 

    def shuffle(self):
        random.shuffle(self.card_pool)
        
    def draw_card(self):
        return self.card_pool.pop()


class hand:
    def __init__(self):
        self.hand_cards = []
        self.value = 0
        self.aces = 0
    
    def add_card(self, new_card):
        self.hand_cards.append(new_card)
        
        if new_card.rank == 'A':
            self.aces += 1
    
    def show_hand(self, hidden):
        if hidden == True:
            print('Hidden card, ', end="")
            for c in self.hand_cards[1:len(self.hand_cards)-2]:
                print(c, end=", ")
            print(self.hand_cards[-1])
        else:
            for c in self.hand_cards[:len(self.hand_cards)-2]:
                print(c, end=", ")
            print(self.hand_cards[-1])
    
    def cal_value(self):
        self.value = 0
        
        for i in self.hand_cards:
            self.value += card_value[i.rank]
        
        if self.aces >0 and self.value <= 11:
            self.value += 10
            
        return self.value

    
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
    
def make_bet(players):
    for player in players:
        while True:  
            bet_tmp = input('%s, how much would you like to bet? ' % player.name)
            type(bet_tmp)
            bet_tmp
            try:
                if 0 < int(bet_tmp) <= int(player.chip):
                    bet[player.name] = int(bet_tmp)
                    break
                else:
                    print('Invalid bet! The bet amount must be between 0 and your balance.')
            except:
                print('The bet amout must be an integer!')
                
    print('\nFinished betting')
    for player in players:
        print('%s bet %d chips.' % (player.name, bet[player.name]))
        

        
def initialization():
    import random         
    global players, card_value, bet
    players = [] # initialization
    card_value = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
    bet = {}
    
    join_game(players)
    make_bet(players)

    
# test
initialization()
