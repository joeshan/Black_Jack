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
    
    def __str__(self):
        return '%d decks shuffled together. %d cards left.' % (self.deck_num, len(self.card_pool)) 

    def shuffle(self):
        for i in decks.suits:
            for j in decks.ranks:
                self.card_pool.append(card(i,j))
        self.card_pool *= self.deck_num
        random.shuffle(self.card_pool)
        
    def deal(self):
        return self.card_pool.pop()


class hand:
    def __init__(self):
        self.hand_cards = []
        self.value = 0
        self.aces = 0
        self.blackjack = 0
        self.bust = 0
        self.play_flag = 1
    
    def add_card(self, new_card):
        self.hand_cards.append(new_card)
    
    def show_hand(self, hidden=False):
        if hidden == True:
            print('Hidden card', end=', ')
            for c in self.hand_cards[1:(len(self.hand_cards)-1)]:
                print(c, end = ', ')
            print(self.hand_cards[-1])
        else:
            for c in self.hand_cards[:(len(self.hand_cards)-1)]:
                print(c, end = ', ')
            print(self.hand_cards[-1])
    
    def cal_value(self):
        self.value = 0
        
        for card in self.hand_cards:
            if card.rank == 'A':
                self.aces += 1
        
        for i in self.hand_cards:
            self.value += card_value[i.rank]
        
        if self.aces >0 and self.value <= 11:
            self.value += 10
        
        if self.aces >0 and self.value == 21 and len(self.hand_cards) == 2:
            self.blackjack = 1
            self.play_flag = 0
            print('Black Jack!')
        
        if self.value > 21:
            self.bust = 1
            self.play_flag = 0
            print('Bust!')
            
        if self.value == 21:
            self.play_flag = 0
            print('The value is 21 now!')
        
        return self.value
    
    
class player:
    def __init__(self, name, chip):
        self.name = name
        self.chip = chip
        self.hand = hand()
        self.dealer_flag = 0
        
    def __str__(self):
        return 'Play %s has %s chips.' % (self.name, str(self.chip))
    
    
def join_game(players):
    join = True
    while len(players)<6 and join == True:
        name_tmp = str(input("Player's name:"))
        chip_tmp = str(input('Chips that %s has:' % name_tmp))
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
            try:
                if 0 < int(bet_tmp) <= int(player.chip):
                    bet[player] = int(bet_tmp)
                    player.chip = int(player.chip) - bet[player]
                    break
                else:
                    print('Bet from 1 to %d!' % int(player.chip))
            except:
                print('Bet a positive integer!')
                
    print('\nFinished betting')
    for player in players:
        print('%s bet %d chips.' % (player.name, bet[player]))
        

def deal_to_player(player, deck, hidden=False):
    new_card = deck.deal()
    player.hand.add_card(new_card)
    if hidden == False:
        print(new_card, end=' ') 
        print('is dealed to %s.' % (player.name))
    else:
        print('A card is dealed to %s.' % (player.name))
    

def adjust_chips(player, bet, win_flag):
    if win_flag == 1:
        print('\n%s won %d chips!' % (player.name, bet[player]))
        player.chip = int(player.chip) + bet[player]*2
    elif win_flag == -1:
        print('\n%s lost %d chips!' % (player.name, bet[player]))
    else:
        print('\nPush!')
        player.chip = int(player.chip) + bet[player]

        
def check_win(dealer, player): # check who wins if no bust
    global bet
    dealer_value = dealer.hand.cal_value()
    player_value = player.hand.cal_value()
    
    print("\nDealer's hand: ", end="")
    dealer.hand.show_hand()
    print("Value of dealer's hand: %d" % dealer_value)
    
    print("\n%s's hand: " % player.name, end="")
    player.hand.show_hand()
    print("Value of %s's hand: %d" % (player.name,player_value))
    
    if dealer.hand.aces == player.hand.aces == 0:
        if dealer_value > player_value:
            win_flags[player] = -1
            adjust_chips(player, bet, win_flags[player])
        elif dealer_value < player_value:
            win_flags[player] = 1
            adjust_chips(player, bet, win_flags[player])
        else:
            win_flags[player] = 0
            adjust_chips(player, bet, win_flags[player])            
    else:
        if dealer_value > player_value:
            win_flags[player] = -1
            adjust_chips(player, bet, win_flags[player])
        elif dealer_value < player_value:
            win_flags[player] = 1
            adjust_chips(player, bet, win_flags[player])
        else:
            if dealer_value == player_value == 21:
                if player.hand.blackjack > dealer.hand.blackjack:
                    win_flags[player] = 1
                    adjust_chips(player, bet, win_flags[player])
                elif player.hand.blackjack < dealer.hand.blackjack:
                    win_flags[player] = -1
                    adjust_chips(player, bet, win_flags[player])
                else:
                    win_flags[player] = 0
                    adjust_chips(player, bet, win_flags[player])
            else:
                win_flags[player] = 0
                adjust_chips(player, bet, win_flags[player])
            

def decision(player):
    while player.hand.play_flag == 1:
        if player.dealer_flag == 0:
            print("Dealer's hand: ", end="")
            dealer.hand.show_hand(hidden=True)
            
            print("%s's hand: " % player.name, end="")
            player.hand.show_hand()
            player.hand.cal_value()
            print("Value of %s's hand: %d" % (player.name,player.hand.value))
            
            option = input('%s, do you want to stand or hit? (S-stand/H-hit): ' % player.name)
            
            if str(option)[0].upper() in ['S', 'H']:
                if str(option)[0].upper() == 'H':
                    deal_to_player(player,deck)
                    print('\n')
                    player.hand.cal_value()
                elif str(option)[0].upper() == 'S':
                    player.hand.play_flag = 0
                    break      
            else:
                print('The input should only be S or H.')
                continue
        elif player.dealer_flag == 1:
            if player.hand.value < 17:
                deal_to_player(player,deck)
                player.hand.cal_value()
            else:
                player.hand.play_flag = 0
                break       

        
def initialization():       
    global players, card_value, bet, dealer, win_flags, next_round, restart, deck
    
    players = [] # initialization
    card_value = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
    bet = {}
    win_flags = {}
    next_round = 'Y'
    restart = 'N'
    
    join_game(players)
    dealer = player('Dealer LuckyMan', 9999)
    dealer.dealer_flag = 1
    
    while True:
        try:
            deck_num = input('How many decks do you want to use? ')
            deck = decks(int(deck_num))
            break
        except:
            continue
    

def game_steps():
    global players, next_round, deck, restart, deck, dealer
    
    for player in players:
        player.hand = hand()
    dealer.hand = hand()
    deck.shuffle()
    print('\nCards shuffled.\n')
    
    make_bet(players)
    print('\n')
    
    # initial deal
    for player in players:
        deal_to_player(player, deck, hidden=False)
        deal_to_player(player, deck, hidden=False)
        print('\n')
        
    deal_to_player(dealer, deck, hidden=True)
    deal_to_player(dealer, deck, hidden=False)
    print('\n')
    
    # round of players
    for player in players:
        decision(player)
        print('\n')
        
    # round of dealer    
    decision(dealer)
    print('\n')
        
    # check win or lose 
    for player in players: 
        if dealer.hand.bust == 1:
            if player.hand.bust == 1:
                win_flags[player] = -1
                adjust_chips(player, bet, win_flags[player])
            else:
                win_flags[player] = 1
                adjust_chips(player, bet, win_flags[player])
        else:
            if player.hand.bust == 1:
                win_flags[player] = -1
                adjust_chips(player, bet, win_flags[player])
            else:
                check_win(dealer, player)
        
        print('%s, now you have %d chips.' % (player.name, player.chip))
        
        if int(player.chip) <= 0: 
            print('%s lost all chips. Time to leave now.' % player.name)
            players.remove(player)
        else:         
            next_round = input('%s, Do you want to play another round? (Y-another round, N-quit, ): ' % player.name)
            if str(next_round)[0].upper() == 'N':
                players.remove(player)
    
#####################                   
#### game starts ####
#####################
import random  
initialization()

while True:
    if len(player) == 0:
        break
    
    if str(restart)[0].upper() == 'Y':
        initialization()
        
    game_steps()
    
    # check if quit            
    quit = input('Do you want to quit the game? (Y/N): ')
    if str(quit)[0].upper() == 'Y':
        break
        
    # check if restart            
    restart = input('Do you want to restart the game? (Y/N): ')

