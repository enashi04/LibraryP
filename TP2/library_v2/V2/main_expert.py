from library_expert import Library, Writer, User, Genre

# Création des écrivains
rowling = Writer("J.K. Rowling", 55)
v_hugo = Writer("Victor Hugo", 63)
exupery = Writer("Antoine de Saint-Exupéry", 44)
moliere = Writer("Molière", 51)
stendhal = Writer("Stendhal", 67)

# Création des livres via les événements des écrivains
rowling.createEvent("Harry Potter")
v_hugo.createEvent("Les Misérables")
exupery.createEvent("Le Petit Prince")
moliere.createEvent("Tartuffe")
stendhal.createEvent("The Red and the Black")

# Création des utilisateurs
alice = User("Alice", 30)
bob = User("Bob", 25)
charlie = User("Charlie", 35)

the_library = Library()

# Enregistrement des utilisateurs
the_library.register(alice)
the_library.register(bob)
the_library.register(charlie)

# Suivre les écrivains
the_library.follow(rowling)
the_library.follow(v_hugo)
the_library.follow(exupery)
the_library.follow(moliere)
the_library.follow(stendhal)

# Désenregistrer un utilisateur
the_library.unregister(charlie)

# Consultation des livres disponibles
print(f"Books available for {alice.name}: {the_library.consult(alice)}")
print(f"Books available for {bob.name}: {the_library.consult(bob)}")

# Emprunt de livres
the_library.borrowBook("Harry Potter", alice)
the_library.borrowBook("Les Misérables", bob)

# Retour d'un livre
the_library.returnBook("Harry Potter")

# Consultation après retour
print(f"Books available for {alice.name}: {the_library.consult(alice)}")
print(f"Books available for {bob.name}: {the_library.consult(bob)}")
