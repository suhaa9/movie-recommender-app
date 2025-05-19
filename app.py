import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

# TMDB API key
API_KEY = "41e8922b30e15d18352e72d9b5ed8364"

# Load dataset
df = pd.read_csv('IMDb_All_Genres_etf_clean1.csv')
df.dropna(subset=['Movie_Title', 'main_genre', 'side_genre', 'Director', 'Actors'], inplace=True)

# Combine important tags
df['tags'] = (
    df['main_genre'].astype(str) + ' ' +
    df['side_genre'].astype(str) + ' ' +
    df['Director'].astype(str) + ' ' +
    df['Actors'].astype(str)
).str.lower()

# Vectorize tags
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(df['tags']).toarray()
similarity = cosine_similarity(vectors)

# Fetch poster from TMDB
def fetch_poster_by_title(title):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
    response = requests.get(search_url).json()
    results = response.get("results")
    if results and results[0].get("poster_path"):
        return f"https://image.tmdb.org/t/p/w500/{results[0]['poster_path']}"
    return ""

# Fetch movie details from TMDB
def fetch_movie_details(title):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
    response = requests.get(search_url).json()
    results = response.get("results", [])
    if not results:
        return None
    movie_id = results[0]['id']
    details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    details = requests.get(details_url).json()
    return {
        "title": details.get('title', ''),
        "overview": details.get('overview', 'No overview available.'),
        "genres": [genre['name'] for genre in details.get('genres', [])],
        "poster_path": "https://image.tmdb.org/t/p/w500" + details.get('poster_path', '')
    }

# Recommendation logic
def recommend(movie, genre_filter="All"):
    movie = movie.lower()
    details_dict = {}

    if movie in df['Movie_Title'].str.lower().values:
        idx = df[df['Movie_Title'].str.lower() == movie].index[0]
        movie_vector = vectors[idx]
        similarity_scores = cosine_similarity([movie_vector], vectors).flatten()

        if genre_filter != "All":
            filtered_indices = df[df['main_genre'] == genre_filter].index
            similarity_scores = [similarity_scores[i] if i in filtered_indices else -1 for i in range(len(similarity_scores))]

        similar_indices = sorted(range(len(similarity_scores)), key=lambda i: similarity_scores[i], reverse=True)[1:6]
        recommended_movies = df.iloc[similar_indices]['Movie_Title'].values

        for title in recommended_movies:
            detail = fetch_movie_details(title)
            if detail:
                details_dict[title] = detail
        return details_dict

    else:
        # Fallback to TMDB
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie}"
        response = requests.get(search_url).json()
        results = response.get("results", [])
        if not results:
            return {}
        movie_id = results[0]['id']
        rec_url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={API_KEY}&language=en-US"
        rec_response = requests.get(rec_url).json()
        rec_results = rec_response.get("results", [])[:5]
        for m in rec_results:
            title = m['title']
            detail = fetch_movie_details(title)
            if detail:
                details_dict[title] = detail
        return details_dict

# --- Streamlit UI Setup ---
st.title("🎬 Movie Recommender System")

# Custom layout and spacing fixes
st.markdown("""
<style>
img {
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
    display: block;
}
[data-testid="column"] {
    padding: 0rem !important;
    margin: 0rem !important;
    background-color: transparent !important;
}
.css-1v0mbdj, .css-1kyxreq, .stImage {
    padding: 0 !important;
    margin: 0 !important;
    background-color: transparent !important;
    box-shadow: none !important;
    border: none !important;
}
.css-1fcdlhq {
    gap: 0px !important;
}
section.main > div {
    padding-top: 0rem;
    padding-bottom: 0rem;
}
</style>
""", unsafe_allow_html=True)

# Genre filter
genre_filter = st.selectbox(
    "Filter by genre (optional)",
    ["All"] + sorted(df['main_genre'].dropna().unique().tolist())
)

# Movie input
movie = st.text_input("Enter a movie title:")

# --- Recommendation Display ---
if movie:
    recommended = recommend(movie, genre_filter=genre_filter)

    if recommended:
        st.markdown("### Recommended Movies")

        cols = st.columns(len(recommended))

        for i, (title, detail) in enumerate(recommended.items()):
            with cols[i]:
                st.image(detail["poster_path"], use_container_width=True)
                st.markdown(
                    f"<p style='text-align:center; font-size:14px; font-weight:bold; margin:8px 0 4px;'>{title}</p>",
                    unsafe_allow_html=True
                )
                if st.button("View Details", key=f"btn_{i}"):
                    st.session_state['selected_movie'] = detail

        if 'selected_movie' in st.session_state:
            selected = st.session_state['selected_movie']
            st.markdown("---")
            st.markdown("## 🎥 Movie Details")
            st.image(selected['poster_path'], width=300)
            st.markdown(f"**Title:** {selected['title']}")
            st.markdown(f"**Genres:** {', '.join(selected['genres'])}")
            st.markdown(f"**Overview:** {selected['overview']}")
    else:
        st.warning("No recommendations found.")
else:
    st.info("Enter a movie title to begin.")
