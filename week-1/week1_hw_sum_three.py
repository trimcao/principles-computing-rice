def appendsums(lst):
    """
    Repeatedly append the sum of the current last three elements of lst to lst.
    """
    length = len(lst)
    total = lst[length - 1] + lst[length - 2] + lst[length - 3] 
    lst.append(total)
 
sum_three = [0, 1, 2]
for i in range(0, 26):
    appendsums(sum_three)

print sum_three[10]    
print sum_three[20]
