
"""
Name: Tri Minh Cao
Email: trimcao@gmail.com
Date: October 2015

NOTE: only works with CodeSkulptor

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
    if (len(list1) < 1):
        return []
    new_list = []
    idx_i = 0 
    idx_j = 0
    new_list.append(list1[idx_i])
    # iterate idx_j from 0 to the end of list1
    for idx_j in range(len(list1)):
        # if index idx_j contains a different entry, 
        # move idx_i to position of idx_j
        if not (list1[idx_j] == list1[idx_i]):
            idx_i = idx_j
            new_list.append(list1[idx_i])
    return new_list

# test remove_duplicates
#test = [1,1,2,2,2,2,3,3,4,4,4,5,5]
#print remove_duplicates(test)
            

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    inter = []
    # remove duplicates from list1 and list2
    #list1_no_dup = remove_duplicates(list1)
    #list2_no_dup = remove_duplicates(list2)
    # idx_i will iterate through list1
    idx_i = 0
    # idx_j will iterate through list2
    idx_j = 0
    while (idx_i < len(list1)) and (idx_j < len(list2)):
        if (list1[idx_i]) == (list2[idx_j]):
            inter.append(list1[idx_i])
            idx_i += 1
            idx_j += 1
        elif (list1[idx_i] < list2[idx_j]):
            idx_i += 1
        else:
            idx_j += 1
        
    return inter

# test intersection
#test1 = [9, 10]
#test2 = [4,5,6,7,8,9,10]
#print intersect(test1, test2)

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    merged = []
    idx_i = 0
    idx_j = 0
    
    while ((idx_i < len(list1)) and (idx_j < len(list2))):
        if (list1[idx_i] <= list2[idx_j]):
            merged.append(list1[idx_i])
            idx_i += 1
        else:
            merged.append(list2[idx_j])
            idx_j += 1

    if (idx_i >= len(list1)):
        #print idx_j
        if (idx_j < len(list2)):
            merged.extend(list2[idx_j:])
    else:
        merged.extend(list1[idx_i:])
            
    return merged

# test merge:
#list1 = [1,2,3]
#list2 = [2,2,2]
#print merge(list1, list2)
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if (len(list1) <= 1):
        return list1
    else:
        mid = len(list1) // 2
        left = merge_sort(list1[:mid])
        right = merge_sort(list1[mid:])
        return merge(left, right)
       
# test merge_sort
#list1 = [9,8,7,6]
#print merge_sort(list1)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if (len(word) == 0):
        return ['']
    elif (len(word) == 1):
        lst = ['']
        lst.append(word)
        return lst
    else:
        # how to call with empty string
        strings_list = gen_all_strings(word[1:])
        final_list = []
        final_list.extend(strings_list)
        # add the first letter to all strings in the strings_list
        first_letter = word[0]
        for each_string in strings_list:
            for idx in range(len(each_string) + 1):
                each_string_lst = list(each_string)
                each_string_lst.insert(idx, first_letter)
                new_string = ''.join(each_string_lst)
                final_list.append(new_string)        
        return final_list
    
# test gen_all_strings:
#test = "ab"
#print gen_all_strings(test)

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    words = []
    for line in netfile.readlines():
        words.append(line[:-1])
    return words    

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    
    

