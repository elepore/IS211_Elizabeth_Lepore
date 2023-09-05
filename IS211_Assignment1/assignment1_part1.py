
# Note: underscores added to name, different from https://github.com/cubanquant/IS211_Assignment1/blob/master/assignment1_part1.py
def list_divide(numbers, divide=2):
    """
    The function returns the number of elements in the numbers list that are divisible by divide
    """
    return len([x for x in numbers if x % divide == 0])
    # List comprehension, for numbers in number goes through each number (x), 
    # if number (x) % divided == 0, it means it's divisble. This list comprehension will 
    # make a new list of those that are divisible, then we use len() to count.  

class ListDivideException(Exception):
    pass


def test_list_divide():
    """
    Test list_divide
    """
    try:
        assert list_divide([1,2,3,4,5]) == 2
    except AssertionError:
        raise ListDivideException("Test Failed") 
        # Wasn't sure if you wanted us to incorporate the exception 
    
    try:
        assert list_divide([2,4,6,8,10]) == 5
    except AssertionError:
        raise ListDivideException("Test Failed")
    
    try:
        assert list_divide([30, 54, 63,98, 100], divide=10) == 2
    except AssertionError:
        raise ListDivideException("Test Failed")
    
    try:
        assert list_divide([]) == 0
    except AssertionError:
        raise ListDivideException("Test Failed")
    
    try:
        assert list_divide([1,2,3,4,5], 1) == 5
    except AssertionError:
        raise ListDivideException("Test Failed")

if __name__ == "__main__":
    test_list_divide()

