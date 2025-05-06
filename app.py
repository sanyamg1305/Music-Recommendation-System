import streamlit as st
from recommender import recommend

# Page configuration
st.set_page_config(page_title="Music Recommender 🎧", page_icon="🎶", layout="centered")

# App header
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🎵 Music Recommender 🎵</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>Discover songs similar to your favorites</p>", unsafe_allow_html=True)

# Text input
song_input = st.text_input("🔍 Enter a song name you like:", placeholder="e.g. Shape of You")

# Button and logic
if st.button("🎧 Recommend Songs"):
    if song_input.strip() == "":
        st.warning("⚠️ Please enter a song name.")
    else:
        results = recommend(song_input.strip())
        if results:
            st.success(f"🎶 Here are songs similar to **{song_input}**:")
            st.markdown("<ul style='line-height: 2;'>", unsafe_allow_html=True)
            for idx, song in enumerate(results, 1):
                st.markdown(f"<li><b>{idx}. {song}</b></li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)
        else:
            st.error(f"🤷‍♂️ Hmm... we couldn't find **{song_input}** in our playlist.")
            st.markdown("Try another song — maybe this one hasn’t hit our radar yet. 👽")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 13px;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)