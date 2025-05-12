import requests
import csv
import time

API_KEY = '56199b73711159f8d57800efd879f45a'  # <-- your TMDB API key here
BASE_URL = 'https://api.themoviedb.org/3'

def fetch_movies(page):
    url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=en-US&page={page}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f"Failed to fetch page {page}: {response.status_code}")
        return []

def save_movies(movies, filename="movies.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'id', 'title', 'overview', 'genres',
            'vote_average', 'vote_count', 'popularity', 'poster_path'
        ])
        for movie in movies:
            genres = [str(genre_id) for genre_id in movie.get('genre_ids', [])]
            writer.writerow([
                movie['id'],
                movie['title'],
                movie.get('overview', ''),
                ",".join(genres),
                movie.get('vote_average', 0),
                movie.get('vote_count', 0),
                movie.get('popularity', 0),
                movie.get('poster_path', '')
            ])

def main():
    all_movies = []
    pages = 500  # ~10,000 movies max
    for page in range(1, pages + 1):
        print(f"Fetching page {page}...")
        movies = fetch_movies(page)
        if not movies:
            break
        all_movies.extend(movies)
        time.sleep(0.25)
    save_movies(all_movies)
    print(f"✅ Saved {len(all_movies)} movies to movies.csv")

if __name__ == "__main__":
    main()


