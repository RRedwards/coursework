"""
Analyzing a simple dice game
"""


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length
    """
    
    ans = set([()])
    for dummy_idx in range(length):
        temp = set()
        for seq in ans:
            for item in outcomes:
                new_seq = list(seq)
                new_seq.append(item)
                temp.add(tuple(new_seq))
        ans = temp
    return ans


def max_repeats(seq):
    """
    Compute the maxium number of times that an outcome is repeated
    in a sequence
    """
    result = max(seq.count(item) for item in seq)
    return result


def count_repeats(seqs, num_to_count):
    """
    Takes set of sequences and number of repeats to look for in each sequence.
    Returns number of sequences that have exactly that number of repeats.
    """
    num_found = 0
    for seq in seqs:
        if max_repeats(seq) == num_to_count:
            num_found += 1
    return num_found


def compute_expected_value():
    """
    Function to compute expected value of simpe dice game
    """
    outcomes = set([1, 2, 3, 4, 5, 6])
    num_total_outcomes = len(outcomes) ** 3
    
    # number of outcomes resulting in doubles and triples:
    num_doubles = count_repeats(gen_all_sequences(outcomes, 3), 2)
    num_triples = count_repeats(gen_all_sequences(outcomes, 3), 3)

    expect_value = (float(num_doubles) / num_total_outcomes * 10) + \
                    (float(num_triples) / num_total_outcomes * 200)
    return expect_value


def run_test():
    """
    Testing code, note that the initial cost of playing the game
    has been subtracted
    """
    outcomes = set([1, 2, 3, 4, 5, 6])
    print "All possible sequences of three dice are"
    print gen_all_sequences(outcomes, 3)
    print
    print "Test for max repeats"
    print "Max repeat for (3, 1, 2) is", max_repeats((3, 1, 2))
    print "Max repeat for (3, 3, 2) is", max_repeats((3, 3, 2))
    print "Max repeat for (3, 3, 3) is", max_repeats((3, 3, 3))
    print
    print "Ignoring the initial $10, the expected value was $", compute_expected_value()
    
run_test()
