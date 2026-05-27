import pickle
import streamlit as st
import requests
from utils.trailer import open_trailer

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

body {
    background-color: #0e1117;
}

.main {
    background: linear-gradient(to bottom, #141414, #0e1117);
    color: white;
}

.title {
    font-size: 60px;
    font-weight: bold;
    color: #E50914;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #bbbbbb;
    margin-bottom: 40px;
    font-size: 20px;
}

.stSelectbox label {
    color: white !important;
    font-size: 18px !important;
}

div[data-baseweb="select"] {
    background-color: #1f1f1f !important;
    border-radius: 12px !important;
}

.stButton>button {
    width: 100%;
    background-color: #E50914;
    color: white;
    font-size: 18px;
    font-weight: bold;
    border-radius: 12px;
    padding: 12px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #ff1f1f;
    transform: scale(1.02);
}

.movie-card {
    background-color: #181818;
    border-radius: 15px;
    padding: 10px;
    transition: 0.3s;
    text-align: center;
    height: 100%;
}

.movie-card:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 15px rgba(255,255,255,0.2);
}

.movie-title {
    color: white;
    font-size: 17px;
    font-weight: bold;
    margin-top: 10px;
}

.rating {
    color: #46d369;
    font-size: 15px;
    margin-top: 5px;
}

.hero {
    background-image: url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=1974&auto=format&fit=crop');
    background-size: cover;
    background-position: center;
    padding: 80px 40px;
    border-radius: 20px;
    margin-bottom: 30px;
}

.hero-text {
    font-size: 50px;
    font-weight: bold;
    color: white;
}

.hero-sub {
    color: #dddddd;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- FUNCTIONS ----------------
def fetch_movie_details(movie_title):
    api_key = "7841e9dd"
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        poster = data.get("Poster")
        if not poster or poster == "N/A":
            poster = "https://via.placeholder.com/500x750?text=No+Poster"

        return {
            "poster": poster,
            "rating": data.get("imdbRating", "N/A"),
            "year": data.get("Year", "N/A"),
            "genre": data.get("Genre", "N/A"),
            "plot": data.get("Plot", "No description available")
        }

    except:
        return {
            "poster": "https://via.placeholder.com/500x750?text=Error",
            "rating": "N/A",
            "year": "N/A",
            "genre": "N/A",
            "plot": "No description available"
        }


@st.cache_data

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommendations = []

    for i in distances[1:11]:
        movie_title = movies.iloc[i[0]].title
        details = fetch_movie_details(movie_title)

        recommendations.append({
            "title": movie_title,
            "poster": details['poster'],
            "rating": details['rating'],
            "year": details['year'],
            "genre": details['genre'],
            "plot": details['plot']
        })

    return recommendations


# ---------------- LOAD DATA ----------------
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_list = movies['title'].values


# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero">
    <div class="hero-text">Unlimited Movies, Recommendations & Fun.</div>
    <div class="hero-sub">
        Discover movies similar to your favorites instantly 🍿
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------- TITLE ----------------
st.markdown('<div class="title">MOVIE RECOMMENDER</div>', unsafe_allow_html=True)

# ---------------- SEARCH ----------------
selected_movie = st.selectbox(
    "Search Your Favorite Movie",
    movie_list
)
if st.button("▶ Watch Trailer"):
    open_trailer(selected_movie)


# ---------------- MAIN MOVIE DETAILS ----------------
movie_details = fetch_movie_details(selected_movie)

col1, col2 = st.columns([1, 2])

with col1:
    st.image(movie_details['poster'])
with col2:

    st.markdown(f"""
    <style>

    .movie-title {{
        font-size: 42px;
        font-weight: 600;
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 18px;
        letter-spacing: 1px;
    }}

    .movie-detail {{
        font-size: 18px;
        font-family: 'Poppins', sans-serif;
        color: #dddddd;
        margin-bottom: 12px;
        line-height: 1.7;
        padding: 8px 12px;
        border-radius: 10px;
        background: rgba(255,255,255,0.03);
    }}

    .rating {{
        color: #FFD700;
        font-weight: 500;
    }}

    .year {{
        color: #00BFFF;
        font-weight: 500;
    }}

    .genre {{
        color: #FF69B4;
        font-weight: 500;
    }}

    .plot {{
        color: #00FFAA;
        font-weight: 500;
    }}

    </style>

    <div class="movie-title">
        🎬 {selected_movie}
    </div>

    <div class="movie-detail">
        ⭐ <span class="rating">IMDb Rating:</span>
        {movie_details['rating']}
    </div>

    <div class="movie-detail">
        📅 <span class="year">Year:</span>
        {movie_details['year']}
    </div>

    <div class="movie-detail">
        🎭 <span class="genre">Genre:</span>
        {movie_details['genre']}
    </div>

    <div class="movie-detail">
        📝 <span class="plot">Plot:</span>
        {movie_details['plot']}
    </div>

    """, unsafe_allow_html=True)
# ---------------- RECOMMEND BUTTON ----------------
if st.button('🎬 Show Recommendations'):

    recommendations = recommend(selected_movie)

    st.markdown("## Recommended For You")

    cols = st.columns(5)

    for idx, movie in enumerate(recommendations[:5]):

        with cols[idx]:
            st.markdown(f"""
            <div class="movie-card">
                <img src="{movie['poster']}" width="100%" style="border-radius:10px;">
                <div class="movie-title">{movie['title']}</div>
                <div class="rating">⭐ {movie['rating']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    cols2 = st.columns(5)

    for idx, movie in enumerate(recommendations[5:10]):

        with cols2[idx]:
            st.markdown(f"""
            <div class="movie-card">
                <img src="{movie['poster']}" width="100%" style="border-radius:10px;">
                <div class="movie-title">{movie['title']}</div>
                <div class="rating">⭐ {movie['rating']}</div>
            </div>
            """, unsafe_allow_html=True)


# ---------------- FOOTER ----------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    "<center style='color:gray;'>Made with ❤️ Akansha Kumari",
    unsafe_allow_html=True
)

