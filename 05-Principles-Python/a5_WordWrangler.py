"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    if len(list1) < 2:
        return list1
    cur_idx = 0
    while cur_idx < len(list1) - 1:
        if list1[cur_idx] == list1[cur_idx + 1]:
            list1.pop(cur_idx + 1)
        else:
            cur_idx += 1
    return list1


def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    if (list1 == []) or (list2 == []):
        return []
    newlist = []
    l1_idx = 0
    l2_idx = 0
    while (l1_idx < len(list1)) and (l2_idx < len(list2)):
        l1_val = list1[l1_idx]
        l2_val = list2[l2_idx]
        if l1_val == l2_val:
            newlist.append(l1_val)
            l1_idx += 1
            l2_idx += 1
        elif l1_val < l2_val:
            l1_idx += 1
        else:
            l2_idx += 1
    return newlist


# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in both list1 and list2.

    This function can be iterative.
    """
    newlist = []
    l1_copy = list(list1)
    l2_copy = list(list2)
    while (len(l1_copy) > 0) and (len(l2_copy) > 0):
        if l1_copy[0] < l2_copy[0]:
            newlist.append(l1_copy[0])
            l1_copy.pop(0)
        else:
            newlist.append(l2_copy[0])
            l2_copy.pop(0)
    if len(l1_copy) > 0:
        newlist = newlist + l1_copy
    if len(l2_copy) > 0:
        newlist = newlist + l2_copy
    return newlist
             
    
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """     
    if len(list1) < 2:
        return list1
    else:
        mid = len(list1) / 2
        return merge(merge_sort(list1[:mid]), merge_sort(list1[mid:]))


# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if word == "":
        return [""]
    else:
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        new_strings = []
        for string in rest_strings:
            for pos in range(len(string) + 1):
                list_copy = list(string)
                list_copy.insert(pos, first)
                new_str = "".join(list_copy)
                new_strings.append(new_str)
        return new_strings + rest_strings


# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    str_list = []
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    for word in netfile.readlines():
        str_list.append(word.strip())
    return str_list

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# see snippet of file to check it loads correctly:
#words = load_words(WORDFILE)
#for word in words[10000 : 10010]:
#    print word
    
# Uncomment when you are ready to try the game
run()

    