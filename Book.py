from datetime import datetime, date

class Book:
    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.is_issued = False
        self.issue_date = None

    def __str__(self):
        status = "Issued" if self.is_issued else "Available"
        return f"[{self.isbn}] {self.title} by {self.author} - {status}"

class Library:
    def __init__(self):
        self.books = {}
        self.fine_per_day = 5

    def add_book(self, isbn, title, author):
        if isbn in self.books:
            print(f"Book with ISBN {isbn} already exists.")
        else:
            new_book = Book(isbn, title, author)
            self.books[isbn] = new_book
            print(f"Book '{title}' added successfully.")

    def view_available_books(self):
        print("\n--- Available Books ---")
        available = [b for b in self.books.values() if not b.is_issued]
        if not available:
            print("No books currently available.")
        for book in available:
            print(book)

    def issue_book(self, isbn):
        book = self.books.get(isbn)
        if book:
            if not book.is_issued:
                book.is_issued = True
                book.issue_date = date.today()
                print(f"Book '{book.title}' has been issued on {book.issue_date}.")
            else:
                print("Book is already issued to someone else.")
        else:
            print("Book not found in library.")

    def return_book(self, isbn, return_date_str=None):

        book = self.books.get(isbn)
        if book and book.is_issued:

            if return_date_str:
                return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()
            else:
                return_date = date.today()


            days_kept = (return_date - book.issue_date).days

            loan_period = 7
            late_days = max(0, days_kept - loan_period)
            fine = late_days * self.fine_per_day

            book.is_issued = False
            book.issue_date = None

            print(f"Book '{book.title}' returned.")
            if fine > 0:
                print(f"LATE RETURN: {late_days} days late. Fine: Rs.{fine}")
            else:
                print("Returned on time. No fine.")
        else:
            print("Invalid return: Book was not issued or doesn't exist.")


my_library = Library()


my_library.add_book("101", "Python Crash Course", "Eric Matthes")
my_library.add_book("102", "Automate the Boring Stuff", "Al Sweigart")


my_library.view_available_books()


my_library.issue_book("101")


my_library.view_available_books()


print("\n--- Returning Book ---")
my_library.return_book("101", "2026-05-17")