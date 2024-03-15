# filter 1 - re-classification

import heapq

def filter_layer_1(threshold,alternate_lifestyles,clf,num_samples,user_lifestyle,disease):

  if disease == 'diabetes':
    applicable_lifestyles_filter = []
    for x in range(1,num_samples):
        Gen_lifestyle = alternate_lifestyles[x].reshape(1, -1)[:,:-1][0]

        print(Gen_lifestyle,"gen lifestyle")
        Gen_lifestyle[0] = user_lifestyle['Family_Diabetes']
        Gen_lifestyle[2] = 0
        Gen_lifestyle[4] = user_lifestyle['RegularMedicine']
        Gen_lifestyle[5] = user_lifestyle['Pregancies']
        Gen_lifestyle[6] = user_lifestyle['Pdiabetes']
        Gen_lifestyle[7] = user_lifestyle['Age_40-49']
        Gen_lifestyle[8] = user_lifestyle['Age_50-59']
        Gen_lifestyle[9] = user_lifestyle['Age_60 or older']
        Gen_lifestyle[10] = user_lifestyle['Age_less than 40']
        Gen_lifestyle[11] = user_lifestyle['Gender_Female']
        Gen_lifestyle[12] = user_lifestyle['Gender_Male']
        Gen_lifestyle[19] = user_lifestyle['UriationFreq_0t much']
        Gen_lifestyle[20] = user_lifestyle['UriationFreq_quite often']
        Gen_lifestyle[21] = user_lifestyle['BP_High']
        Gen_lifestyle[22] = user_lifestyle['BP_low']
        Gen_lifestyle[23] = user_lifestyle['BP_Normal']

        alternate = {
            'Family_Diabetes': Gen_lifestyle[0],  # 0: No family history of diabetes
            'BMI': Gen_lifestyle[1],  # BMI value
            'Alcohol': Gen_lifestyle[2],  # 0: Non-drinker, 1: Drinker
            'Sleep': Gen_lifestyle[3],  # Hours of sleep per day
            'RegularMedicine': Gen_lifestyle[4],  # 0: Does not take regular medicine, 1: Takes regular medicine
            'Pregancies': Gen_lifestyle[5],  # Number of pregnancies (if applicable)
            'Pdiabetes': Gen_lifestyle[6],  # 0: Gen_lifestyle[0]o history of previous diabetes
            'Age_40-49': Gen_lifestyle[7],  # 0 or 1 based on user's age range
            'Age_50-59': Gen_lifestyle[8],  # 0 or 1 based on user's age range
            'Age_60 or older': Gen_lifestyle[9],  # 0 or 1 based on user's age range
            'Age_less than 40': Gen_lifestyle[10],  # 0 or 1 based on user's age range
            'Gender_Female': Gen_lifestyle[11],  # 0: Gen_lifestyle[0]ale, 1: Gen_lifestyle[0]emale
            'Gender_Male': Gen_lifestyle[12],  # 0: Gen_lifestyle[0]emale, 1: Gen_lifestyle[0]ale
            'PhysicallyActive_less than half an hr': 1,  # 0 or 1 based on user's physical activity level
            'JunkFood_occasionally': Gen_lifestyle[14],  # 0 or 1 based on user's junk food consumption frequency
            'JunkFood_very often': Gen_lifestyle[15],  # 0 or 1 based on user's junk food consumption frequency
            'Stress_very_frequently': Gen_lifestyle[16],  # 0 or 1 based on user's stress level
            'Stress_very_less': Gen_lifestyle[17],  # 0 or 1 based on user's stress level
            'Stress_Sometimes': Gen_lifestyle[18],  # 0 or 1 based on user's stress level
            'UriationFreq_0t much': Gen_lifestyle[19],  # 0 or 1 based on user's urination frequency
            'UriationFreq_quite often': Gen_lifestyle[20],  # 0 or 1 based on user's urination frequency
            'BP_High': Gen_lifestyle[21],  # 0: Gen_lifestyle[0]ormal blood pressure, 1: Gen_lifestyle[0]igh blood pressure
            'BP_low': Gen_lifestyle[22],  # 0: Gen_lifestyle[0]ormal blood pressure, 1: Gen_lifestyle[0]ow blood pressure
            'BP_Normal': Gen_lifestyle[23]  # 0 or 1 based on user's blood pressure status
        }
        test_df = pd.DataFrame([alternate])
        if(clf.predict_proba(test_df)[0][1] > threshold ):
          continue
        else:
          applicable_lifestyles_filter.append(alternate)

    return applicable_lifestyles_filter
  elif disease == 'heart':
    applicable_lifestyles_filter = []
    for x in range(1,num_samples):
        Gen_lifestyle = alternate_lifestyles[x].reshape(1, -1)[0]

        # print(Gen_lifestyle,"gen lifestyle")

        Gen_lifestyle[0] = user_lifestyle['Diabetes_binary']
        Gen_lifestyle[3] = user_lifestyle['CholCheck']
        Gen_lifestyle[4] = 30 # comes from diabetes_recommendation or give a range and iterate over it
        Gen_lifestyle[5] = 0
        Gen_lifestyle[9] = user_lifestyle['HvyAlcoholConsump']
        Gen_lifestyle[11] = user_lifestyle['NoDocbcCost']
        Gen_lifestyle[15] = user_lifestyle['DiffWalk']
        Gen_lifestyle[16] = user_lifestyle['Sex']
        Gen_lifestyle[17] = user_lifestyle['Age']
        Gen_lifestyle[18] = user_lifestyle['Education']
        Gen_lifestyle[19] = user_lifestyle['Income']


        alternate = {
          'Diabetes_binary': Gen_lifestyle[0], # No diabetes risk
          'HighBP': Gen_lifestyle[1], # High blood pressure
          'HighChol': Gen_lifestyle[2], # High cholesterol
          'CholCheck': Gen_lifestyle[3], # Had a cholesterol check in the last 5 years
          'BMI': Gen_lifestyle[4] ,# BMI of 25 (normal weight)
          'Smoker': Gen_lifestyle[5], # Non-smoker
          'PhysActivity': Gen_lifestyle[6], # Engaged in physical activity in the past 30 days
          'Fruits': Gen_lifestyle[7], # Consumes fruit 1 or more times per day
          'Veggies': Gen_lifestyle[8], # Consumes vegetables 1 or more times per day
          'HvyAlcoholConsump': Gen_lifestyle[9], # No heavy alcohol consumption
          'AnyHealthcare': Gen_lifestyle[10], # Has healthcare coverage
          'NoDocbcCost': Gen_lifestyle[11], # No cost barrier to seeing a doctor
          'GenHlth': Gen_lifestyle[12], # General health is good
          'MentHlth': Gen_lifestyle[13], # No days of poor mental health in the past 30 days
          'PhysHlth': Gen_lifestyle[14], # No physical illness or injury in the past 30 days
          'DiffWalk': Gen_lifestyle[15], # No difficulty walking or climbing stairs
          'Sex': Gen_lifestyle[16], # Male
          'Age': Gen_lifestyle[17], # 18-24 years old
          'Education': Gen_lifestyle[18], # High school graduate
          'Income': Gen_lifestyle[19] # $75,000 or more
        }
        test_df = pd.DataFrame([alternate])
        if(clf.predict_proba(test_df)[0][1] > threshold ):
          continue
        else:
          applicable_lifestyles_filter.append(alternate)

    return applicable_lifestyles_filter



# filter layer 2 - based on medical guidelines and user context

def filter_layer_2(applicable_lifestyle_filter_1,recommended_lifestyle,user,phyActDuration,current_stress):
  # creating list
   most_optimal_lifestyles = []
   stress_compromised_lifestyles = []
   phyAct_compromised_lifestyles = []
   bmi_compromised_lifestyles = []
   sleep_compromised_lifestyles = []

   for lifestyle in applicable_lifestyle_filter_1:

      compromise_bmi = -1
      compromise_sleep = -1
      compromise_phyAct = 0
      compromise_stress = -1



      # filtering for bmi
      if lifestyle['BMI'] < recommended_lifestyle.lifestyle_guidelines['normal_bmi'][1] and lifestyle['BMI'] > recommended_lifestyle.lifestyle_guidelines['normal_bmi'][0]:
        compromise_bmi = 0 # add lifestyle to optimal
      elif lifestyle['BMI'] < 29 and lifestyle['BMI'] > recommended_lifestyle.lifestyle_guidelines['normal_bmi'][0]:
        compromise_bmi = 0 # add lifestyle to compromise_bmi_list
      elif lifestyle['BMI'] > 30 and lifestyle['BMI'] < recommended_lifestyle.lifestyle_guidelines['normal_bmi'][0]:
        compromise_bmi = -1 # discard lifestyle

      # filtering for sleep
      if lifestyle['Sleep'] < recommended_lifestyle.lifestyle_guidelines['sleep_range'][1] and lifestyle['Sleep'] > user.user_context['max_sleep_window'][0]:
        compromise_sleep = 0
      elif lifestyle['Sleep'] < recommended_lifestyle.lifestyle_guidelines['sleep_range'][1]:
        compromise_sleep = 1
      else:
        compromise_sleep = -1

      # # filtering for physical activity
      # if recommended_lifestyle.lifestyle_guidelines['physical_activity_range'][1] < user.user_context['physical_activity_range'][1]:
      #   if recommended_lifestyle.lifestyle_guidelines['physical_activity_range'][0] > user.user_context['physical_activity_range'][0]:
      #     if phyActDuration < user.user_context['physical_activity_range'][1] and phyActDuration > recommended_lifestyle.lifestyle_guidelines['physical_activity_range'][0]:
      #       compromise_phyAct = 0
      #     elif phyActDuration < user.user_context['physical_activity_range'][1] and phyActDuration < user.user_context['physical_activity_range'][0]:
      #       compromise_phyAct = 1
      #   else:
      #     if phyActDuration < user.user_context['physical_activity_range'][1] and phyActDuration > recommended_lifestyle.lifestyle_guidelines['physical_activity_range'][0]:
      #       compromise_phyAct = 0
      #     else:
      #       compromise_phyAct = -1
      # else:
      #   if recommended_lifestyle.lifestyle_guidelines['physical_activity_range'][0] < user.user_context['physical_activity_range'][0]:
      #     if phyActDuration > user.user_context['physical_activity_range'][1] and phyActDuration < recommended_lifestyle.lifestyle_guidelines['physical_activity_range'][1]:
      #       compromise_phyAct = 1
      #     elif phyActDuration < user.user_context['physical_activity_range'][1] and phyActDuration > user.user_context['physical_activity_range'][0]:
      #       compromise_phyAct = 0
      #     elif phyActDuration < user.user_context['physical_activity_range'][0] and phyActDuration > recommended_lifestyle.lifestyle_guidelines['physical_activity_range'][0]:
      #       compromise_phyAct = 0
      #     else:
      #       compromise_phyAct = -1
      #   else:
      #     if phyActDuration > user.user_context['physical_activity_range'][1] and phyActDuration < recommended_lifestyle.lifestyle_guidelines['physical_activity_range'][1]:
      #       compromise_phyAct = 1
      #     elif phyActDuration > user.user_context['physical_activity_range'][0] and phyActDuration < user.user_context['physical_activity_range'][1]:
      #       compromise_phyAct = 0
      #     else:
      #       compromise_phyAct = -1

      compromise_phyAct = 0

        # filter stress
      print("current stress" , current_stress , ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
      # if lifestyle['Stress_very_frequently'] == 1 and (current_stress == 'medium' or current_stress == 'low'):
      #     compromise_stress = -1
      # elif lifestyle['Stress_Sometimes'] == 1 and (current_stress == 'low'):
      #     compromise_stress = -1
      # elif lifestyle['Stress_very_frequently'] == 1 and (current_stress == 'high'):
      #     compromise_stress = -1
      if (lifestyle['Stress_very_less'] ==1 or lifestyle['Stress_Sometimes'] == 1 )  and (current_stress == 'high'):
          compromise_stress = 0
      elif lifestyle['Stress_very_less'] == 1 and (current_stress == 'medium'):
          compromise_stress = 0
      elif lifestyle['Stress_very_less'] == 1 and (current_stress == 'low'):
          compromise_stress = 0
      elif lifestyle['Stress_very_frequently'] == 1 :
          compromise_stress = -1
      # else:
      #     compromise_stress = 1 # high - high , medium - medium




      # assigning lifestyle to each
      if compromise_bmi == 0 and compromise_sleep == 0 and compromise_phyAct == 0 and compromise_stress == 0:
        most_optimal_lifestyles.append(lifestyle)
      if compromise_sleep == 1 and compromise_bmi == 0 and compromise_phyAct == 0 and compromise_stress == 0:
        sleep_compromised_lifestyles.append(lifestyle)
      if compromise_sleep == 0 and compromise_bmi == 0 and compromise_phyAct == 0 and compromise_stress == 1:
        stress_compromised_lifestyles.append(lifestyle)
      if compromise_sleep == 0 and compromise_bmi == 0 and compromise_phyAct == 1 and compromise_stress == 1:
        phyAct_compromised_lifestyles = []
      if compromise_sleep == 0 and compromise_bmi == 1 and compromise_phyAct == 1 and compromise_stress == 1:
        bmi_compromised_lifestyles = []

   return most_optimal_lifestyles



# to implement selection of lifestyles with minimum cost


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0 # to avoid same priority value conflict

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority,self._index, item))
        self._index += 1
        print(self._queue[0])

    def pop(self):
        return heapq.heappop(self._queue)[2]

    def __len__(self):
        return len(self._queue)

    def is_empty(self):
        return len(self._queue) == 0

def select_top_n(cost_of_changing_lifestyles,applicable_lifestyles_filter_3,n):
  min1 = 1000
  min2 = 1000
  min3 = 1000

  L1 = {}
  L2 = {}
  L3 = {}
  final_recommendation = []

  pq = PriorityQueue()
  print(len(cost_of_changing_lifestyles)," ",  len(applicable_lifestyles_filter_3))
  print(cost_of_changing_lifestyles)
  for cost,lifestyle in zip(cost_of_changing_lifestyles,applicable_lifestyles_filter_3):
    print(type(cost))
    print('tuple ==> ' , cost, lifestyle)
    pq.push(item=lifestyle,priority = cost)
    print('2323232323',lifestyle)

  for x in range(n):
    if len(pq) > 0:
      final_recommendation.append(pq.pop())
    else:
      break

  return final_recommendation



  # if len(cost_of_changing_lifestyles) == 2:
  #   if cost_of_changing_lifestyles[0] < cost_of_changing_lifestyles[1]:
  #     L1 = applicable_lifestyles_filter_3[0]
  #     L2 = applicable_lifestyles_filter_3[1]
  #   else:
  #     L1 = applicable_lifestyles_filter_3[1]
  #     L2 = applicable_lifestyles_filter_3[0]
  # elif len(cost_of_changing_lifestyles) == 1:
  #   L1 = applicable_lifestyles_filter_3[0]
  # else:
  #   for c,l in zip(cost_of_changing_lifestyles,applicable_lifestyles_filter_3):
  #    #   print('2323232323',applicable_lifestyles_filter_3)
  #     if c < min1:
  #       min3 = min2
  #       min2 = min1
  #       min1 = c
  #       L3 = L2
  #       L2 = L1
  #       L1 = l
  #     elif c < min2:
  #       min3 = min2
  #       min2 = c
  #       L3 = L2
  #       L2 = l
  #     elif c < min3:
  #       min3 = c
  #       L3 = l


  # return final_recommendation

# out of the generate ones we cannot recommend all we need to find the cost

def filter_3(applicable_lifestyles_filter_2,user_context,user_lifestyle,current_stress):
  cost_of_changing_lifestyles = []
  applicable_lifestyles_filter_3 = []
  cost_bmi = 0
  cost_sleep = 0
  cost_stress = 0
  for lifestyle in applicable_lifestyles_filter_2:

    cost_bmi = abs((user_lifestyle['BMI'] - lifestyle['BMI']) * (10-user_context['willingness_to_change_bmi']))   # (actual - recommend_bmi)*resistance

    cost_sleep = abs((user_lifestyle['Sleep'] - lifestyle['Sleep']) * (10-user_context['willingness_to_increase_sleep']))

    if current_stress == 'high':
      cost_stress = abs((user_lifestyle['Stress_very_frequently'] - 2*lifestyle['Stress_Sometimes'] - 3*lifestyle['Stress_very_less']) * (10 - user_context['willingness_to_reduce_stress']))
    elif current_stress == 'medium':
      cost_stress = abs((user_lifestyle['Stress_Sometimes'] - 2*lifestyle['Stress_very_less']) * (10 - user_context['willingness_to_reduce_stress']))
    elif current_stress == 'low':
      cost_stress = abs((user_lifestyle['Stress_very_less'] - lifestyle['Stress_very_less']) * (10 - user_context['willingness_to_reduce_stress']))


    total_cost = cost_bmi + cost_sleep + cost_stress

    cost_of_changing_lifestyles.append(total_cost)
    applicable_lifestyles_filter_3.append(lifestyle)
    print("2390294093 ", lifestyle)
  return select_top_n( cost_of_changing_lifestyles = cost_of_changing_lifestyles , applicable_lifestyles_filter_3 = applicable_lifestyles_filter_3 ,n=5)


