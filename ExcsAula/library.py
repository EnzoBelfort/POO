from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
import datetime

LOAN_PERIOD_DAYS = 14
COOLDOWN_DAYS = 7

class LibraryError(Exception):
    def __init__(self, message: str = "An error occurred in the library system")
        super().__init__(message)

class NonMemberError(LibraryError):
    def __init__(self, member_name: str):
        message = f"{member_name} is not registered"
        super().__init__(message)

class BookNotAvailableError(LibraryError):
    def __init__(self, book_title: str):
        message = f"The book '{book_title}' is not available"
        super().__init__(message)

class CooldownPeriodError(LibraryError):
    def __init__(self, member_name: str, cooldown_end_date: datetime.datetime):
        message = f"{member_name} is in a cooldown period until {cooldown_end_date}"
        super().__init__(message)

@dataclass
class Book:
    title: str
    authors: List[str]
    edition: int

class Status(Enum):
    AVAILABLE = 1
    LOANED = 2
    LOST = 3

@dataclass
class Loan:
    book_item: 'BookItem'
    member: 'Member'
    date_borrowed: datetime.datetime
    date_returned: Optional[datetime.datetime] = None
    due_date: datetime.datetime = None

@dataclass
class BookItem:
    book: Book
    status: Status = Status.AVAILABLE

@dataclass
class Member:
    name: str
    cooldown_end_date: Optional[datetime.datetime] = None
    current_loan: Optional[BookItem] = None

@dataclass 
class Library:
    items: List[BookItem] = field(default_factory=list)
    loan_history: List[Loan] = field(default_factory=list)
    members: List[Member] = field(default_factory=list)

    def add_book_item(self, book_item: BookItem):
        self.items.append(book_item)

    def add_member(self, member: Member):
        self.members.append(member)

    def checkout(self, book_item: BookItem, member: Member) -> None:
        if member not in self.members:
            raise NonMemberError(member.name)
        if book_item.status != Status.AVAILABLE:
            raise BookNotAvailableError(book_item.book.title)
        if member.cooldown_end_date and member.cooldown_end_date > datetime.datetime.now():
            raise CooldownPeriodError(member.name, member.cooldown_end_date)

        book_item.status = Status.LOANED
        date_borrowed = datetime.datetime.now()
        due_date = date_borrowed + datetime.timedelta(days=LOAN_PERIOD_DAYS)
        loan = Loan(book_item=book_item, member=member, date_borrowed=date_borrowed, due_date=due_date)
        member.current_loan = loan
        self.loan_history.append(loan)

    def return_book(self, book_item: BookItem, member: Member) -> None:
      if member not in self.members:
          raise NonMemberError(member.name)        
      if member.current_loan is None or member.current_loan.book_item != book_item:
          raise LibraryError(f"{member.name} não possui o livro '{book_item.book.title}' em empréstimo.")
      
      
      current_loan = member.current_loan
      current_loan.date_returned = datetime.datetime.now()
      
      if current_loan.date_returned > current_loan.due_date:
          member.cooldown_end_date = current_loan.date_returned + datetime.timedelta(days=COOLDOWN_DAYS)
      
      book_item.status = Status.AVAILABLE
      member.current_loan = None
      self.loan_history.append(current_loan)      