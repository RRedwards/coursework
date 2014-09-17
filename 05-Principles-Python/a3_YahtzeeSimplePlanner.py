"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

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
    max_score = 0
    for item in hand:
        item_score = item * hand.count(item)
        if item_score > max_score:
            max_score = item_score
    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcome_list = [num + 1 for num in range(num_die_sides)]
    seq_set = gen_all_sequences(outcome_list, num_free_dice)
    sum_values = 0.0
    for item in seq_set:
        sum_values += score(list(held_dice) + list(item))
    expect_val = float(sum_values) / len(seq_set)
    return expect_val


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    
    if hand == ():
        return set([()])
    else:
        first = hand[0]
        rest = hand[1:]
        rest_hand = gen_all_holds(rest)
        new_hand = []
        for tup in rest_hand:
            new_tuple = tuple([first]) + tup
            new_hand.append(new_tuple)
        list_rest_hand = list(rest_hand)
        new_list = new_hand + list_rest_hand
        return set(new_list)


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    max_score = 0.0
    hold_dice = ()
    holds_set = gen_all_holds(hand)
    for holds in holds_set:
        num_free_dice = len(hand) - len(holds)
        cur_value = expected_value(holds, num_die_sides, num_free_dice)
        if cur_value > max_score:
            max_score = cur_value
            hold_dice = holds
    return (max_score, hold_dice)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
#    hand = (1, 1, 1, 5, 6)
    hand = (4, 1, 4, 6, 4)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
# QUICK TESTS: ------------------------------

#print score([1, 1, 1, 1, 6])
#print score([2, 2, 2, 4, 4])
#print gen_all_sequences([1, 2], 2)
#print expected_value([1, 1, 1], 2, 2)
print gen_all_holds((1, 2, 2))
print gen_all_holds((2, 1, 2))


