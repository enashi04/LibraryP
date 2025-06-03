# My Little Library — Event-Driven Book Management App

A playful, event-driven library management system in Python, designed with clean object-oriented architecture.
This project simulates a library where authors create books, users follow them, and events trigger book availability updates.

Includes two interactive modes:

- A classic command-line interface (CLI) using standard prints.
- A colorful and child-friendly version powered by colorama, with emojis and vibrant text output.

Features:

📖 Book creation by writers (with optional co-authors)

🔔 Event system for book publication and availability (Observer pattern)

🧍 Users can register, borrow, return, and reserve books

🧑‍🎓 Users can follow authors to receive real-time book release notifications

Two entry points (mains):

- main_lite.py: Simple terminal interaction
- main_colorama.py: Fun, colorful CLI using colorama

-> Singleton design for the library

-> Built on solid OOP concepts: inheritance, enums, encapsulation, and abstract base classes

