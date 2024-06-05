import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib


# Load the dataset
df = pd.read_csv('cleaned_water_potability.csv')

# Verify that there are no more missing values
print(df.isnull().sum())



# Assuming 'Potability' is the purity measure scaled to 0% and 100%
df['Purity'] = df['Potability'] * 100  # Scale to percentage

# Split the data into features and target variable
X = df.drop(['Potability', 'Purity'], axis=1)
y = df['Purity']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")
# Save the trained model
joblib.dump(model, 'water_purity_model.pkl')

# Load the model (for future use)
# loaded_model = joblib.load('water_purity_model.pkl')