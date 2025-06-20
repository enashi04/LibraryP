# -*- coding: utf-8 -*-
# For the books, make a library with a list of books and users (use inheritance and composition)
from __future__ import annotations
from enum import Enum
import random

# Genre Enum
class Genre(Enum):
    FICTION = "Fiction"
    NON_FICTION = "Non-Fiction"
    MYSTERY = "Mystery"
    FANTASY = "Fantasy"
    SCIFI = "Science Fiction"
    BIOGRAPHY = "Biography"
    HISTORY = "History"
    ROMANCE = "Romance"
    THRILLER = "Thriller"
    CHILDREN = "Children"
    ADVENTURE = "Adventure"

# Observer pattern
class Observer:
    def update(self, book: Book):
        raise NotImplementedError("implement update")
class Subject:
    def __init__(self):
        self.observers = {}  

    def add_observer(self, book: Book, observer: Observer):
        if book not in self.observers:
            self.observers[book] = []  # Initialiser une liste pour ce livre
        if observer not in self.observers[book]:
            self.observers[book].append(observer)

    def remove_observer(self, book: Book, observer: Observer):
        if book in self.observers and observer in self.observers[book]:
            self.observers[book].remove(observer)

    def notify_observers(self, book: Book):
        if book in self.observers:
            for observer in self.observers[book]:
                observer.update(book)
# Person class
class Person(Observer):
    def __init__(self, name: str, age: int):
        super().__init__()
        self.name = name
        self.age = age
        # hashmap of books read
        self.books_read = {}

    def greet(self):
        return f"Hello, my name is {self.name}"

    def read_book(self, book: Book):
        print(f"{self.name} is reading {book.title} by {book.author.name}.")
        self.books_read[book] = self.books_read.get(book, 0) + 1

    def number_of_books_read(self) -> int:
        return sum(self.books_read.values())

    def has_read_book(self, book: Book) -> bool:
        return book in self.books_read

    def read_genre(self, genre: Genre) -> list[Book]:
        return [book for book in self.books_read if book.genre == genre]
    
    def update(self, book: Book):
        print(f"Notification for {self.name}: '{book.title}' is now available!")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Person):
            return NotImplemented
        return self.name == other.name and self.age == other.age

# Author class
class Author(Person):  # Factory pattern 
    def __init__(self, name: str, age: int):
        super().__init__(name, age)
        self.books_written = []

    def write_book(self, title: str, year: int, genre: Genre) -> Book:
        book = Book(title, self, year, genre)
        if book not in self.books_written:
            self.books_written.append(book)
        return book

    def __repr__(self):
        return f"{self.name} (Author)"
    

# Book class
class Book:
    def __init__(self, title: str, author: Author, year: int, genre: Genre):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
       
        if self not in author.books_written:
            author.books_written.append(self)

    def __repr__(self):
        return f"'{self.title}' by {self.author.name} ({self.year}) - {self.genre.value}"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        return self.title == other.title
    
    def __hash__(self):
        return hash(self.title)

# Library class
class Library(Subject):
    def __init__(self):
        super().__init__()
        self.books = {} 
        self.users = []  
        self.list_wait = {}  

    def add_book(self, book: Book):
        self.books[book] = self.books.get(book, 0) + 1  

    def add_user(self, user: Person):
        self.users.append(user)

    def books_available(self):
        print("Books available in the library:")
        for book, count in self.books.items():
            print(f" - {book} ({count} items available)") 

    def users_registered(self):
        print("Registered users:")
        for user in self.users:
            print(f" - {user.name}, {user.age} years old")
    
    def unregister_user(self, user: Person):
        if user in self.users:
            self.users.remove(user)
            print(f"{user.name} has been unregistered from the library.")
        else:
            print(f"{user.name} is not registered in the library.")

    def borrow_book(self, user: Person, book: Book):
        if book in self.books and self.books[book] > 0:
            self.books[book] -= 1 
            if self.books[book] == 0:
                del self.books[book]  
            user.read_book(book)
            print(f"{user.name} borrowed '{book.title}'")
        else:
            print(f"Sorry, '{book.title}' is not available in the library.")
            self.waiting_list(book, user) 

    def return_book(self, user: Person, book: Book):
        if book in user.books_read:
            self.books[book] = self.books.get(book, 0) + 1
            print(f"{user.name} returned '{book.title}'")
            self.notify_observers(book)  #notification observer
        else:
            print(f"{user.name} has not borrowed '{book.title}'")

    def display_book_availability(self):
        print("Available books:")
        for book, count in self.books.items():
            if count > 0:
                print(f" - {book.title} by {book.author.name} ({count} items available)")

    def choose_random_book(self, user: Person)->Book :
        random_book = random.choice(list(self.books.keys()))
        print(f"{user.name} has chosen '{random_book.title}' by {random_book.author.name}")
        return random_book
    
    def waiting_list(self, book: Book, user: Person):
        if book not in self.list_wait:
            self.list_wait[book] = []

        if user not in self.list_wait[book]:
            self.list_wait[book].append(user)
            self.add_observer(book, user)  # Ajouter l'utilisateur comme observateur pour ce livre
            print(f"{user.name} has been added to the waiting list for '{book.title}'")
        else:
            print(f"{user.name} is already in the waiting list for '{book.title}'")

        print(f"Waiting list for '{book.title}': {[u.name for u in self.list_wait[book]]}")

#Proxy pattern
class BookProxy:
    def __init__(self, book: Book, library: Library):
        self.book = book 
        self.library = library  

    def borrow(self, user: Person):
        if self.book in self.library.books and self.library.books[self.book] > 0:
            self.library.borrow_book(user, self.book) 
        else:
            print(f"'{self.book.title}' is not available. Adding {user.name} to the waiting list.")
            self.library.waiting_list(self.book, user)

    def return_book(self, user: Person):
        self.library.return_book(user, self.book)