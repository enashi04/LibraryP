from colorama import init, Fore, Style
from time import sleep
from library_lite import Library, User, Writer, Genre

def pause():
    sleep(1)
    print()

init(autoreset=True)

library = Library()
ihsane = User("Ihsane", 24)
quentin = User("Quentin", 25)

library.register(ihsane)
library.register(quentin)

rowling = Writer("J.K. Rowling", 55)
v_hugo = Writer("Victor Hugo", 63)
exupery = Writer("Antoine de Saint-Exupéry", 44)
moliere = Writer("Molière", 51)
stendhal = Writer("Stendhal", 67)

harry_potter = rowling.write("Harry Potter", nb_pages=308, genres={Genre.FANTASY})
miserables = v_hugo.write("Les Misérables", nb_pages=1664, genres={Genre.HISTORY})
petit_prince = exupery.write("Le Petit Prince", nb_pages=120, genres={Genre.CHILDREN})
tartuffe = moliere.write("Tartuffe", nb_pages=128, genres={Genre.FICTION})
red_and_black = stendhal.write("The Red and the Black", nb_pages=608, genres={Genre.HISTORY})

def main():
    print(Fore.MAGENTA + Style.BRIGHT + f"\n🌟 Bienvenue dans '{library.name}' 📚\n")

    user_name = input(Fore.YELLOW + "Quel est ton nom ? ")
    age = int(input(Fore.YELLOW + "Quel est ton âge ? "))
    user = User(user_name, age)
    library.register(user)
    print(Fore.GREEN + f"Bienvenue, {user.name} ! Tu peux maintenant emprunter des livres.\n")

    while True:
        print(Fore.CYAN + f"👋 Bonjour {user.name} ! Que veux-tu faire ?")
        print(Fore.YELLOW + "1. 📚 Consulter les livres disponibles")
        print("2. 📥 Emprunter un livre")
        print("3. 📤 Rendre un livre")
        print("4. 🚪 Quitter")

        choice = input(Fore.GREEN + "👉 Ton choix : ")

        if choice == "1":
            print(Fore.BLUE + "\n📚 Livres disponibles :")
            for book, qte in library.getStock().items():
                print(f"🔹 {book.title} ({qte} exemplaire{'s' if qte > 1 else ''})")
            pause()

        elif choice == "2":
            print(Fore.BLUE + "\n📖 Quel livre veux-tu emprunter ?")
            for book in library.consult(user):
                print(f"📗 {book}")
            title = input("✍️  Titre exact : ")
            user.borrow(title)
            pause()

        elif choice == "3":
            if user.nbBorrowed()==0:
                print(Fore.YELLOW + "Tu n'as emprunté aucun livre.")
            else:
                print(Fore.BLUE + "\n📤 Quel livre veux-tu rendre ?")
                user_borrowed_books = user._User__borrowed  # accès à l'attribut privé
                for idx, book in enumerate(user_borrowed_books, 1):
                    print(f"{idx}. {book.title}")
                try:
                    idx = int(input("Numéro du livre à rendre : ")) - 1
                    if 0 <= idx < len(user_borrowed_books):
                        user.returnBook(user_borrowed_books[idx])
                        print(Fore.GREEN + "Livre rendu avec succès.")
                    else:
                        print(Fore.RED + "Numéro invalide.")
                except ValueError:
                    print(Fore.RED + "Entrée invalide.")
            pause()

        elif choice == "4":
            print(Fore.MAGENTA + "\n À bientôt dans ta librairie magique ! ✨")
            break

        else:
            print(Fore.RED + "❌ Choix invalide ! Essaie encore.")
            pause()

if __name__ == "__main__":
    main()
