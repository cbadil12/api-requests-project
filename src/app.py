# ===============================================================
# IMPORTS
# ===============================================================
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# ===============================================================
# INPUTS
# ===============================================================
artist_uri = "5TYxZTjIPqKM8K8NuP9woO" # C. Tangana
num_top_tracks = 30
popularity_top = 3

# ===============================================================
# LOAD ENVIROMENT VARIABLES
# ===============================================================
# Absolute path for file .env in project's root
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
# load the .env file variables
load_dotenv(env_path)
# Get credential values
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

# ===============================================================
# CONNECT TO SPOTIFY API
# ===============================================================
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(auth_manager=auth_manager)

# ===============================================================
# GET TRACKS
# ===============================================================
artist_name = spotify.artist(artist_id=artist_uri)
artist_name = artist_name["name"]
top_tracks = spotify.artist_top_tracks(artist_id=artist_uri)
top_tracks = top_tracks["tracks"][:num_top_tracks]

# ===============================================================
# BUILD DATAFRAME
# ===============================================================
top_tracks_name = []
top_tracks_popularity = []
top_tracks_duration = []
for track in top_tracks:
    name = track["name"]
    popularity = track["popularity"]
    duration_min = track["duration_ms"] / 1000 / 60   # Convert ms → min
    top_tracks_name.append(name)
    top_tracks_popularity.append(popularity)
    top_tracks_duration.append(duration_min)

top_tracks_df = pd.DataFrame({
    "name": top_tracks_name,
    "popularity": top_tracks_popularity,
    "duration_min": top_tracks_duration
})

# ===============================================================
# TOP POPULAR TRACKS
# ===============================================================
print(f"TOP tracks by {artist_name}:\n {top_tracks_df} \n\n")
top_popular_tracks_df = top_tracks_df.sort_values("popularity",ascending=False)[:3]
print(f"TOP {popularity_top} popular tracks by {artist_name}:\n {top_popular_tracks_df} \n")

# ALL VARIABLES HEATMAP
corr_matrix = top_tracks_df[["popularity", "duration_min"]].corr()
corr_order = corr_matrix.mean().sort_values(ascending=False).index
corr_matrix = corr_matrix.loc[corr_order, corr_order]

fig, axes = plt.subplots(nrows=1,ncols=2,figsize=(8, 8))

sns.heatmap(
    ax= axes[0],
    data=corr_matrix,
    annot=True,
    vmin=-1,
    vmax=1,
    fmt=".2f",
    annot_kws={"size": 20}
).set_title("CORRELATION", fontsize=30, fontweight="bold")

sns.scatterplot(
    ax= axes[1],
    data=top_tracks_df,
    x="duration_min",
    y="popularity",
    hue="name",
    size="name").set_title("SCATTER", fontsize=30, fontweight="bold")

plt.tight_layout()
plt.show()