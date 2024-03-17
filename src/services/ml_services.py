import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

import tensorflow as tf
from tensorflow.keras import layers, models


class Predictor:
  def __init__(self):
    self.rf_classifier_diabetes = NULL
    self.rf_classifier_stroke = NULL
    self.rf_classifier_heart_stroke = NULL

    def train_diabetes(df_diabetes):

        X_diabetes = df_diabetes.drop('Diabetic', axis=1)
        y_diabetes = df_diabetes['Diabetic']

        # Split the data into training and testing sets (80% train, 20% test)
        X_train_diabetes, X_test_diabetes, y_train_diabetes, y_test_diabetes = train_test_split(X_diabetes, y_diabetes, test_size=0.2, random_state=42)

        # Initialize the Random Forest classifier
        rf_classifier_diabetes = RandomForestClassifier(n_estimators=100, random_state=42)

        # Train the classifier on the training data
        rf_classifier_diabetes.fit(X_train_diabetes, y_train_diabetes)

       
    def train_heart_stroke(df_heart):
        y_heart = df_heart['HeartDiseaseorAttack']
        y_stroke = df_heart['Stroke']
        X_heart_stroke_train = df_heart.drop(['Stroke','HeartDiseaseorAttack'],axis=1)

        # Adjusted mapping to incorporate the new pairs
        y_combined = (2*y_heart + y_stroke).apply(lambda x: 0 if x == 0 else 1 if x == 2 else 2 if x == 1 else 3 if x == 3 else 4)

        # The adjusted mapping now includes:
        # 0: No risk (neither heart disease nor stroke) --> 2*0+0 = 0 -> return 0
        # 1: Only heart disease risk --> 2*1+0 = 2 -> return 1
        # 2: Only stroke disease risk --> 2*0+1 = 1 -> return 2
        # 3: High risk (both heart disease and stroke) --> 2*1+1 = 3 -> return 3

        # Split the data into training and testing sets
        X_train_heart_stroke, X_test_heart_stroke, y_train_heart_stroke, y_test_heart_stroke = train_test_split(X_heart_stroke_train, y_combined, test_size=0.2, random_state=42)

        # Initialize the Random Forest classifier
        rf_heart_stroke = RandomForestClassifier(n_estimators=100, random_state=42)

        # Train the classifier
        rf_heart_stroke.fit(X_train_heart_stroke, y_train_heart_stroke)


    def train_stroke(df_stroke):
        # Split the dataset into features (X) and target variable (y)
        X_stroke = df_stroke.drop('stroke', axis=1)
        y_stroke  = df_stroke['stroke']

        # Split the data into training and testing sets (80% train, 20% test)
        X_train_stroke , X_test_stroke , y_train_stroke , y_test_stroke  = train_test_split(X_stroke , y_stroke , test_size=0.2, random_state=42)

        # Initialize the Random Forest classifier
        rf_classifier_stroke  = RandomForestClassifier(n_estimators=100, random_state=42)

        # Train the classifier on the training data
        rf_classifier_stroke .fit(X_train_stroke , y_train_stroke )

        def train_prediction_models(dataframes):
            self.rf_classifier_diabetes = self.train_diabetes(dataframes['for_diabetes.csv'])
            self.rf_classifier_stroke = self.train_diabetes(dataframes['heart-to-stroke.csv'])
            self.rf_classifier_heart_stroke = self.train_diabetes(dataframes['diabetes_to_heart_clean.csv'])

class RECOMMENDER:
  
    def __init__(self,df_diabetes,disease):
      # Normalize data
      if disease == 'diabetes':
        self.data_gan = self.df_diabetes
        self.scaler = MinMaxScaler()
      elif disease == 'heart':
        self.data_gan = self.X_heart
        self.scaler = StandardScaler()
      self.normalized_data = self.scaler.fit_transform(self.data_gan)

    # Defining the generator model
    def build_generator(self,latent_dim, output_dim):
        model = models.Sequential()
        model.add(layers.Dense(256, input_dim=latent_dim, activation='relu'))
        model.add(layers.BatchNormalization())
        model.add(layers.Dense(512, activation='relu'))
        model.add(layers.BatchNormalization())
        model.add(layers.Dense(output_dim, activation='sigmoid'))
        return model

    # Defining the discriminator model
    def build_discriminator(self,input_dim):
        model = models.Sequential()
        model.add(layers.Dense(512, input_dim=input_dim, activation='relu'))
        model.add(layers.Dense(256, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))
        return model

    # Defining the GAN model
    def build_gan(self,generator, discriminator):
        discriminator.trainable = False
        model = models.Sequential()
        model.add(generator)
        model.add(discriminator)
        return model

    # Defining the combined model
    def build_combined(self,generator, discriminator):
        model = models.Sequential()
        model.add(generator)
        model.add(discriminator)
        return model


    def train(self):
      # Defining the hyperparameters
      latent_dim =100
      self.latent_dim = latent_dim
      self.normalized_data = self.scaler.fit_transform(self.data_gan)
      feature_dim = self.normalized_data.shape[1]

      # Building and compiling the discriminator
      discriminator = self.build_discriminator(feature_dim)
      discriminator.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

      # Building and compiling the generator
      generator = self.build_generator(latent_dim, feature_dim)
      self.generator = generator
      generator.compile(loss='binary_crossentropy', optimizer='adam')

      # Building and compiling the GAN
      gan = self.build_gan(generator, discriminator)
      gan.compile(loss='binary_crossentropy', optimizer='adam')

      # Building and compiling the combined model
      combined_model = self.build_combined(generator, discriminator)
      combined_model.compile(loss='binary_crossentropy', optimizer='adam')


      print("Generator Summary:")
      generator.summary()

      print("\nDiscriminator Summary:")
      discriminator.summary()

      print("\nGAN Summary:")
      gan.summary()

      print("\nCombined Model Summary:")
      combined_model.summary()

      # Defining the number of training epochs and batch size
      epochs = 100
      batch_size = 32

      # Training the GAN
      for epoch in range(epochs):
          # Generate a batch of noise vectors
          noise = np.random.normal(0, 1, (batch_size, latent_dim))

          # Generate synthetic samples with the generator
          generated_samples = generator.predict(noise)

          # Select a random batch of real samples
          idx = np.random.randint(0, self.normalized_data.shape[0], batch_size)
          real_samples = self.normalized_data[idx]

          # Labels for real and fake samples
          real_labels = np.ones((batch_size, 1))
          fake_labels = np.zeros((batch_size, 1))

          # Training the discriminator on real samples
          d_loss_real = discriminator.train_on_batch(real_samples, real_labels)

          # Training the discriminator on fake samples
          d_loss_fake = discriminator.train_on_batch(generated_samples, fake_labels)

          # Combining the losses for the discriminator
          d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

          # Training the generator to fool the discriminator
          valid_labels = np.ones((batch_size, 1))
          g_loss = combined_model.train_on_batch(noise, valid_labels)

          print(f"Epoch {epoch}, D Loss: {d_loss[0]}, G Loss: {g_loss}")
          if d_loss[0] <= 0.008:
            break



    # generate alternate lifestyles
    def generate_alternate_lifestyle(self,num_samples):
      # generating n samples
      noise = np.random.normal(0, 1, (num_samples, self.latent_dim))
      generated_samples = self.generator.predict(noise)

      # Transform the generated samples back to the original scale
      generated_samples_original_scale = self.scaler.inverse_transform(generated_samples)
      rounded_values = np.round(generated_samples_original_scale).astype(int)
      return rounded_values

