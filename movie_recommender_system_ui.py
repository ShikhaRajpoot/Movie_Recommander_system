import streamlit as st
import pickle
import pandas as pd
import requests  # to hit API

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=b1a477e87a043dd4b7cae52e46455381&language=en-US'
        .format(movie_id))
    data = response.json()  # convert this into json
    return 'https://image.tmdb.org/t/p/w500' + data['poster_path']

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
selected_movie_name = movies['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommand(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommanded_movies = []
    recommanded_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id

        recommanded_movies.append(movies.iloc[i[0]]['title'])

        # fetch poster through API.
        recommanded_movies_poster.append(fetch_poster(movie_id))
    return recommanded_movies, recommanded_movies_poster

st.title('Movie Recommender System')
option = st.selectbox('How would you like to be contacted?', selected_movie_name)

if st.button('Recommend'):
    name, poster = recommand(option)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(name[0])
        st.image(poster[0])

    with col2:
        st.text(name[1])
        st.image(poster[1])

    with col3:
        st.text(name[2])
        st.image(poster[2])

    with col4:
        st.text(name[3])
        st.image(poster[3])

    with col5:
        st.text(name[4])
        st.image(poster[4])
