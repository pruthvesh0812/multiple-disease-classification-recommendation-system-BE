from dotenv import load_dotenv
from google_drive.drive_auth import list_blobs
from google_drive.drive_auth import create_file_dfs
from services import Predictor,RECOMMENDER
from models.user_model import User
import os

load_dotenv()

def main():
    list_blobs('major-project-bucket', os.getenv("PATH_TO_CREDENTIALS"))
    all_dataframes = create_file_dfs('major-project-bucket')
    predictor = Predictor()
    predictor.train_prediction_models(all_dataframes)
    recommend_diabetes = RECOMMENDER(all_dataframes['for_diabetes.csv'],'diabetes')
    recommend_diabetes.train()
    
    return [predictor,recommend_diabetes]