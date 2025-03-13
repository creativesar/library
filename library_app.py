import json
import streamlit as st
from typing import List, Dict, Any
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import random

# Set page configuration
st.set_page_config(
    page_title="Modern Library Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subheader {
        font-size: 1.8rem;
        color: #0D47A1;
        margin-bottom: 1rem;
    }
    .card {
        border-radius: 15px;
        padding: 1.8rem;
        background: linear-gradient(145deg, #ffffff, #f5f7fa);
        box-shadow: 5px 5px 15px #d1d9e6, -5px -5px 15px #ffffff;
        margin-bottom: 1.5rem;
        transition: transform 0.2s ease;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    
    /* Enhanced Book Card */
    .book-card {
        border-left: 5px solid #1E88E5;
        padding: 1.2rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .book-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* Enhanced Badges */
    .read-badge {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    .unread-badge {
        background: linear-gradient(45deg, #FFC107, #FFB300);
        color: #212121;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Enhanced Form Controls */
    .stTextInput > div > div {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 0.5rem;
    }
    .stTextInput > div > div:focus-within {
        border-color: #1E88E5;
        box-shadow: 0 0 0 2px rgba(30,136,229,0.2);
    }
    
    /* Enhanced Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(45deg, #1E88E5, #1976D2);
        color: white;
        font-weight: 500;
        padding: 0.6rem 1.2rem;
        border: none;
        box-shadow: 0 4px 15px rgba(30,136,229,0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30,136,229,0.4);
    }
    
    /* Enhanced Metrics */
    .metric-card {
        background: linear-gradient(145deg, #ffffff, #f5f7fa);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 5px 5px 15px #d1d9e6;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
    }
    .metric-label {
        font-size: 1.1rem;
        color: #424242;
        margin-top: 0.5rem;
    }
    
    /* Enhanced Charts */
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

class LibraryManager:
    def __init__(self):
        self.books = []
        self.load_library()

    def add_book(self, title: str, author: str, year: int, genre: str, read: bool, rating: int = 0, date_added: str = None) -> None:
        if not date_added:
            date_added = datetime.now().strftime("%Y-%m-%d")
            
        book = {
            'title': title,
            'author': author,
            'year': year,
            'genre': genre,
            'read': read,
            'rating': rating,
            'date_added': date_added
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

    def get_statistics(self) -> Dict[str, Any]:
        total_books = len(self.books)
        read_books = sum(1 for book in self.books if book['read'])
        percent_read = (read_books / total_books * 100) if total_books > 0 else 0
        
        # Get genre distribution
        genres = {}
        for book in self.books:
            genre = book['genre']
            if genre in genres:
                genres[genre] += 1
            else:
                genres[genre] = 1
                
        # Get author distribution (top 5)
        authors = {}
        for book in self.books:
            author = book['author']
            if author in authors:
                authors[author] += 1
            else:
                authors[author] = 1
        top_authors = dict(sorted(authors.items(), key=lambda x: x[1], reverse=True)[:5])
        
        return {
            'total_books': total_books,
            'read_books': read_books,
            'percent_read': round(percent_read, 2),
            'genres': genres,
            'top_authors': top_authors
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
    # Initialize session state for library manager
    if 'library_manager' not in st.session_state:
        st.session_state['library_manager'] = LibraryManager()

    # Custom header with HTML
    st.markdown('<h1 class="main-header">📚 Modern Library Manager</h1>', unsafe_allow_html=True)

    # Remove this duplicate initialization block
    # if 'library_manager' not in st.session_state:
    #     st.session_state.library_manager = LibraryManager()

    # Sidebar with gradient background
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #1E88E5;">Navigation</h2>
        </div>
        """, unsafe_allow_html=True)
        
        menu = st.selectbox(
            "Choose an option",
            ["📕 Add Book", "🗑️ Remove Book", "🔍 Search Books", "📚 My Library", "📊 Statistics & Analytics"]
        )

    if "📕 Add Book" in menu:
        st.markdown('<h2 class="subheader">Add a New Book</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            with st.form("add_book_form"):
                title = st.text_input("Title")
                author = st.text_input("Author")
                col_year, col_genre = st.columns(2)
                with col_year:
                    year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, value=datetime.now().year)
                with col_genre:
                    genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", "Mystery", "Thriller", 
                                                  "Romance", "Biography", "History", "Self-Help", "Other"])
                
                col_read, col_rating = st.columns(2)
                with col_read:
                    read = st.checkbox("Have you read this book?")
                with col_rating:
                    rating = st.slider("Rating", 0, 5, 0, help="Rate this book from 0 to 5 stars")
                
                if st.form_submit_button("Add to Library"):
                    if title and author:
                        st.session_state.library_manager.add_book(title, author, year, genre, read, rating)
                        st.success(f"Added: {title} by {author}")
                    else:
                        st.error("Title and author are required!")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Book Preview")
            if 'title' in locals() and title:
                st.markdown(f"""
                <div class="book-card">
                    <div class="book-title">{title or "Title"}</div>
                    <div class="book-author">by {author or "Author"}</div>
                    <div class="book-meta">{genre or "Genre"} • {year or "Year"}</div>
                    <div style="margin-top: 10px;">
                        <span class="{'read-badge' if read else 'unread-badge'}">{
                            "Read ✓" if read else "Not Read"}</span>
                        <span style="margin-left: 10px;">{"⭐" * rating}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Fill in the form to see a preview of your book entry")
            st.markdown('</div>', unsafe_allow_html=True)

    elif "🗑️ Remove Book" in menu:
        st.markdown('<h2 class="subheader">Remove a Book</h2>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        books = st.session_state.library_manager.get_all_books()
        if books:
            book_titles = [book['title'] for book in books]
            title_to_remove = st.selectbox("Select a book to remove", book_titles)
            
            # Display the selected book details
            selected_book = next((book for book in books if book['title'] == title_to_remove), None)
            if selected_book:
                st.markdown(f"""
                <div class="book-card">
                    <div class="book-title">{selected_book['title']}</div>
                    <div class="book-author">by {selected_book['author']}</div>
                    <div class="book-meta">{selected_book['genre']} • {selected_book['year']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("Remove Selected Book"):
                if st.session_state.library_manager.remove_book(title_to_remove):
                    st.success(f"Removed: {title_to_remove}")
                    st.experimental_rerun()
                else:
                    st.error("Book not found!")
        else:
            st.info("Your library is empty.")
        st.markdown('</div>', unsafe_allow_html=True)

    elif "🔍 Search Books" in menu:
        st.markdown('<h2 class="subheader">Search Books</h2>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        query = st.text_input("Search by title or author")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_by_title = st.checkbox("Title", value=True)
        with col2:
            search_by_author = st.checkbox("Author", value=True)
        with col3:
            search_by_genre = st.checkbox("Genre", value=False)
            
        if query:
            results = st.session_state.library_manager.search_books(query)
            
            # Filter based on checkboxes
            filtered_results = []
            for book in results:
                if (search_by_title and query.lower() in book['title'].lower()) or \
                   (search_by_author and query.lower() in book['author'].lower()) or \
                   (search_by_genre and query.lower() in book['genre'].lower()):
                    filtered_results.append(book)
            
            if filtered_results:
                st.write(f"Found {len(filtered_results)} books matching '{query}'")
                for book in filtered_results:
                    st.markdown(f"""
                    <div class="book-card">
                        <div class="book-title">{book['title']}</div>
                        <div class="book-author">by {book['author']}</div>
                        <div class="book-meta">{book['genre']} • {book['year']}</div>
                        <div style="margin-top: 10px;">
                            <span class="{'read-badge' if book['read'] else 'unread-badge'}">{
                                "Read ✓" if book['read'] else "Not Read"}</span>
                            <span style="margin-left: 10px;">{"⭐" * book.get('rating', 0)}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No books found matching your search.")
        st.markdown('</div>', unsafe_allow_html=True)

    elif "📚 My Library" in menu:
        st.markdown('<h2 class="subheader">My Library</h2>', unsafe_allow_html=True)
        
        books = st.session_state.library_manager.get_all_books()
        
        if books:
            # Create tabs for different views
            tab1, tab2 = st.tabs(["Card View", "Table View"])
            
            with tab1:
                # Card view with columns
                cols = st.columns(3)
                for i, book in enumerate(books):
                    with cols[i % 3]:
                        st.markdown(f"""
                        <div class="book-card">
                            <div class="book-title">{book['title']}</div>
                            <div class="book-author">by {book['author']}</div>
                            <div class="book-meta">{book['genre']} • {book['year']}</div>
                            <div style="margin-top: 10px;">
                                <span class="{'read-badge' if book['read'] else 'unread-badge'}">{
                                    "Read ✓" if book['read'] else "Not Read"}</span>
                                <span style="margin-left: 10px;">{"⭐" * book.get('rating', 0)}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            with tab2:
                # Table view
                df = pd.DataFrame(books)
                if 'rating' not in df.columns:
                    df['rating'] = 0
                if 'date_added' not in df.columns:
                    df['date_added'] = "Unknown"
                
                # Reorder columns
                columns_order = ['title', 'author', 'year', 'genre', 'read', 'rating', 'date_added']
                df = df[columns_order]
                
                # Rename columns
                df.columns = ['Title', 'Author', 'Year', 'Genre', 'Read', 'Rating', 'Date Added']
                
                # Format the Read column
                df['Read'] = df['Read'].map({True: "✅", False: "❌"})
                
                # Format the Rating column
                df['Rating'] = df['Rating'].apply(lambda x: "⭐" * int(x))
                
                st.dataframe(df, use_container_width=True)
        else:
            st.info("Your library is empty. Add some books to get started!")

    elif "📊 Statistics & Analytics" in menu:
        st.markdown('<h2 class="subheader">Library Statistics & Analytics</h2>', unsafe_allow_html=True)
        
        stats = st.session_state.library_manager.get_statistics()
        
        # Top metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['total_books']}</div>
                <div class="metric-label">Total Books</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['read_books']}</div>
                <div class="metric-label">Read Books</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['percent_read']}%</div>
                <div class="metric-label">Completion Rate</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Charts row
        st.markdown('<h3 style="margin-top: 20px;">Reading Analytics</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Reading status pie chart
            fig = go.Figure(data=[go.Pie(
                labels=['Read', 'Unread'],
                values=[stats['read_books'], stats['total_books'] - stats['read_books']],
                hole=.6,
                marker_colors=['#4CAF50', '#FFC107']
            )])
            fig.update_layout(
                title_text="Reading Status",
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title_x=0.5
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            # Genre distribution
            if stats['genres']:
                genres_df = pd.DataFrame({
                    'Genre': list(stats['genres'].keys()),
                    'Count': list(stats['genres'].values())
                })
                fig = px.bar(genres_df, x='Genre', y='Count', color='Count',
                            color_continuous_scale='Blues')
                fig.update_layout(title_text="Books by Genre")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Add books with genres to see this chart")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Author analysis
        st.markdown('<h3 style="margin-top: 20px;">Author Analysis</h3>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        if stats['top_authors']:
            authors_df = pd.DataFrame({
                'Author': list(stats['top_authors'].keys()),
                'Books': list(stats['top_authors'].values())
            })
            fig = px.bar(authors_df, x='Author', y='Books', color='Books',
                        color_continuous_scale='Greens')
            fig.update_layout(title_text="Top Authors in Your Library")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add more books to see author statistics")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Reading timeline (if date_added exists)
        books = st.session_state.library_manager.get_all_books()
        if books and any('date_added' in book for book in books):
            st.markdown('<h3 style="margin-top: 20px;">Reading Timeline</h3>', unsafe_allow_html=True)
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            # Filter books with date_added
            dated_books = [book for book in books if 'date_added' in book]
            if dated_books:
                # Create timeline dataframe
                timeline_df = pd.DataFrame(dated_books)
                timeline_df['date_added'] = pd.to_datetime(timeline_df['date_added'])
                timeline_df = timeline_df.sort_values('date_added')
                
                # Create cumulative count
                timeline_df['cumulative_count'] = range(1, len(timeline_df) + 1)
                
                # Plot timeline
                fig = px.line(timeline_df, x='date_added', y='cumulative_count',
                            labels={'date_added': 'Date', 'cumulative_count': 'Total Books'},
                            title='Library Growth Over Time')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Books with dates will appear in this timeline")
                
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()