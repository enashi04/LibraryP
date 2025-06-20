from library_advanced import Library, Writer, User, Genre

rowling = Writer("J.K. Rowling", 55)
v_hugo = Writer("Victor Hugo", 63)
exupery = Writer("Antoine de Saint-Exupéry", 44)
moliere = Writer("Molière", 51)
stendhal = Writer("Stendhal", 67)

harry_potter = rowling.write("Harry Potter", genres={Genre.FANTASY})
miserables = v_hugo.write("Les Misérables", genres={Genre.HISTORY})
petit_prince = exupery.write("Le Petit Prince", genres={Genre.CHILDREN})
tartuffe = moliere.write("Tartuffe", genres={Genre.FICTION})
red_and_black = stendhal.write("The Red and the Black", genres={Genre.HISTORY})

alice = User("Alice", 30)
bob = User("Bob", 25)
charlie = User("Charlie", 35)

library = Library()

library.register(alice)
library.register(bob)
library.register(charlie)

print(library)

library.follow(rowling)
library.follow(v_hugo)
library.follow(exupery)
library.follow(moliere)
library.follow(stendhal)

library.notice(harry_potter, rowling)
library.notice(miserables, v_hugo)
library.notice(petit_prince, exupery)
library.notice(tartuffe, moliere)
library.notice(red_and_black, stendhal)

library.unregister(charlie)

print(library)

print(f"Books available for {alice.name}: {library.consult(alice)}")
print(f"Books available for {bob.name}: {library.consult(bob)}")

borrowed_harry_potter = library.borrow("Harry Potter", alice)
borrowed_miserables = library.borrow("Les Misérables", bob)

print(f"{alice.name} borrowed: {borrowed_harry_potter}")
print(f"{bob.name} borrowed: {borrowed_miserables}")

library.returnBook(borrowed_harry_potter)

print(library)

print(f"Books available for {alice.name}: {library.consult(alice)}")
print(f"Books available for {bob.name}: {library.consult(bob)}")


alice.listenWriter(rowling, library)
bob.listenWriter(v_hugo, library)

alice.borrowWithProbability(harry_potter, library, 0.7)

bob.borrowWithProbability(miserables, library, 0.5)

library.returnBook(harry_potter)
library.notifyAvailability(harry_potter)

print(library)