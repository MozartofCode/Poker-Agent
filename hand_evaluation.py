# @Author: Bertan Berker
# @Language: Python
# 


# Hand also includes the cards on the table (total 7 cards)

# player1 - hand
# player2 - hand
def choose_winner(player1, player2):

    result1 = evaluate_hand(player1)
    result2 = evaluate_hand(player2)

    rankings = ["High Card", "Pair", "Two Pairs", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush", "Royal Flush"]
    
    if rankings.index(result1) > rankings.index(result2):
        return True
    
    elif rankings.index(result1) < rankings.index(result2):
        return False
    
    else:
        #TODO: Implement tie breaker for the future
        # Any tie goes to player 1 for now
        return tie_breaker()
    




def evaluate_hand(hand):

    if is_royal_flush(hand):
        return "Royal Flush"
    
    elif is_straight_flush(hand):
        return "Straight Flush"
    
    elif is_four_of_a_kind(hand):
        return "Four of a Kind"
    
    elif is_full_house(hand):
        return "Full House"
    
    elif is_flush(hand):
        return "Flush"
    
    elif is_straight(hand):
        return "Straight"
    
    elif is_three_of_a_kind(hand):
        return "Three of a Kind"
    
    elif is_two_pairs(hand):
        return "Two Pairs"
    
    elif is_pair(hand):
        return "Pair"
    
    else:
        return "High Card"



def tie_breaker():
    return True


def is_royal_flush(hand):

    if not is_straight_flush(hand):
        return False

    values = []

    for card in hand:
        values.append(card.get_value())
    
    values.sort()

    # There are 7 cards = 2 hand + 5 table
    return values[2] == 10 and values[-1] == 14


def is_straight_flush(hand):
    return is_straight(hand) and is_flush(hand)


def is_four_of_a_kind(hand):

    values = {}

    if not is_three_of_a_kind(hand):
        return False

    for card in hand:
        if card.get_value() in values:
            values[card.get_value()] += 1
        else:
            values[card.get_value()] = 1
    
    for value in values:
        if values[value] >= 4:
            return True
    
    return False



def is_full_house(hand):
    
    values = {}

    if not is_three_of_a_kind(hand):
        return False

    for card in hand:
        if card.get_value() in values:
            values[card.get_value()] += 1
        else:
            values[card.get_value()] = 1
    
    three_of_a_kind = False
    pair = False

    for value in values:
        if values[value] >= 3:
            three_of_a_kind = True
        elif values[value] >= 2:
            pair = True
    
    return three_of_a_kind and pair


def is_flush(hand):

    suits = {}
    
    for card in hand:
        if card.get_suit() in suits:
            suits[card.get_suit()] += 1
        else:
            suits[card.get_suit()] = 1
    
    for suit in suits:
        if suits[suit] == 5:
            return True
        
    return False


def is_straight(hand):
    
    values = []
    
    for card in hand:
        values.append(card.get_value())
    
    values.sort()

    sequence_count = 0
    
    for i in range(1, len(values)):
        if values[i] == values[i-1] + 1:
            sequence_count += 1
        
    return sequence_count >= 5


def is_three_of_a_kind(hand):

    values = {}

    if not is_pair(hand):
        return False

    for card in hand:
        if card.get_value() in values:
            values[card.get_value()] += 1
        else:
            values[card.get_value()] = 1
    
    for value in values:
        if values[value] >= 3:
            return True
    
    return False



def is_two_pairs(hand):

    if not is_pair(hand):
        return False
    
    values = {}

    for card in hand:
        if card.get_value() in values:
            values[card.get_value()] += 1
        else:
            values[card.get_value()] = 1
    
    # Check if there are two pairs
    pair_count = 0

    for value in values:    
        if values[value] >= 2:
            pair_count += 1
    
    return pair_count >= 2



def is_pair(hand):

    values = set()
    
    for card in hand:
        if card.get_value() in values:
            return True
        
        values.add(card.get_value())

    return False

    