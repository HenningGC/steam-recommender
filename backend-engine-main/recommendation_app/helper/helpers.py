import pandas as pd
from lightfm import LightFM
from scipy import sparse
from scipy.sparse import csr_matrix
import numpy as np
import json
import pickle

def create_interaction_matrix(df,user_col, item_col, rating_col, norm= False, threshold = None):
    '''
    Creates an interaction matrix DataFrame
    Arguments:
        df = Pandas DataFrame containing user-item interactions
        user_col = column name containing user's identifier
        item_col = column name containing item's identifier
        rating col = column name containing user rating on given item
        norm (optional) = True if a normalization of ratings is needed
        threshold (required if norm = True) = value above which the rating is favorable
    Returns:
        Pandas DataFrame with user-item interactions
    '''
    interactions = df.groupby([user_col, item_col])[rating_col] \
            .sum().unstack().reset_index(). \
            fillna(0).set_index(user_col)
    if norm:
        interactions = interactions.applymap(lambda x: 1 if x > threshold else 0)
    return interactions

def create_user_dict(interactions):
    '''
    Creates a user dictionary based on their index and number in interaction dataset
    Arguments:
        interactions - DataFrame with user-item interactions
    Returns:
        user_dict - Dictionary containing interaction_index as key and user_id as value
    '''
    user_id = list(interactions.index)
    user_dict = {}
    counter = 0 
    for i in user_id:
        user_dict[i] = counter
        counter += 1
    return user_dict

def create_item_dict(df,id_col,name_col):
    '''
    Creates an item dictionary based on their item_id and item name
    Arguments: 
        - df = Pandas dataframe containing item information
        - id_col = column name containing unique identifier for an item
        - name_col = column name containing name of the item
    Returns:
        item_dict = Dictionary containing item_id as key and item_name as value
    '''
    item_dict ={}
    for i in range(df.shape[0]):
        item_dict[(df.loc[i,id_col])] = df.loc[i,name_col]
    return item_dict

def run_model(interactions, n_components=30, loss='warp', epoch=30, n_jobs = 4):
    '''
    Runs matrix-factorization model using LightFM
    Arguments:
        interactions = Pandas DataFrame containing user-item interactions
        n_components = number of desired embeddings to create to define item and user
        loss = loss function other options are logistic, brp
        epoch = number of epochs to run 
        n_jobs = number of cores used for execution 
    Returns:
        Model = Trained model
    '''
    x = sparse.csr_matrix(interactions.values)
    model = LightFM(no_components= n_components, loss=loss)
    model.fit(x,epochs=epoch,num_threads = n_jobs)
    return model


def get_recs(model, interactions, user_id, user_dict, 
                               item_dict,threshold = 0,num_items = 10, show_known = True, show_recs = True):
    '''
    Produces user recommendations
    Arguments:
        model = Trained matrix factorization model
        interactions = dataset used for training the model
        user_id = user ID for which we need to generate recommendation
        user_dict = Dictionary containing interaction_index as key and user_id as value
        item_dict = Dictionary containing item_id as key and item_name as value
        threshold = value above which the rating is favorable in new interaction matrix
        num_items = Number of recommendations to provide
        show_known (optional) - if True, prints known positives
        show_recs (optional) - if True, prints list of N recommended items  which user hopefully will be interested in
    Returns:
        list of titles user_id is predicted to be interested in 
    '''
    n_users, n_items = interactions.shape
    # Get value for user_id using dictionary
    user_x = user_dict[user_id]
    # Generate predictions
    scores = pd.Series(model.predict(user_x,np.arange(n_items)))
    # Get top predictions
    scores.index = interactions.columns
    scores = list(pd.Series(scores.sort_values(ascending=False).index))
    # Get list of known values
    known_items = list(pd.Series(interactions.loc[user_id,:] \
                                 [interactions.loc[user_id,:] > threshold].index).sort_values(ascending=False))
    # Ensure predictions are not already known
    scores = [x for x in scores if x not in known_items]
    # Take required number of items from prediction list
    return_score_list = scores[0:num_items]
    # Convert from item id to item name using item_dict
    known_items = list(pd.Series(known_items).apply(lambda x: item_dict[x]))
    scores = list(pd.Series(return_score_list).apply(lambda x: item_dict[x]))
    
    if show_known == True:
        print("Known Likes:")
        counter = 1
        for i in known_items:
            print(str(counter) + '- ' + i)
            counter+=1
            
    if show_recs == True:
        print("\n Recommended Items:")
        counter = 1
        for i in scores:
            print(str(counter) + '- ' + i)
            counter+=1
    return scores

def generate_interactions():
    recdata = pd.read_csv(r'backend-engine-main\recommendation_app\data\recdata.csv', index_col = 0)
    interactions = create_interaction_matrix(df = recdata,
                                         user_col = 'uid',
                                         item_col = 'id',
                                         rating_col = 'owned')
    return interactions

def get_gamesdata():
    gamesdata = pd.read_csv(r'backend-engine-main\recommendation_app\data\gamesdata.csv', index_col = 0)
    return gamesdata


def export_recommendations(recommendations):

    with open(r"backend-engine-main\recommendation_app\data\recommendations.txt", "wb") as file:
        pickle.dump(recommendations, file)