from Library import Library, Book, Author, Person, Genre

# # List of books
# harry_potter = Book("Harry Potter", Author("J.K. Rowling", 55), 1997, Genre.FANTASY)
# miserables = Book("Les Misérables", Author("Victor Hugo", 63), 1862, Genre.HISTORY)
# petit_prince = Book("Le Petit Prince", Author("Antoine de Saint-Exupéry", 44), 1943, Genre.CHILDREN)
# bourgeois = Book("Le bourgeois gentilhomme", Author("Molière", 51), 1670, Genre.FICTION)
# rouge_noir = Book("Le Rouge et le Noir", Author("Stendhal", 67), 1830, Genre.ROMANCE)
# monte_cristo = Book("Le Comte de Monte-Cristo", Author("Alexandre Dumas", 61), 1844, Genre.ADVENTURE)

# Auteur écrivent des livres
harry_potter = Author("J.K. Rowling", 55).write_book("Harry Potter", 1997, Genre.FANTASY)
miserables = Author("Victor Hugo", 63).write_book("Les Misérables", 1862, Genre.HISTORY)
petit_prince=Author("Antoine de Saint-Exupéry", 44).write_book("Le Petit Prince", 1943, Genre.CHILDREN)
bourgeois=Author("Molière", 51).write_book("Le bourgeois gentilhomme", 1670, Genre.FICTION)
rouge_noir=Author("Stendhal", 67).write_book("Le Rouge et le Noir", 1830, Genre.ROMANCE)
monte_cristo= Author("Alexandre Dumas", 61).write_book("Le Comte de Monte-Cristo", 1844, Genre.ADVENTURE)

# List of person
alice = Person("Alice", 30)
bob = Person("Bob", 25)
charlie = Person("Charlie", 35)

# Create library 
library = Library()
#Add books and users to the library
library.add_book(harry_potter)
library.add_book(miserables)
library.add_book(petit_prince)
library.add_book(bourgeois)
library.add_book(rouge_noir)
library.add_book(monte_cristo)

library.add_user(alice)
library.add_user(bob)
library.add_user(charlie)

#display books and users signed up in the library
library.books_available()
print("\n")
library.users_registered()

#greet users
print(alice.greet())
print(bob.greet())
print(charlie.greet(),"\n")

#borrow books
library.borrow_book(alice, harry_potter)
library.borrow_book(bob, miserables)
library.borrow_book(charlie, petit_prince)

# display books available in the library
library.books_available()

#alice returns the book
library.return_book(alice, harry_potter)
library.books_available()
library.borrow_book(alice, miserables) #not possible because bob has it 
library.borrow_book(alice, petit_prince) #not possible because charlie has it

#display the number of books read by Alice
alice.number_of_books_read()
books_alice=alice.has_read_book(miserables)
print(f"Alice has read {miserables.title} : {books_alice} and she has read {alice.number_of_books_read()} books in total")

# Display the books written by each author
print("\n\nBooks written by each author:\n")
print(f"{harry_potter.author.name} has written: {[book.title for book in harry_potter.author.books_written]}")
print(f"{miserables.author.name} has written: {[book.title for book in miserables.author.books_written]}")
print(f"{petit_prince.author.name} has written: {[book.title for book in petit_prince.author.books_written]}")
print(f"{bourgeois.author.name} has written: {[book.title for book in bourgeois.author.books_written]}")
print(f"{rouge_noir.author.name} has written: {[book.title for book in rouge_noir.author.books_written]}")

#alice choose a random book to read
print(f"Alice choose : {library.choose_random_book(alice)}")

#alice wants to borrow a book that is not available
library.borrow_book(alice, miserables) #not possible because Stendhal has it


# Bob returns "Les Misérables"
library.return_book(bob,miserables)  # This will notify Alice that the book is now available

