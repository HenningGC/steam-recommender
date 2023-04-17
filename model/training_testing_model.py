import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

from scipy import sparse
from scipy.spatial import distance

from lightfm import LightFM
from lightfm.evaluation import precision_at_k, auc_score

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import TSNE

from gensim.models.keyedvectors import WordEmbeddingsKeyedVectors

from resources import *

# ignore warnings
warnings.filterwarnings("ignore")

# Load user items data
recdata = pd.read_csv('../Data/steam/recdata.csv', index_col=0).rename(columns={'variable': 'id', 'value': 'owned'})

# Load games data
gamesdata = pd.read_csv('gamesdata.csv', index_col=0)

# Use create_interaction_matrix function
interactions = create_interaction_matrix(df=recdata, user_col='uid', item_col='id', rating_col='owned')

# Define train and test sets
train_num = round((80 / 100) * len(interactions))
train = interactions[:train_num]
test = interactions[train_num:]

# Create user dictionary using helper function
user_dict = create_user_dict(interactions=interactions)

# Create game dictionary using helper function
games_dict = create_item_dict(df=gamesdata, id_col='id', name_col='title')

# Create sparse matrices for evaluation
train_sparse = sparse.csr_matrix(train.values)
test_sparse = sparse.csr_matrix(test.values)

# Add X users to Test so that the number of rows in Train match Test
N = train.shape[0]  # Rows in Train set
n, m = test.shape  # Rows & columns in Test set
z = np.zeros([(N - n), m])  # Create the necessary rows of zeros with m columns
test = np.vstack((test, z))  # Vertically stack Test on top of the blank users
test_sparse = sparse.csr_matrix(test)

# Instantiate and fit model on full interactions set
mf_model = run_model(interactions=interactions, n_components=30, loss='warp', epoch=30, n_jobs=4)

# Get embeddings
embeddings = mf_model.item_embeddings

# Get game names
game_names = [games_dict[id] for id in interactions.columns]

# Get similarity matrix
similarity_matrix = cosine_similarity(embeddings)

# Find games similar to Counter-Strike
idx = game_names.index('Counter-Strike')
similar_games = np.argsort(-similarity_matrix[idx])[:10]
print('Games similar to Counter-Strike:')
for i in similar_games:
    print(game_names[i])
    
# Find games similar to Half-Life 2
idx = game_names.index('Half-Life 2')
similar_games = np.argsort(-similarity_matrix[idx])[:10]
print('\nGames similar to Half-Life 2:')
for i in similar_games:
    print(game_names[i])
# Get data for both games
selected_games = gamesdata.loc[gamesdata['title'].isin(['Counter-Strike', 'Left 4 Dead 2'])]

# Obtain embeddings vector for Counter-Strike
cs_index = selected_games[selected_games['title'] == 'Counter-Strike'].index[0]
cs_vector = embeddings[cs_index]
cs_vector

# Retrieve game id for Left 4 Dead 2
lfd2_id = selected_games[selected_games['title'] == 'Left 4 Dead 2']['id'].values[0]

# Obtain index for Left 4 Dead 2 in interactions matrix
lfd2_index = list(interactions.columns).index(lfd2_id)

# Obtain embeddings vector for Left 4 Dead 2
lfd2_vector = embeddings[lfd2_index]
lfd2_vector

# Compute Euclidean distance
from scipy.spatial import distance
distance.euclidean(cs_vector, lfd2_vector)

# Get data for both games
selected_games = gamesdata.loc[gamesdata['title'].isin(['Counter-Strike', 'The Room'])]

# Retrieve game id for The Room
room_id = selected_games[selected_games['title'] == 'The Room']['id'].values[0]

# Obtain index for The Room in interactions matrix
room_index = list(interactions.columns).index(room_id)

# Obtain embeddings vector for The Room
room_vector = embeddings[room_index]
room_vector

# Compute Euclidean distance
distance.euclidean(cs_vector, room_vector)

# Compute cosine similarity
distance.cosine(cs_vector, lfd2_vector)
distance.cosine(cs_vector, room_vector)

# Create instance
from gensim.models import KeyedVectors
kv = KeyedVectors(embeddings.shape[1])

# Add embeddings to kv
kv.add(gameslist, embeddings)

# Get games closest to Counter-Strike
kv.most_similar('Counter-Strike')

# Get games closest to Left 4 Dead 2
kv.most_similar('Left 4 Dead 2')

# Get games closest to The Room
kv.most_similar('The Room')

# Get games closest to RollerCoaster Tycoon
kv.most_similar('RollerCoaster Tycoon®: Deluxe')

# Get games closest to Dishonored
kv.most_similar('Dishonored')

# Get games closest to The Jackbox Party Pack
kv.most_similar('The Jackbox Party Pack')

# Get games closest to American Truck Simulator
kv.most_similar('American Truck Simulator')

def plot_similar(item, ax, topn=5):
    '''
    Plots a bar chart of similar items
    Arguments:
        - item, string
        - ax, axes on which to plot
        - topn (default = 5) number of similar items to plot
    '''
    sim = kv.most_similar(item, topn=topn)[::-1]
    y = np.arange(len(sim))
    w = [t[1] for t in sim]
    ax.barh(y, w)
    left = min(.6, min(w))
    ax.set_xlim(right=1.0, left=left)
    # Split long titles over multiple lines
    labels = [textwrap.fill(t[0] , width=24) for t in sim]
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_title(item)  

# Define list of games to visualise similar items for
games = ['Counter-Strike', 'The Room', 'RollerCoaster Tycoon®: Deluxe', 'Dishonored', 'The Jackbox Party Pack', 'American Truck Simulator']

# Set figure/axes to have 3 rows with 2 columns
fig, axes = plt.subplots(3, 2, figsize=(15, 9))

# Loop through games and use plot_similar function 
for game, ax in zip(games, axes.flatten()):
    plot_similar(game, ax)
    
fig.tight_layout()

# Instantiate tsne, specify cosine metric
tsne = TSNE(random_state=0, n_iter=1000, metric='cosine')

# Fit and transform
embeddings2d = tsne.fit_transform(embeddings)

# Create DataFrame with the game name and 2d embeddings
embeddingsdf = pd.DataFrame()
embeddingsdf['game'] = gameslist
embeddingsdf['x'] = embeddings2d[:, 0]
embeddingsdf['y'] = embeddings2d[:, 1]

# Draw a scatterplot of the games
fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(embeddingsdf.x, embeddingsdf.y, alpha=.1)
plt.title('Scatter plot of games using t-SNE')
plt.show()

# Check if games we expect to be close are indeed close in this 2-dimensional space
match = embeddingsdf[embeddingsdf.game.str.contains('RollerCoaster')]
fig, ax = plt.subplots(figsize=(10, 8))
Xlabeled = embeddings2d[match.index, 0]
Ylabeled = embeddings2d[match.index, 1]
labels = match['game'].values
for x, y, label in zip(Xlabeled, Ylabeled, labels):
    ax.scatter(x, y, marker='1', label=label, s=90, color='red')
ax.scatter(embeddingsdf.x, embeddingsdf.y, alpha=.1)
plt.title('Scatter plot of games using t-SNE')
plt.legend()
plt.show
