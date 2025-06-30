import pandas as pd
from sklearn.neighbors import NearestNeighbors
import joblib
import json
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

# load model and data paths
model_path = os.path.join(base_dir, "model.joblib")
csv_path = os.path.join(base_dir, "encoded_model.csv")


# load the trained model
knn = joblib.load(model_path)
model_data = pd.read_csv(csv_path)
model_data = model_data.set_index('Ticker')
feature_cols = model_data.columns


# user input should be in a dictionary format:
# {
#    'sector': 'Healthcare',
#    'marketCapLevel': 'high',
#    'growthValueType': 'growth',
#    'forwardPE': 15
# }
def get_recs(user_input):
    # encode user input
    user_df = pd.DataFrame([user_input])
    user_encoded = pd.get_dummies(user_df)
    user_encoded = user_encoded.reindex(columns=feature_cols, fill_value=0)

    # perform nn search
    distances, indices = knn.kneighbors(user_encoded.values)
    nearest_tickers = model_data.iloc[indices[0]].index.tolist()

    return json.dumps({'recs': nearest_tickers})


"""
testing:
inp = {
    'sector': 'Technology',
    'marketCapLevel': 'high',
    'growthValueType': 'growth',
    'forwardPE': 100
}

print(get_recs(inp))
"""