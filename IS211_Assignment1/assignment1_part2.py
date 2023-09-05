
class Book:
    def __init__(self, author="", title=""):
        self.author = author # Is the author
        self.title = title # Is the title

    def display(self):
        print(f"{self.title}, written by {self.author}")
        # Print title, author

if __name__ == "__main__":
    Youre_a_wizard_harry = Book("J. K. Rowling", "Harry Potter and the Goblet of Fire")
    Youre_a_wizard_harry.display() 
    Knights_live_for_glory = Book("Walter Scott.", "Ivanhoe: A Romance")
    Knights_live_for_glory.display() 