import pickle
from lightfm import LightFM
import json

from .helper.helpers import generate_interactions
from .helper.helpers import get_gamesdata
from .helper.helpers import create_user_dict
from .helper.helpers import create_item_dict
from .helper.helpers import get_recs
from .helper.helpers import export_recommendations


def generate_recommendations(id):
    with open(r'backend-engine-main\recommendation_app\models\mf_model.pkl', 'rb') as f:
        mf_model = pickle.load(f)

    with open(r'backend-engine-main\recommendation_app\data\user_dict.pkl', 'rb') as f:
        user_dict = pickle.load(f)

    with open(r'backend-engine-main\recommendation_app\data\games_dict.pkl', 'rb') as f:
        games_dict = pickle.load(f)

    interactions = generate_interactions()

    users = user_dict
    items = games_dict

    recommendations = get_recs(model = mf_model, 
                    interactions = interactions, 
                    user_id = id, 
                    user_dict = users,
                    item_dict = items, 
                    threshold = 0,
                    num_items = 5,
                    show_known = True, 
                    show_recs = True)
    export_recommendations(recommendations)
    return recommendations