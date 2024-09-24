import streamlit as st
import pickle 
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from starlette.responses import RedirectResponse




def add_bg_from_local():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://i.pinimg.com/originals/d5/6f/4d/d56f4ddeacfafae7650b5e1aa553f108.jpg");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local()

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello":"World"}

@app.get("/")
async def favicon():
    return RedirectResponse(url="/")

def fetch_poster(anime_id):
    if not anime_id:
        print("Anime ID is Not Found.")
        return None
    
    anime_url = f"https://myanimelist.net/anime/{anime_id}"
    try:
        response = requests.get(anime_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content,'html.parser')
        poster_img = soup.find('img', {'class':  'lazyload'})

        if poster_img:
            poster_url = poster_img.get('data-src') or poster_img.get('src')
            if poster_url:
                return poster_url
            else:
                print("poster url not found in image attribute")
                return None
        else:
            print("poster image not found.")
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"failed to retrive anime page.Error:{e}")
        return None
    

def recommend(anime):
    index = animes[animes['title']==anime].index[0]
    dis = sorted(list(enumerate(similarity[index])), reverse = True, key = lambda vector:vector[1])
    recommend_animes=[]
    recommend_poster=[]
    for i in dis[1:6]:
        anime_id = animes.iloc[i[0]]['id']
        if anime_id:
            poster_url = fetch_poster(anime_id)
            if poster_url:
              recommend_animes.append(animes.iloc[i[0]].title)
              recommend_poster.append(poster_url)
    return recommend_animes, recommend_poster
       
st.header("Anime Recommendation System")
animes = pickle.load(open("anime_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))

anime_list = animes['title'].values
select_values = st.selectbox("Select animes from dropdown", anime_list)

if st.button("Show Recommend"):
    recommend_anime, recommend_poster = recommend(select_values)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommend_anime[0])
        st.image(recommend_poster[0], width = 100)
    with col2:
        st.text(recommend_anime[1])
        st.image(recommend_poster[1], width = 100)
    with col3:
        st.text(recommend_anime[2])
        st.image(recommend_poster[2], width= 100)
    with col4:
        st.text(recommend_anime[3])
        st.image(recommend_poster[3], width = 100)
    with col5:
        st.text(recommend_anime[4])
        st.image(recommend_poster[4], width = 100)

