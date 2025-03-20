from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base, sessionmaker


Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    UniqueConstraint('title', 'author', name='uix_1')
    items = relationship("BookItem", back_populates="book")

class BookItem(Base):
    __tablename__ = "book_items"
    id = Column(Integer, primary_key=True)
    is_available = Column(Boolean, default=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    book = relationship("Book", back_populates="items")

    def borrow(self):
        if self.is_available:
            self.is_available = False
            return True
        return False

    def return_book(self):
        if not self.is_available:
            self.is_available = True
            return True
        return False

engine = create_engine('mysql+mysqlconnector://sql10749185:ZXr2RRDHxL@sql10.freemysqlhosting.net/sql10749185')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def add_book_to_library(session, title, author):
    book = Book(title=title, author=author)
    session.add(book)
    session.commit()
    return book

def add_book_item(session, book_id):
    book = session.query(Book).get(book_id)
    if book:
        book_item = BookItem(book=book)
        session.add(book_item)
        session.commit()
        return book_item

def list_all_books(session):
    return session.query(Book).all()

def list_book_items(session):
    items = session.query(BookItem).all()
    for item in items:
        status = "Available" if item.is_available else "Borrowed"
        print(f"Exemplar ID: {item.id}, Book: {item.book.title}, Status: {status}")

def borrow_book_by_id(session, item_id):
    item = session.query(BookItem).get(item_id)
    if item and item.borrow():
        session.commit()
        return item
    return None

def return_book_by_id(session, item_id):
    item = session.query(BookItem).get(item_id)
    if item and item.return_book():
        session.commit()
        return item
    return None

def add_book_ui(session):
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    book = add_book_to_library(session, title, author)
    print(f"Book '{book.title}' by {book.author} added to the library.")

def list_books_ui(session):
    books = list_all_books(session)
    if not books:
        print("No books in the library.")
    else:
        for book in books:
            print(f"{book.id}: {book.title} by {book.author}")

def add_book_item_ui(session):
    book_id = int(input("Enter Book ID to add an exemplar: "))
    add_book_item(session, book_id)

def borrow_book_item_ui(session):
    item_id = int(input("Enter the ID of the exemplar to borrow:"))
    item = borrow_book_by_id(session, item_id)
    if item:
        print(f"You have borrowed '{item.book.title}.'")
    else:
        print("Exemplar not found or already borrowed.")

def return_book_item_ui(session):
    item_id = int(input("Enter the ID of the exemplar to return:"))
    item = return_book_by_id(session, item_id)
    if item:
        print(f"You have returned '{item.book.title}.'")
    else:
        print("Exemplar not found or was not borrowed.")

def main():
    session = Session()
    while True:
        print("\nLibrary Menu")
        print("1. Add Book")
        print("2. List Books")
        print("3. Add Book Item")
        print("4. List Book Items")
        print("5. Borrow Book Item")
        print("6. Return Book Item")
        print("7. Exit")
        choice = int(input("Enter your choice:"))

        if choice == 1:
            add_book_ui(session)
        elif choice == 2:
            list_books_ui(session)
        elif choice == 3:
            add_book_item_ui(session)
        elif choice == 4:
            list_book_items(session)
        elif choice == 5:
            borrow_book_item_ui(session)
        elif choice == 6:
            return_book_item_ui(session)
        elif choice == 7:
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
