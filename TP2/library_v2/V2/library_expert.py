from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import List
from random import randint, random


# Enum class for Genre: genre can only ba among a predefined list
class Genre(Enum):
    FICTION = "Fiction"
    NON_FICTION = "Non-Fiction"
    MYSTERY = "Mystery"
    FANTASY = "Fantasy"
    SCIFI = "Science Fiction"
    BIOGRAPHY = "Biography"
    HISTORY = "History"
    COMEDY = "Comedy"
    ROMANCE = "Romance"
    THRILLER = "Thriller"
    CHILDREN = "Children"
    ADVENTURE = "Adventure"


# ABC super-class: Abstract Class: make it impossible to create a Person
# Only User and Writer should exist in the program
class Person(ABC):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"[{type(self).__name__}] {self.name} ({self.age} years old)"

# Base class for Book Events
class BookEvent:
    def __init__(self, source, title: str):
        self.source = source  # the writer
        self.title = title

class BookListener(ABC):
    def eventAction(self, event: BookEvent):
        pass


# Abstract class for event generators
class BookGenerator(ABC):
    def __init__(self):
        self._listeners: List[BookListener] = []

    def registerListener(self, listener: BookListener):
        self._listeners.append(listener)

    def createEvent(self, title: str):
        pass  # will be implemented by Writer


class Book:
    def __init__(self, title: str, genres: set[Genre] = None, pages: int = 0):
        self.title = title
        self.genres = genres if genres else set()
        self.pages = pages

    def __repr__(self):
        return f"[Book] {self.title}"

class Writer(Person, BookGenerator):
    def __init__(self, name: str, age: int):
        Person.__init__(self, name, age)
        BookGenerator.__init__(self)

    def createEvent(self, title: str):
        print(f"{self.name} created a new book: {title}")
        event = BookEvent(self, title)
        for listener in self._listeners:
            listener.eventAction(event)


# User listens to writers
class User(Person, BookListener):
    def __init__(self, name: str, age: int):
        super().__init__(name, age)
        self.notifications = []

    def eventAction(self, event: BookEvent):
        print(f"{self.name} was notified of '{event.title}' by {event.source.name}")
        # Probability-based borrowing
        p = 0.5
        if random() < p:
            print(f"{self.name} decided to borrow '{event.title}' (p={p})")
            self.notifications.append(event.title)
        else:
            print(f"{self.name} decided not to borrow '{event.title}' (p={p})")


# Correction complète pour intégrer les fonctionnalités avancées tout en conservant les blocs generator, event, listener
class Library(BookListener):
    def __init__(self):
        self.books = {}  # Dictionnaire pour stocker les livres et leurs quantités
        self.reservations = {}  # Gestion des réservations
        self.registered_users = set()  # Utilisateurs enregistrés

    def eventAction(self, event: BookEvent):
        if event.title in self.books:
            self.books[event.title] += 1
        else:
            self.books[event.title] = 1
        print(f"Library added '{event.title}' by {event.source.name} to its catalog")

        # Notifier les utilisateurs ayant réservé ce livre
        if event.title in self.reservations and self.reservations[event.title]:
            user = self.reservations[event.title].pop(0)  # Premier utilisateur dans la file d'attente
            print(f"Notification: {user.name}, the book '{event.title}' is now available!")

    def register(self, user: User):
        self.registered_users.add(user)
        print(f"{user.name} has been registered to the library.")

    def unregister(self, user: User):
        if user in self.registered_users:
            self.registered_users.remove(user)
            print(f"{user.name} has been unregistered from the library.")

    def borrowBook(self, title: str, user: User):
        if user not in self.registered_users:
            print(f"{user.name} is not registered and cannot borrow books.")
            return

        if title in self.books and self.books[title] > 0:
            self.books[title] -= 1
            print(f"{user.name} borrowed '{title}'")
        else:
            print(f"{title} is not available. Adding {user.name} to the reservation list.")
            if title not in self.reservations:
                self.reservations[title] = []
            self.reservations[title].append(user)

    def returnBook(self, title: str):
        if title in self.books:
            self.books[title] += 1
            print(f"'{title}' has been returned to the library.")

            # Notifier les utilisateurs ayant réservé ce livre
            if title in self.reservations and self.reservations[title]:
                user = self.reservations[title].pop(0)
                print(f"Notification: {user.name}, the book '{title}' is now available!")
        else:
            self.books[title] = 1
            print(f"'{title}' has been added to the library.")

    def consult(self, user: User):
        if user not in self.registered_users:
            print(f"{user.name} is not registered and cannot consult books.")
            return []
        return [title for title, quantity in self.books.items() if quantity > 0]

    def follow(self, writer: Writer):
        writer.registerListener(self)
        print(f"Library is now following {writer.name}.")
