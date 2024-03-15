from flask import Flask, request, jsonify
# from dotenv import load_dotenv
# from google_drive.drive_auth import list_blobs
# from google_drive.drive_auth import create_file_dfs
# from services import Predictor,RECOMMENDER
# from models.user_model import User
# import os
# from google_drive.drive_auth import get_files_from_drive
app = Flask(__name__)

# service = authenticate_google_drive()

# load_dotenv()

# list_blobs('major-project-bucket', os.getenv("PATH_TO_CREDENTIALS"))
# all_dataframes = create_file_dfs('major-project-bucket')
# predictor = Predictor()
# predictor.train_prediction_models(all_dataframes)
# recommend_diabetes = RECOMMENDER('diabetes')
# recommend_diabetes.train()
from main import main

predictor, recommender = main()

# testing user - global
user1= User(NULL,NULL,NULL,NULL,NULL)

@app.route('/')
def home():
    return jsonify({"message": "Files listed successfully"})


@app.route('/create_user', methods=['POST'])
def predict():
    data = request.get_json()
    user1 = User("user_id_1","john","john@gmail.com",predictor,recommender)
    # prediction = predict_disease(data)
    return jsonify({"user_id":"user_id_1"}) 


@app.route('/create_user_lifestyle', methods=['POST'])
def create_user_lifestyle():
    data = request.get_json()
    if data == null:
        return jsonify({"message":"no data sent"})

    user1.create_Lifestyle(data.user_input_lifestyle,data.user_input_lifestyle_heart_stroke,data.user_input_lifestyle_stroke)
    user1.create_user_context(data.user_context)
    user1.update_recommendation_guidelines()
    # prediction = predict_disease(data)
    return jsonify({"user_id":"user_id_1"}) 


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # predicting diabetes
    result_diabetes = user1.predict_diabetes()
    diabetes_prediction = result_diabetes[0]
    diabetes_high_risk_probability = result_diabetes[1]
    print('diabetes risk:',diabetes_prediction ,' with probability of:', diabetes_high_risk_probability )
    # predicting heart and stroke
    result = user1.predict_heart_stroke()
    print('heart risk: ',result[0])
    print('stroke risk: ',result[1])
    return jsonify({"message":"prediction successful",'diabetes risk':diabetes_prediction,'heart risk':result[0],'stroke risk':result[1]})


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()

    if user1.diabetes_risk_prediction == 0:
        print("diabetes risk low with risky probability of: ", diabetes_high_risk_probability)
        return jsonify({"diabetes risk low with risky probability of": diabetes_high_risk_probability})
    else:
        print("Diabetes risk -> HIGH with risky probability of: ", diabetes_high_risk_probability)
        print()
        print("Recommending lifestyle ...")
        recommended_lifestyles_for_diabetes = user1.give_recommendation_for_diabetes()
    return jsonify(recommended_lifestyles_for_diabetes)


if __name__ == '__main__':
    app.run(debug=True)
