import tkinter as tk
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

root = tk.Tk()
root.title("Movie Genre Prediction")


def predict_genre():
    try:
        rating = float(entry_rating.get())
        views = int(entry_views.get())

        keyword = entry_keyword.get()
        params = {"keyword": keyword}

        url = "https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword"
        api_key = "71c5dd47-2ab2-40d4-bb00-4974097af5b6"
        headers = {"X-API-KEY": api_key}

        response = requests.get(url, params=params, headers=headers)
        films_data = response.json()

        if 'films' in films_data and isinstance(films_data['films'], list):
            films_info = films_data['films']
            print(films_info)
            films_with_genres = [film for film in films_info if 'genres' in film]
            genres = [genre['genre'] for film in films_with_genres for genre in film['genres']]
            film_ratings = [(film.get('rating', 0)) for film in films_with_genres]
            ratings_filtered = [float(rating) if rating != 'null' else 0 for rating in film_ratings]


            print(ratings_filtered)


            rating_vote_count = [film.get('ratingVoteCount', 0) for film in films_with_genres]

            films_info_new = [{
                'rating': ratings_filtered[i],
                'ratingVoteCount': rating_vote_count[i],
                'genre': genres[i] if i < len(genres) else 'Unknown'
            } for i in range(len(films_with_genres))]
            print(films_info_new)

            X = [[film['rating'], film['ratingVoteCount']] for film in films_info_new]
            y = [film['genre'] for film in films_info_new]

            random_forest = RandomForestClassifier(n_estimators=100)
            random_forest.fit(X, y)

            predicted_genre = random_forest.predict([[rating, views]])
            result_label.config(text=f"Predicted genre: {predicted_genre}")

        else:
            result_label.config(text="Error: Incorrect movie data from API")
    except ValueError:
        result_label.config(text="Error: Please enter valid values")


label_keyword = tk.Label(root, text="Введите ключевое слово фильма:")
label_keyword.pack()
entry_keyword = tk.Entry(root)
entry_keyword.pack()

label_rating = tk.Label(root, text="Введите рейтинг фильма:")
label_rating.pack()
entry_rating = tk.Entry(root)
entry_rating.pack()

label_views = tk.Label(root, text="Введите количество отзывов:")
label_views.pack()
entry_views = tk.Entry(root)
entry_views.pack()

predict_button = tk.Button(root, text="Получить данные и предсказать жанр", command=predict_genre)
predict_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()


root.mainloop()