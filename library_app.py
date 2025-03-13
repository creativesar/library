import json
import streamlit as st
from typing import List, Dict, Any
from datetime import datetime
import plotly.express as px
import pandas as pd

# Updated Custom styling
st.set_page_config(page_title="Modern Library Manager", layout="wide", initial_sidebar_state="expanded")

# Enhanced CSS with modern styling
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        background-color: #f8f9fa;
    }
    .book-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease-in-out;
    }
    .book-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    }
    .stats-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    .main-header {
        padding: 2rem 0;
        text-align: center;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    .sidebar .stSelectbox {
        background-color: white;
        border-radius: 10px;
        padding: 0.5rem;
    }
    .stButton button {
        width: 100%;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        background: #4b6cb7;
        color: white;
    }
    .stButton button:hover {
        background: #182848;
    }
    </style>
""", unsafe_allow_html=True)

class LibraryManager:
    def __init__(self):
        self.books = []
        self.load_library()

    def add_book(self, title: str, author: str, year: int, genre: str, read: bool, 
                 rating: int = 0, cover_url: str = "", tags: List[str] = None) -> None:
        book = {
            'title': title,
            'author': author,
            'year': year,
            'genre': genre,
            'read': read,
            'rating': rating,
            'cover_url': cover_url,
            'tags': tags or [],
            'date_added': datetime.now().isoformat(),
            'last_modified': datetime.now().isoformat()
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

    def search_books(self, query: str, filters: Dict = None) -> List[Dict[str, Any]]:
        results = self.books
        
        if filters:
            if filters.get('genre'):
                results = [b for b in results if b['genre'] == filters['genre']]
            if filters.get('year_from'):
                results = [b for b in results if b['year'] >= filters['year_from']]
            if filters.get('year_to'):
                results = [b for b in results if b['year'] <= filters['year_to']]
            if filters.get('rating'):
                results = [b for b in results if b['rating'] >= filters['rating']]

        if query:
            query = query.lower()
            results = [b for b in results if 
                      query in b['title'].lower() or 
                      query in b['author'].lower() or
                      query in ' '.join(b['tags']).lower()]
        
        return results

    def get_statistics(self) -> Dict[str, Any]:
        total_books = len(self.books)
        read_books = sum(1 for book in self.books if book['read'])
        percent_read = (read_books / total_books * 100) if total_books > 0 else 0
        
        # Get genre distribution
        genres = {}
        for book in self.books:
            genres[book['genre']] = genres.get(book['genre'], 0) + 1

        # Get rating distribution
        ratings = {}
        for book in self.books:
            ratings[book['rating']] = ratings.get(book['rating'], 0) + 1
        
        return {
            'total_books': total_books,
            'read_books': read_books,
            'percent_read': round(percent_read, 2),
            'genres': genres,
            'ratings': ratings
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
    with st.container():
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.title("📚 Modern Library Manager")
        st.markdown('</div>', unsafe_allow_html=True)

    # Modernized sidebar
    with st.sidebar:
        st.markdown("### 📑 Navigation")
        menu = st.selectbox(
            "",
            ["📖 Add Book", "🔍 Search Books", "📚 Display All Books", "📊 Statistics", "🗑️ Remove Book"]
        )

    if menu == "📖 Add Book":
        st.markdown("### 📖 Add New Book")
        with st.form("add_book_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("📕 Title")
                author = st.text_input("✍️ Author")
                year = st.number_input("📅 Publication Year", min_value=1000, max_value=2023, value=2023)
                genre = st.selectbox("📚 Genre", ["Fiction", "Non-Fiction", "Science", "Technology", "History", "Biography", "Other"])
            
            with col2:
                cover_url = st.text_input("🖼️ Cover Image URL (optional)")
                rating = st.slider("⭐ Rating", 0, 5, 0)
                tags = st.multiselect("🏷️ Tags", ["Classic", "Bestseller", "Academic", "Self-Help", "Reference", "Novel"])
                read = st.checkbox("📖 Have you read this book?")
            
            submit = st.form_submit_button("Add Book", use_container_width=True)
            if submit:
                if title and author:
                    st.session_state.library_manager.add_book(
                        title, author, year, genre, read, rating, cover_url, tags
                    )
                    st.success(f"✅ Added: {title} by {author}")
                else:
                    st.error("❌ Title and Author are required!")

    elif menu == "🔍 Search Books":
        st.header("Search Books")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            query = st.text_input("Search by title, author, or tags")
        with col2:
            genre_filter = st.selectbox("Filter by Genre", ["All"] + list(set(b['genre'] for b in st.session_state.library_manager.get_all_books())))
        with col3:
            rating_filter = st.slider("Minimum Rating", 0, 5, 0)

        filters = {
            'genre': genre_filter if genre_filter != "All" else None,
            'rating': rating_filter
        }

        results = st.session_state.library_manager.search_books(query, filters)
        
        for book in results:
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    if book['cover_url']:
                        st.image(book['cover_url'], width=150)
                    else:
                        st.image("https://placeholder.com/150x200", width=150)
                with col2:
                    st.markdown(f"### {book['title']}")
                    st.write(f"**Author:** {book['author']}")
                    st.write(f"**Year:** {book['year']} | **Genre:** {book['genre']}")
                    st.write(f"**Rating:** {'⭐' * book['rating']}")
                    st.write(f"**Tags:** {', '.join(book['tags'])}")
                    st.write(f"**Status:** {'Read ✓' if book['read'] else 'Unread'}")
                st.divider()

    elif menu == "📊 Statistics":
        st.header("Library Statistics")
        stats = st.session_state.library_manager.get_statistics()
        
        # Basic metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Books", stats['total_books'])
        with col2:
            st.metric("Read Books", stats['read_books'])
        with col3:
            st.metric("Percentage Read", f"{stats['percent_read']}%")

        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Genre distribution
            df_genres = pd.DataFrame(list(stats['genres'].items()), columns=['Genre', 'Count'])
            fig_genres = px.pie(df_genres, values='Count', names='Genre', title='Books by Genre')
            st.plotly_chart(fig_genres)
        
        with col2:
            # Rating distribution
            df_ratings = pd.DataFrame(list(stats['ratings'].items()), columns=['Rating', 'Count'])
            fig_ratings = px.bar(df_ratings, x='Rating', y='Count', title='Books by Rating')
            st.plotly_chart(fig_ratings)

    elif menu == "Remove Book":
        st.header("Remove a Book")
        title = st.text_input("Enter the title of the book to remove")
        if st.button("Remove Book"):
            if st.session_state.library_manager.remove_book(title):
                st.success(f"Removed: {title}")
            else:
                st.error("Book not found!")

    elif menu == "Display All Books":
        st.markdown("### 📚 Library Collection")
        books = st.session_state.library_manager.get_all_books()
        if books:
            for book in books:
                with st.container():
                    st.markdown(f"""
                    <div class="book-card">
                        <h3>{book['title']}</h3>
                        <p><strong>Author:</strong> {book['author']}</p>
                        <p><strong>Year:</strong> {book['year']} | <strong>Genre:</strong> {book['genre']}</p>
                        <p><strong>Rating:</strong> {"⭐" * book['rating']}</p>
                        <p><strong>Status:</strong> {"📖 Read" if book['read'] else "📕 Unread"}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("📚 Your library is empty. Start by adding some books!")

if __name__ == "__main__":
    main()