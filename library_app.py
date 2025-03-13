import json
import streamlit as st
from typing import List, Dict, Any

class LibraryManager:
    def __init__(self):
        self.books = []
        self.load_library()

    def add_book(self, title: str, author: str, year: int, genre: str, read: bool) -> None:
        book = {
            'title': title,
            'author': author,
            'year': year,
            'genre': genre,
            'read': read
        }
        self.books.append(book)
        self.save_library()

    def remove_book(self, title: str) -> bool:
        for book in self.books:
            if book['title'].lower() == title.lower():
                self.books.remove(book)
                self.save_library()
                return True
        return False

    def search_books(self, query: str) -> List[Dict[str, Any]]:
        query = query.lower()
        return [book for book in self.books if 
                query in book['title'].lower() or 
                query in book['author'].lower()]

    def get_all_books(self) -> List[Dict[str, Any]]:
        return self.books

    def get_statistics(self) -> Dict[str, float]:
        total_books = len(self.books)
        read_books = sum(1 for book in self.books if book['read'])
        percent_read = (read_books / total_books * 100) if total_books > 0 else 0
        
        return {
            'total_books': total_books,
            'read_books': read_books,
            'percent_read': round(percent_read, 2)
        }

    def save_library(self) -> None:
        with open('library.json', 'w') as f:
            json.dump(self.books, f)

    def load_library(self) -> None:
        try:
            with open('library.json', 'r') as f:
                self.books = json.load(f)
        except FileNotFoundError:
            self.books = []

def main():
    st.title("Personal Library Manager")

    if 'library_manager' not in st.session_state:
        st.session_state.library_manager = LibraryManager()

    menu = st.sidebar.selectbox(
        "Menu",
        ["Add Book", "Remove Book", "Search Books", "Display All Books", "Statistics"]
    )

    if menu == "Add Book":
        st.header("Add a New Book")
        with st.form("add_book_form"):
            title = st.text_input("Title")
            author = st.text_input("Author")
            year = st.number_input("Publication Year", min_value=1000, max_value=2023, value=2023)
            genre = st.text_input("Genre")
            read = st.checkbox("Have you read this book?")
            
            if st.form_submit_button("Add Book"):
                st.session_state.library_manager.add_book(title, author, year, genre, read)
                st.success(f"Added: {title} by {author}")

    elif menu == "Remove Book":
        st.header("Remove a Book")
        title = st.text_input("Enter the title of the book to remove")
        if st.button("Remove Book"):
            if st.session_state.library_manager.remove_book(title):
                st.success(f"Removed: {title}")
            else:
                st.error("Book not found!")

    elif menu == "Search Books":
        st.header("Search Books")
        query = st.text_input("Search by title or author")
        if query:
            results = st.session_state.library_manager.search_books(query)
            if results:
                for book in results:
                    st.write(f"📚 {book['title']} by {book['author']} ({book['year']}) - {book['genre']}")
                    st.write(f"Status: {'Read ✓' if book['read'] else 'Unread'}")
                    st.divider()
            else:
                st.info("No books found matching your search.")

    elif menu == "Display All Books":
        st.header("All Books")
        books = st.session_state.library_manager.get_all_books()
        if books:
            for book in books:
                st.write(f"📚 {book['title']} by {book['author']} ({book['year']}) - {book['genre']}")
                st.write(f"Status: {'Read ✓' if book['read'] else 'Unread'}")
                st.divider()
        else:
            st.info("Your library is empty.")

    elif menu == "Statistics":
        st.header("Library Statistics")
        stats = st.session_state.library_manager.get_statistics()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Books", stats['total_books'])
        with col2:
            st.metric("Read Books", stats['read_books'])
        with col3:
            st.metric("Percentage Read", f"{stats['percent_read']}%")

if __name__ == "__main__":
    main()