"""
Tri Minh Cao
trimcao@gmail.com
September 2015

Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""
#NUM_DICES = 5 # NUM_DICES depend on the hand given in strategy method

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    best = 0
    temp = 0
    for idx in range(len(hand)):
        if (idx - 1) in range(len(hand)):
            if (hand[idx] != hand[idx - 1]):
                temp = 0
        temp += hand[idx]
        if (temp > best):
            best = temp
    return best


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    total = 0
    outcomes = [dummy_idx for dummy_idx in range(1, num_die_sides + 1)]
    dice_rolls = gen_all_sequences(tuple(outcomes), num_free_dice)
    for each in dice_rolls:
        new_hand = held_dice + each
        #print new_hand
        new_hand = tuple(sorted(new_hand))
        #print new_hand
        #print score(new_hand)
        total += score(new_hand)    
        
    num_hands = len(dice_rolls)
    #print num_hands
    expected = float(total) / num_hands
    return expected  

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    hand = tuple(sorted(hand)) # make sure hand is sorted
    final_set = set([()])
    for idx in range(len(hand)):
        # use temp_set to keep the final_set stable
        temp_set = set()
        # process each hold in the final set 
        # add the current dice to each of the partial hold
        for partial_hold in final_set:
            new_hold = list(partial_hold)
            new_hold.append(hand[idx])
            temp_set.add(tuple(new_hold))
        final_set = final_set.union(temp_set)
    return final_set

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    possible_holds = gen_all_holds(hand)
    #print possible_holds
    optimum = 0
    best_hold = ()
    for each in possible_holds:
        expected = expected_value(each, num_die_sides, len(hand) - len(each))
        if (expected > optimum):
            optimum = expected
            best_hold = each
    return (optimum, best_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1,)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)

#test_hand = (1,2,3,3,3)
#print score(test_hand)

#held = (1,2,3)
#sorted(held)
#print held
#expected = expected_value(held, 6, 1)
#print expected
                                       
#outcomes = [idx for idx in range(1, 6 + 1)]
#print outcomes
    
#test_hand = (2, 3, 3)
#print gen_all_holds(test_hand)


#test_hand = (1,)
#print strategy(test_hand, 6)
#print score((3,3,3))
#a = set()
#print len(a)
#outcomes = [dummy_idx for dummy_idx in range(1, 6 + 1)]
#b = gen_all_sequences(outcomes, 5)
#print len(b)
#print expected_value((2, 2), 6, 1)
#print expected_value((2, 4), 6, 3)
#print expected_value((5, 5), 6, 4)
