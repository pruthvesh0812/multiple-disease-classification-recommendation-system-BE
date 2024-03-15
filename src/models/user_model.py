from services import filter_layer_1, filter_layer_2, filter_3

class User:
  user_id = -1
  name = ""
  email = ""

  diabetes_risk_prediction = -1
  heart_risk_prediction = -1
  stroke_risk_prediction = -1
  diabetes_risk_prob = -1

  phyActDuration = -1
  current_stress = -1




  user_lifestyle = {
    'Family_Diabetes': -1,  # 0: No family history of diabetes
    'BMI': -1,  # BMI value
    'Alcohol': -1,  # 0: Non-drinker, 1: Drinker
    'Sleep': -1,  # Hours of sleep per day
    'RegularMedicine': -1,  # 0: Does not take regular medicine, 1: Takes regular medicine
    'Pregancies': -1,  # Number of pregnancies (if applicable)
    'Pdiabetes': -1,  # 0: No history of previous diabetes
    'Age_40-49': -1,  # 0 or 1 based on user's age range
    'Age_50-59': -1,  # 0 or 1 based on user's age range
    'Age_60 or older': -1,  # 0 or 1 based on user's age range
    'Age_less than 40': -1,  # 0 or 1 based on user's age range
    'Gender_Female': -1,  # 0: Male, 1: Female
    'Gender_Male': -1,  # 0: Female, 1: Male
    'PhysicallyActive_less than half an hr': -1,  # 0 or 1 based on user's physical activity level
    'JunkFood_occasionally': -1,  # 0 or 1 based on user's junk food consumption frequency
    'JunkFood_very often': -1,  # 0 or 1 based on user's junk food consumption frequency
    'Stress_very_frequently': -1,  # 0 or 1 based on user's stress level
    'Stress_very_less': -1,  # 0 or 1 based on user's stress level
    'Stress_Sometimes': -1,  # 0 or 1 based on user's stress level
    'UriationFreq_0t much': -1,  # 0 or 1 based on user's urination frequency
    'UriationFreq_quite often': -1,  # 0 or 1 based on user's urination frequency
    'BP_High': -1,  # 0: Normal blood pressure, 1: High blood pressure
    'BP_low': -1,  # 0: Normal blood pressure, 1: Low blood pressure
    'BP_Normal': -1
  }

  user_lifestyle_heart_stroke = {
    'Diabetes_binary': -1, # No diabetes risk
    'HighBP': -1, # High blood pressure
    'HighChol': -1, # High cholesterol
    'CholCheck': -1, # Had a cholesterol check in the last 5 years
    'BMI': -1 ,# BMI of 25 (normal weight)
    'Smoker': -1, # Non-smoker
    # 'Stroke': 0, # No history of stroke
    # 'HeartDiseaseorAttack': 0, # No history of heart disease or attack
    'PhysActivity': -1, # Engaged in physical activity in the past 30 days
    'Fruits': -1, # Consumes fruit 1 or more times per day
    'Veggies': -1, # Consumes vegetables 1 or more times per day
    'HvyAlcoholConsump': -1, # No heavy alcohol consumption
    'AnyHealthcare': -1, # Has healthcare coverage
    'NoDocbcCost': -1, # No cost barrier to seeing a doctor
    'GenHlth': -1, # General health is good
    'MentHlth': -1, # No days of poor mental health in the past 30 days
    'PhysHlth': -1, # No physical illness or injury in the past 30 days
    'DiffWalk': -1, # No difficulty walking or climbing stairs
    'Sex': -1, # Male
    'Age': -1, # 18-24 years old
    'Education': -1, # High school graduate
    'Income': -1 # $75,000 or more
  }

  user_lifestyle_stroke = {
    'age': -1, # Age in years
    'hypertension': -1, # Binary: 1 = Yes, 0 = No
    'heart_disease': -1, # Binary: 1 = Yes, 0 = No
    'avg_glucose_level': -1, # Average glucose level in mg/dL
    'bmi': -1, # Body Mass Index
    'gender_Female': -1, # Binary: 1 = Female, 0 = Not Female
    'gender_Male': -1, # Binary: 1 = Male, 0 = Not Male
    'gender_Other': -1, # Binary: 1 = Other, 0 = Not Other
    'ever_married_No': -1, # Binary: 1 = No, 0 = Yes
    'ever_married_Yes': -1, # Binary: 1 = Yes, 0 = No
    'work_type_Govt_job': -1, # Binary: 1 = Yes, 0 = No
    'work_type_Never_worked': -1, # Binary: 1 = Yes, 0 = No
    'work_type_Private': -1, # Binary: 1 = Yes, 0 = No
    'work_type_Self-employed': -1, # Binary: 1 = Yes, 0 = No
    'work_type_children': -1, # Binary: 1 = Yes, 0 = No
    'Residence_type_Rural': -1, # Binary: 1 = Rural, 0 = Urban
    'Residence_type_Urban': -1, # Binary: 1 = Urban, 0 = Rural
    'smoking_status_Unknown': -1, # Binary: 1 = Unknown, 0 = Known
    'smoking_status_formerly smoked': -1, # Binary: 1 = Formerly smoked, 0 = Not formerly smoked
    'smoking_status_never smoked': -1, # Binary: 1 = Never smoked, 0 = Smoked
    'smoking_status_smokes': -1, # Binary: 1 = Smokes, 0 = Does not smoke
    # 'stroke': -1 # Binary: 1 = Yes, 0 = No
  }

  user_context = {
      'max_sleep_window' : [0,0],
      'diet_preference':"", # vegetarian/ non-vegetarian/ vegan
      'stress_type':"" ,# work/family/social/health/money
      'physical_limitation': "",
      'physical_activity_range':[0,0],
      'willingness_to_change_bmi':-1, # value out of 10
      'willingness_to_increase_sleep':-1, # out of 10
      'willingness_to_reduce_sleep': -1,
      'willingness_to_reduce_stress': -1
  }

  recommended_user_lifestyle = Recommended_Lifestyle()
#   gan_diabetes = gan_diabetes
#   gan_heart = gan_heart

  def __init__(self,user_id,name,email,predictor, recommender):
    self.user_id = user_id
    self.name = name
    self.email = email
    self.predictor = predictor
    self.gan_diabetes = recommender
    print("New User Created: ", self.user_id," ",self.name," ", self.email )

  def create_Lifestyle(self,lifestyle_object_diabetes,lifestyle_object_heart,lifestyle_object_stroke):
    self.user_lifestyle = copy.deepcopy(lifestyle_object_diabetes)
    self.user_lifestyle_heart_stroke = copy.deepcopy(lifestyle_object_heart)
    self.user_lifestyle_stroke = copy.deepcopy(lifestyle_object_stroke)

  def create_user_context(self,user_context):
    self.user_context = copy.deepcopy(user_context)

  def update_recommendation_guidelines(self):
    if self.user_lifestyle['Stress_very_frequently'] == 1:
      self.current_stress = 'high'
    elif self.user_lifestyle['Stress_Sometimes'] == 1:
      self.current_stress = 'medium'
    elif self.user_lifestyle['Stress_very_less'] == 1:
      self.current_stress = 'low'
    # NOTE : THIS CODE IS REMAINING - FUZZY FOR PHYSICAL ACTIVITY

    # update sleep range
    # recommended_user_lifestyle['sleep_range'] = user_context['max_sleep_window']

    # update physical activity range
    # use fuzzy rules to get physical activity range

    # temp use from user context only
    self.recommended_user_lifestyle.lifestyle_guidelines['physical_activity_range'][0] = self.user_context['physical_activity_range'][0]
    self.recommended_user_lifestyle.lifestyle_guidelines['physical_activity_range'][1] = self.user_context['physical_activity_range'][1]

  def predict_diabetes(self):
    #create test_df
    test_df = pd.DataFrame([self.user_lifestyle])
    # Make predictions on the test data
    prob_diabetes = self.predictor.rf_classifier_diabetes.predict_proba(test_df)
    prediction_diabetes = rf_classifier_diabetes.predict(test_df)

    print("Predicted Class:", prediction_diabetes , " probability low_risk:",prob_diabetes[0][0] , " probability high_risk:", prob_diabetes[0][1])

    # update user diabetes risk
    self.diabetes_risk_prediction = prediction_diabetes[0]

    return [prediction_diabetes , prob_diabetes[0][1]]

  def predict_heart_stroke(self):
    # update diabetes risk from prediction output
    self.user_lifestyle_heart_stroke['Diabetes_binary'] = self.diabetes_risk_prediction

    test_df = pd.DataFrame([self.user_lifestyle_heart_stroke])
    # Make predictions on the test data
    prob_heart_stroke= self.predictor.rf_classifier_heart_stroke.predict_proba(test_df)
    prediction_heart_stroke = self.predictor.rf_classifier_heart_stroke.predict(test_df)

    print("Predicted Class:", prediction_heart_stroke ,"since this option has max probability")
    print( "probability No risk (neither heart disease nor stroke):",prob_heart_stroke[0][0] )
    print( "probability only heart:",prob_heart_stroke[0][1]  )
    print("probability only stroke:",prob_heart_stroke[0][2])
    print( "probability high risk both:",prob_heart_stroke[0][3]  )

    # update heart risk prediction
    if prediction_heart_stroke == 0 or prediction_heart_stroke == 2:
        self.heart_risk_prediction = 0
    elif prediction_heart_stroke == 1 or prediction_heart_stroke == 3:
        self.heart_risk_prediction = 1

    prob_stroke_1 = max(prob_heart_stroke[0][2],prob_heart_stroke[0][3])
    prob_stroke_2 = self.predict_stroke()

    prob_stroke = ( prob_stroke_1 + prob_stroke_2[0][1] )/2
    print(prob_stroke, prob_stroke_1,prob_stroke_2)
    if prob_stroke < 0.5:
      prediction_stroke = 0
    else:
      prediction_stroke = 1

    self.stroke_risk_prediction = prediction_stroke

    return [self.heart_risk_prediction , self.stroke_risk_prediction]

  def predict_stroke(self):
    self.user_lifestyle_stroke['heart_disease'] = self.diabetes_risk_prediction

    test_df = pd.DataFrame([self.user_lifestyle_stroke])

    prob_stroke= self.predictor.rf_classifier_stroke.predict_proba(test_df)
    prediction_stroke = self.predictor.rf_classifier_stroke.predict(test_df)

    # return prob of high risk of stroke
    return prob_stroke

  def give_recommendation_for_diabetes(self):


      final_recommendation = []
    # while len(final_recommendation) == 0:
      num_samples = 1000
      alternate_lifestyles_diabetes = self.gan_diabetes.generate_alternate_lifestyle(num_samples)

      applicable_lifestyles_filter_1 = filter_layer_1 ( threshold = 0.5,
                                                        alternate_lifestyles = alternate_lifestyles_diabetes,
                                                        clf = self.predictor.rf_classifier_diabetes,
                                                        num_samples = num_samples,
                                                        user_lifestyle = self.user_lifestyle,
                                                        disease = 'diabetes' )

      applicable_lifestyles_filter_2 = filter_layer_2 ( applicable_lifestyle_filter_1 = applicable_lifestyles_filter_1,
                                                        recommended_lifestyle = self.recommended_user_lifestyle,
                                                        user = self,
                                                        phyActDuration = 1,
                                                        current_stress = self.current_stress )
    #   print("sdkflskdflksdf" , applicable_lifestyles_filter_2)

      final_recommendation = filter_3 ( applicable_lifestyles_filter_2 = applicable_lifestyles_filter_2,
                                        user_context = self.user_context,
                                        user_lifestyle = self.user_lifestyle,
                                        current_stress = self.current_stress )
      return final_recommendation


  # THERE IS NOTHING IN THIS DATASET THAT WE CAN RECOMMEND
  # def give_recommendation_for_heart(self):


  #     final_recommendation = []
  #   # while len(final_recommendation) == 0:
  #     num_samples = 1000
  #     alternate_lifestyles_heart = self.gan_heart.generate_alternate_lifestyle(num_samples)

  #     applicable_lifestyles_filter_1 = filter_layer_1 ( threshold = 0.5,
  #                                                       alternate_lifestyles = alternate_lifestyles_heart,
  #                                                       clf = self.predictor.rf_classifier_heart_stroke,
  #                                                       num_samples = num_samples,
  #                                                       user_lifestyle = self.user_lifestyle_heart_stroke,
  #                                                       disease = 'heart' )
  #     return applicable_lifestyles_filter_1
      # applicable_lifestyles_filter_2 = filter_layer_2 ( applicable_lifestyle_filter_1 = applicable_lifestyles_filter_1,
      #                                                   recommended_lifestyle = self.recommended_user_lifestyle,
      #                                                   user = self,
      #                                                   phyActDuration = 1,
      #                                                   current_stress = self.current_stress )
      # print("sdkflskdflksdf" , applicable_lifestyles_filter_2)

      # final_recommendation = filter_3 ( applicable_lifestyles_filter_2 = applicable_lifestyles_filter_2,
      #                                   user_context = self.user_context,
      #                                   user_lifestyle = self.user_lifestyle,
      #                                   current_stress = self.current_stress )
      # return final_recommendation


class Recommended_Lifestyle:
  diabetes = {
    'Family_Diabetes': -1,
    'BMI': -1,
    'Alcohol': -1,
    'Sleep': -1,
    'RegularMedicine': -1,
    'Pregancies': -1,
    'Pdiabetes': -1,
    'Age_40-49': -1,
    'Age_50-59': -1,
    'Age_60 or older': -1,
    'Age_less than 40': -1,
    'Gender_Female': -1,
    'Gender_Male': -1,
    'PhysicallyActive_less than half an hr': -1,
    'JunkFood_occasionally': -1,
    'JunkFood_very often': -1,
    'Stress_very_frequently': -1,
    'Stress_very_less': -1,
    'Stress_Sometimes': -1,
    'UriationFreq_0t much': -1,
    'UriationFreq_quite often': -1,
    'BP_High': -1,
    'BP_low': -1,
    'BP_Normal': -1
  }
  # [0, 23, 0, 11, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]

  lifestyle_guidelines = {
      'normal_bmi': [17,26], # [min,max]
      'sleep_range':[7,9],
      'physical_activity_range': [-1,-1], # calculated from user lifestyle and context
      'stress_PSS_score': [0,13], # Perceived Stress Scale (0,13) - low stress , (14,26) - moderate , (27,40) - high
      'Alcohol':0,
      'Smoking':0
  }





