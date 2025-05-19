# 🎬 Movie Recommender App

This is a content-based Movie Recommender System built with **Streamlit**, using movie metadata (genres, actors, director) and **cosine similarity** to suggest similar movies. It also integrates with **TMDB API** to display movie posters and additional details.

## 🚀 Features

- Recommend movies based on title, genre, director, and actors
- Optional genre filtering
- Fetch movie posters and descriptions from **TMDB**
- Beautiful UI with Streamlit
- Fallback TMDB recommendations if the movie is not found in the local dataset

## 🧠 Technologies Used

- Python
- Pandas, Scikit-learn
- Streamlit
- TMDB API

## 📂 Dataset

- CSV File: `IMDb_All_Genres_etf_clean1.csv`
- Contains movie titles, genres, directors, and actor details

## 🛠️ How to Run Locally

1. **Clone the repo**
```bash
git clone https://github.com/suhaa9/movie-recommender-app.git
cd movie-recommender-app

Install dependencies
pip install -r requirements.txt

Run the app
streamlit run app.py
Open http://localhost:8501 in your browser.

🌐 Live Demo (Coming soon)
Once deployed on Streamlit Cloud, you’ll be able to access it here:
https://movie-recommender-app.streamlit.app (placeholder link)

🔑 TMDB API Key
Make sure to include your TMDB API key in the app.py file:
API_KEY = "your_tmdb_api_key_here"

🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

📧 Contact
Made with ❤️ by Suha Saleem
