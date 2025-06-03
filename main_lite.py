from library_lite import Library, User, Writer, Genre

# Initialize the library
library = Library()

# Create authors
rowling = Writer("J.K. Rowling", 55)
v_hugo = Writer("Victor Hugo", 63)
exupery = Writer("Antoine de Saint-Exupéry", 44)
moliere = Writer("Molière", 51)
stendhal = Writer("Stendhal", 67)

# Create books (automatiquement ajoutés à la bibliothèque via write)
harry_potter = rowling.write("Harry Potter", nb_pages=308, genres={Genre.FANTASY})
miserables = v_hugo.write("Les Misérables", nb_pages=1664, genres={Genre.HISTORY})
petit_prince = exupery.write("Le Petit Prince", nb_pages=120, genres={Genre.CHILDREN})
tartuffe = moliere.write("Tartuffe", nb_pages=128, genres={Genre.FICTION})
red_and_black = stendhal.write("The Red and the Black", nb_pages=608, genres={Genre.HISTORY})

# Create users
ihsane = User("Ihsane", 24)
quentin = User("Quentin", 25)
jordane = User("Jordane", 24)
emilie = User("Emilie", 25)

# Register users to the library
for user in [ihsane, quentin, jordane, emilie]:
    library.register(user)

# Users follow authors
ihsane.follow(v_hugo)
quentin.follow(rowling)
jordane.follow(exupery)
emilie.follow(stendhal)

# Consult available books
print("\nBooks available in the library:")
for title in library.consult(ihsane):
    print(f"- {title}")

# Display books with details
print("\nDetailed list of books available:")
for book, qte in library.getStock().items():
    if qte > 0:
        print(f"- {book.title} by {book.getListAuthorsName()} ({book.nb_pages} pages)")
        print(f"  {qte} copies available")

# Borrow books
ihsane.borrow("Harry Potter")
quentin.borrow("Les Misérables")
jordane.borrow("Le Petit Prince")

# Display books after borrowing
print("\nBooks available after borrowing:")
for book, qte in library.getStock().items():
    if qte > 0:
        print(f"- {book.title} by {book.getListAuthorsName()} ({book.nb_pages} pages)")
        print(f"  {qte} copies available")

# Try to borrow a book not available
emilie.borrow("Harry Potter")

# Return book
ihsane.returnBook(harry_potter)

# Display after return
print("\nBooks available after return:")
for book, qte in library.getStock().items():
    if qte > 0:
        print(f"- {book.title} by {book.getListAuthorsName()} ({book.nb_pages} pages)")
        print(f"  {qte} copies available")

# Random borrow
# print("\nIhsane borrows a random book:")
ihsane.borrowRandomBook()
