import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer

from sakila import query

st.set_page_config(page_title="Find similar films", page_icon="🔎")
st.title("🔎 Find similar films")


@st.cache_resource
def load_model():
    """TODO 7: load and return the sentence embedding model all-MiniLM-L6-v2 (Week 7, Day 2)."""
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource
def film_vectors():
    """TODO 8: read the title, description and rating of every film, embed the descriptions
    (normalised), and return the DataFrame and the vectors."""
    films = query("SELECT title, description, rating FROM film")
    model = load_model()
    embeddings = model.encode(films["description"].tolist(), normalize_embeddings=True)
    return films, embeddings


# TODO 9: a st.text_area for the customer's description and a st.button("Get your recommendations").
#         When it is clicked: warn if the text is empty; otherwise embed it, compute the cosine similarity
#         with every film (a dot product, since the vectors are normalised), and show the top 3 films
#         with their title, rating and similarity.
st.text_area("Describe the film you want to watch", key="description", 
             placeholder="A thoughtful drama about a monk who discovers a shark in Australia")
if st.button("Get your recommendations"):
    if not st.session_state.description:
        st.warning("Please describe a film first.")
    else:
        films, embeddings = film_vectors()
        model = load_model()
        query_vector = model.encode(st.session_state.description, normalize_embeddings=True)
        similarities = np.dot(embeddings, query_vector)
        top_indices = np.argsort(similarities)[-3:][::-1]
        top_films = films.iloc[top_indices]
        top_films["similarity"] = similarities[top_indices]
        st.dataframe(top_films[["title", "rating", "similarity"]])

        for _, film in top_films.iterrows():
            st.markdown(
                f"**{film['title'].title()}** · Rating: {film['rating']} · "
                f"Similarity: {film['similarity']:.2f}"
            )
