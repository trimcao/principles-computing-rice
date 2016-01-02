# Name: Tri Minh Cao
# Email: trimcao@gmail.com
# Date: Aug 30, 2015

"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # replace with your code
    new_line = []
    zeroes_count = 0
    for i in range(0, len(line)):
        if (line[i] == 0):
            zeroes_count += 1
        else:
            new_line.append(line[i])
    for i in range(0, zeroes_count):
        new_line.append(0)
        
    move(new_line)    
    merge_helper(new_line)
    move(new_line)
    return new_line

def move(line):
    """
    Function that moves all the blocks to the left
    """
    step_count = 0
    for i in range(0, len(line)):
        while(line[i] == 0) and (step_count < len(line)):
            del line[i]
            line.append(0)
            step_count += 1
            
def merge_helper(line):
    """
    Helper method for merge.
    """
    for i in range(0, len(line) - 1):
        if (line[i] == line[i+1]):
            if line[i] == 0:
                break
            else:
                line[i] = 2 * line[i]
                line[i + 1] = 0
        
    return line

"""
test = [8, 16, 16, 8]
print merge(test)
"""
"""
[2, 0, 2, 4] should return [4, 4, 0, 0]
[0, 0, 2, 2] should return [4, 0, 0, 0]
[2, 2, 0, 0] should return [4, 0, 0, 0]
[2, 2, 2, 2, 2] should return [4, 4, 2, 0, 0]
[8, 16, 16, 8] should return [8, 32, 8, 0]
"""
"""
test = [2,2,2,2,2]
print test
merge_helper(test)
print test
move(test)
print test
"""
