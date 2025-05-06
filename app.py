# app.py
import streamlit as st
from recommender import recommend  # Import the recommend function

# Set the title of the app
st.title("Music Recommendation System")

# Create an input field for the song name
song_name = st.text_input("Enter a song name:")

# Ask the user to select a recommendation method (content-based or collaborative)
method = st.radio("Choose recommendation method:", ("content", "collab"))

# When the user clicks the "Get Recommendations" button
if st.button("Get Recommendations"):
    if song_name:
        # Get recommendations using the selected method
        recommendations = recommend(song_name, method=method, top_n=5)
        
        # Check if the recommendation function returned a message or actual songs
        if isinstance(recommendations, str):
            st.write(recommendations)  # If it's a string (e.g., "track not found"), display the message
        else:
            # Display the recommendations in a nice format
            st.write("Here are 5 similar songs:")
            for idx, row in recommendations.iterrows():
                st.write(f"**{row['name']}** (Popularity: {row['popularity']})")
    else:
        st.write("Please enter a song name.")
