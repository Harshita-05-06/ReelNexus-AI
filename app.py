import streamlit as st
import pickle
import requests

OMDB_API_KEY = "106afd86"
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


movies = pickle.load(open('movies.pkl', 'rb'))

movies['tags'] = movies['tags'].fillna('')

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

similarity = cosine_similarity(vectors)

def fetch_poster(movie_title):
    try:
        clean_title = movie_title.split("(")[0].strip()

        url = f"http://www.omdbapi.com/?s={clean_title}&apikey={OMDB_API_KEY}"
        data = requests.get(url).json()

        if data.get("Search"):
            for item in data["Search"]:
                if item.get("Poster") and item["Poster"] != "N/A":
                    return item["Poster"]

    except:
        pass

    return "https://via.placeholder.com/300x450?text=No+Poster"

st.set_page_config(
    page_title="ReelNexus AI",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0b0b0f;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# NETFLIX STYLE GLOBAL UI
# =========================
st.markdown("""
<style>

/* Smooth overall UI */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* App background glow effect */
.stApp {
    background: radial-gradient(circle at top, #111122, #0b0b0f);
    color: white;
}

/* Movie title hover card effect */
div[data-testid="column"] {
    transition: transform 0.3s ease;
}

div[data-testid="column"]:hover {
    transform: scale(1.08);
    z-index: 2;
}

/* Button glow + animation */
div.stButton > button:first-child {
    background: linear-gradient(90deg, #7C4DFF, #448AFF);
    color: white;
    font-size: 16px;
    padding: 10px 24px;
    border-radius: 12px;
    border: none;
    transition: all 0.3s ease-in-out;
    box-shadow: 0px 0px 0px rgba(0,0,0,0);
}

div.stButton > button:hover {
    transform: scale(1.08);
    box-shadow: 0px 0px 20px rgba(124,77,255,0.8);
    background: linear-gradient(90deg, #651FFF, #2979FF);
}

/* Selectbox glow */
div[data-baseweb="select"] {
    border-radius: 10px;
    transition: 0.3s;
}

div[data-baseweb="select"]:hover {
    box-shadow: 0px 0px 15px rgba(124,77,255,0.6);
    transform: scale(1.01);
}

/* Poster hover zoom (IMPORTANT - Netflix feel) */
img {
    border-radius: 12px;
    transition: transform 0.35s ease, box-shadow 0.35s ease;
}

img:hover {
    transform: scale(1.18);
    box-shadow: 0px 15px 30px rgba(0,0,0,0.8);
    z-index: 10;
}

/* Recommendation title glow */
h2, h3 {
    text-shadow: 0px 0px 12px rgba(124,77,255,0.5);
}

/* Divider styling */
hr {
    border: 1px solid rgba(255,255,255,0.1);
}

</style>
""", unsafe_allow_html=True)
# -------------------------
# TITLE SECTION
# -------------------------
st.markdown(
    "<h1 style='text-align:center; color:#7C4DFF;'>🎬 ReelNexus AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; color:gray;'>Discover movies that match your vibe</p>",
    unsafe_allow_html=True
)

st.divider()

st.markdown("""
<style>
h1 {
    text-shadow: 0px 0px 25px rgba(124,77,255,0.8);
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)
# -------------------------
# SELECT MOVIE
# -------------------------
movie_list = movies['title'].values
selected_movie = st.selectbox("Search a movie you like:", movie_list)

st.write("")

# -------------------------
# BUTTON STYLE
# -------------------------
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #7C4DFF, #448AFF);
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 12px;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #651FFF, #2979FF);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="column"] div:hover {
    transform: scale(1.05);
    transition: 0.3s;
}
</style>
""", unsafe_allow_html=True)
# -------------------------
# RECOMMENDATION LOGIC PLACEHOLDER
# -------------------------
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
    except:
        return []
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies

# -------------------------
# ACTION
# -------------------------
if st.button("Recommend "):

    results = recommend(selected_movie)
    
    if len(results) == 0:
        st.error("No recommendation found. Try another movie")
    else:
        st.markdown("##  Recommended for you")

        cols = st.columns(5)

        for i, col in enumerate(cols):
            if i < len(results):
                with col:
                    poster = fetch_poster(results[i])

                    st.markdown(f"""
                        <div style="
                            background-color: #141414;
                            border-radius: 16px;
                            padding: 10px;
                            box-shadow: 0px 4px 20px rgba(0,0,0,0.6);
                            transition: transform 0.3s;
                        ">
                    """, unsafe_allow_html=True)

                    st.image(poster, use_container_width=True)

                    st.markdown(f"""
                        <p style="
                            text-align:center;
                            font-weight:600;
                            color:white;
                            margin-top:10px;
                        ">{results[i]}</p>
                        </div>
                    """, unsafe_allow_html=True)

st.markdown("""
    <hr>
    <div style="text-align:center; color:#888; font-size:13px;">
        Built by <b>Harshita Ramchandani</b> • 
        <a href="https://github.com/" target="_blank">GitHub</a>
    </div>
""", unsafe_allow_html=True)
