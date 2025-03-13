import json
import streamlit as st
from typing import List, Dict, Any
from datetime import datetime
import plotly.express as px
import pandas as pd

# Custom styling
st.set_page_config(page_title="Modern Library Manager", layout="wide", initial_sidebar_state="expanded")

# Apply custom CSS for a modern, trendy look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        background-color: #f8f9fa;
    }
    
    .main-header {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .book-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        border-left: 5px solid #6366F1;
    }
    
    .book-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1);
    }
    
    .stats-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
        border-top: 5px solid #8B5CF6;
    }
    
    .sidebar .stSelectbox {
        background-color: white;
        border-radius: 10px;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(107, 114, 128, 0.25);
    }
    
    .stTextInput input, .stNumberInput input, .stSelectbox, .stMultiselect {
        border-radius: 10px;
        border: 1px solid #e5e7eb;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #6366F1;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #6B7280;
        margin-top: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        color: white;
    }
    
    div.stSlider > div[data-baseweb="slider"] > div > div {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
    }
    
    div.stSlider > div[data-baseweb="slider"] > div > div[role="slider"] {
        background-color: white;
        border: 2px solid #6366F1;
    }
    
    /* Additional trendy styles */
    .empty-library {
        text-align: center;
        padding: 4rem 0;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .empty-library img {
        width: 150px;
        opacity: 0.7;
    }
    
    .empty-library p {
        margin-top: 1rem;
        font-size: 1.2rem;
        color: #6B7280;
    }
    
    /* Animated elements */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .float-animation {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Badge styles */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-right: 0.5rem;
    }
    
    .badge-read {
        background-color: #10B981;
        color: white;
    }
    
    .badge-unread {
        background-color: #F59E0B;
        color: white;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c7d2fe;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #6366F1;
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
    # Create a modern header
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("📚 Bookshelf")
    st.markdown('<p style="font-size: 1.2rem; opacity: 0.8;">Your Personal Library Manager</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if 'library_manager' not in st.session_state:
        st.session_state.library_manager = LibraryManager()

    # Create a modern sidebar
    with st.sidebar:
        st.markdown('<h3 style="margin-bottom: 20px;">📑 Navigation</h3>', unsafe_allow_html=True)
        menu = st.selectbox(
            "",
            ["📖 Add Book", "🔍 Search Books", "📚 My Collection", "📊 Statistics", "🗑️ Manage Books"]
        )

    if menu == "📖 Add Book":
        st.markdown('<h2 style="margin-bottom: 20px;">📖 Add New Book</h2>', unsafe_allow_html=True)
        
        with st.form("add_book_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("📕 Title")
                author = st.text_input("✍️ Author")
                year = st.number_input("📅 Publication Year", min_value=1000, max_value=2023, value=2023)
                genre = st.selectbox("📚 Genre", ["Fiction", "Non-Fiction", "Science", "Technology", "History", "Biography", "Fantasy", "Mystery", "Romance", "Thriller", "Other"])
            
            with col2:
                cover_url = st.text_input("🖼️ Cover Image URL (optional)")
                rating = st.slider("⭐ Rating", 0, 5, 0)
                tags = st.multiselect("🏷️ Tags", ["Classic", "Bestseller", "Academic", "Self-Help", "Reference", "Novel", "Award-Winner", "Series", "Young Adult", "Children"])
                read = st.checkbox("📖 Have you read this book?")
            
            submit = st.form_submit_button("Add to My Collection", use_container_width=True)
            if submit:
                if title and author:
                    st.session_state.library_manager.add_book(
                        title, author, year, genre, read, rating, cover_url, tags
                    )
                    st.success(f"✅ Added: {title} by {author}")
                else:
                    st.error("❌ Title and Author are required!")

    elif menu == "🔍 Search Books":
        st.markdown('<h2 style="margin-bottom: 20px;">🔍 Find Books</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            query = st.text_input("🔎 Search by title, author, or tags")
        with col2:
            genre_filter = st.selectbox("📚 Filter by Genre", ["All"] + list(set(b['genre'] for b in st.session_state.library_manager.get_all_books())))
        with col3:
            rating_filter = st.slider("⭐ Minimum Rating", 0, 5, 0)

        filters = {
            'genre': genre_filter if genre_filter != "All" else None,
            'rating': rating_filter
        }

        results = st.session_state.library_manager.search_books(query, filters)
        
        if not results:
            st.info("📚 No books found matching your search criteria.")
        
        for book in results:
            with st.container():
                st.markdown(f'<div class="book-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 3])
                with col1:
                    if book['cover_url']:
                        st.image(book['cover_url'], width=150)
                    else:
                        st.image("https://via.placeholder.com/150x200?text=No+Cover", width=150)
                with col2:
                    st.markdown(f"### {book['title']}")
                    st.markdown(f"**Author:** {book['author']}")
                    st.markdown(f"**Year:** {book['year']} | **Genre:** {book['genre']}")
                    st.markdown(f"**Rating:** {'⭐' * book['rating']}")
                    st.markdown(f"**Tags:** {', '.join(book['tags']) if book['tags'] else 'None'}")
                    st.markdown(f"**Status:** {'📖 Read' if book['read'] else '📕 Unread'}")
                st.markdown('</div>', unsafe_allow_html=True)

    elif menu == "📊 Statistics":
        st.markdown('<h2 style="margin-bottom: 20px;">📊 Library Insights</h2>', unsafe_allow_html=True)
        stats = st.session_state.library_manager.get_statistics()
        
        # Modern metrics display
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{stats["total_books"]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Total Books</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{stats["read_books"]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Books Read</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{stats["percent_read"]}%</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Completion Rate</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
        
        # Enhanced visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            # Genre distribution
            df_genres = pd.DataFrame(list(stats['genres'].items()), columns=['Genre', 'Count'])
            fig_genres = px.pie(df_genres, values='Count', names='Genre', title='Books by Genre',
                               color_discrete_sequence=px.colors.sequential.Agsunset)
            fig_genres.update_traces(textposition='inside', textinfo='percent+label')
            fig_genres.update_layout(
                title_font_size=20,
                legend_title_font_size=16,
                legend_font_size=14
            )
            st.plotly_chart(fig_genres, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            # Rating distribution
            df_ratings = pd.DataFrame(list(stats['ratings'].items()), columns=['Rating', 'Count'])
            fig_ratings = px.bar(df_ratings, x='Rating', y='Count', title='Books by Rating',
                                color='Count', color_continuous_scale='Agsunset')
            fig_ratings.update_layout(
                title_font_size=20,
                xaxis_title_font_size=16,
                yaxis_title_font_size=16
            )
            st.plotly_chart(fig_ratings, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    elif menu == "🗑️ Manage Books":
        st.markdown('<h2 style="margin-bottom: 20px;">🗑️ Manage Books</h2>', unsafe_allow_html=True)
        
        title = st.text_input("Enter the title of the book to remove")
        if st.button("Remove Book", use_container_width=True):
            if st.session_state.library_manager.remove_book(title):
                st.success(f"✅ Successfully removed: {title}")
            else:
                st.error("❌ Book not found in your collection!")

    elif menu == "📚 My Collection":
        st.markdown('<h2 style="margin-bottom: 20px;">📚 My Book Collection</h2>', unsafe_allow_html=True)
        books = st.session_state.library_manager.get_all_books()
        
        if not books:
            st.info("📚 Your library is empty. Start by adding some books!")
            st.markdown("""
            <div style="text-align: center; padding: 3rem 0;">
                <img src="https://cdn-icons-png.flaticon.com/512/2702/2702134.png" width="150">
                <p style="margin-top: 1rem; font-size: 1.2rem;">Your bookshelf is waiting to be filled!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Create tabs for different views
            tab1, tab2 = st.tabs(["📚 Grid View", "📋 List View"])
            
            with tab1:
                # Grid view with 3 books per row
                for i in range(0, len(books), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i+j < len(books):
                            book = books[i+j]
                            with cols[j]:
                                st.markdown(f'<div class="book-card">', unsafe_allow_html=True)
                                if book['cover_url']:
                                    st.image(book['cover_url'], width=150)
                                else:
                                    st.image("https://via.placeholder.com/150x200?text=No+Cover", width=150)
                                st.markdown(f"### {book['title']}")
                                st.markdown(f"**Author:** {book['author']}")
                                st.markdown(f"**Genre:** {book['genre']}")
                                st.markdown(f"**Rating:** {'⭐' * book['rating']}")
                                st.markdown(f"**Status:** {'📖 Read' if book['read'] else '📕 Unread'}")
                                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                # List view with more details
                for book in books:
                    with st.container():
                        st.markdown(f'<div class="book-card">', unsafe_allow_html=True)
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            if book['cover_url']:
                                st.image(book['cover_url'], width=150)
                            else:
                                st.image("https://via.placeholder.com/150x200?text=No+Cover", width=150)
                        with col2:
                            st.markdown(f"### {book['title']}")
                            st.markdown(f"**Author:** {book['author']}")
                            st.markdown(f"**Year:** {book['year']} | **Genre:** {book['genre']}")
                            st.markdown(f"**Rating:** {'⭐' * book['rating']}")
                            st.markdown(f"**Tags:** {', '.join(book['tags']) if book['tags'] else 'None'}")
                            st.markdown(f"**Status:** {'📖 Read' if book['read'] else '📕 Unread'}")
                            st.markdown(f"**Added on:** {book.get('date_added', 'Unknown').split('T')[0]}")
                        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()