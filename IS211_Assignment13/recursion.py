
import unittest

def fibonacci(n):
    """Recursively calculates the nth Fibonacci number."""
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

def gcd(a, b):
    """Recursively finds the greatest common divisor (GCD) of a and b using Euclid's algorithm."""
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def compareTo(s1, s2):
    """Recursively compares two strings."""
    if not s1 and not s2:
        return 0
    elif not s1:
        return -ord(s2[0])
    elif not s2:
        return ord(s1[0])
    elif s1[0] != s2[0]:
        return ord(s1[0]) - ord(s2[0])
    else:
        return compareTo(s1[1:], s2[1:])

class TestRecursionMethods(unittest.TestCase):

    def test_fibonacci(self):
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)
        self.assertEqual(fibonacci(5), 5)
        self.assertEqual(fibonacci(10), 55)

    def test_gcd(self):
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(gcd(54, 24), 6)
        self.assertEqual(gcd(20, 8), 4)
        self.assertEqual(gcd(17, 13), 1)

    def test_compareTo(self):
        self.assertEqual(compareTo("apple", "apple"), 0)
        self.assertEqual(compareTo("apple", "banana"), -1)
        self.assertEqual(compareTo("banana", "apple"), 1)
        self.assertEqual(compareTo("", "apple"), -ord("a"))
        self.assertEqual(compareTo("apple", ""), ord("a"))
        self.assertEqual(compareTo("", ""), 0)
        
if __name__ == '__main__':
    unittest.main()
    