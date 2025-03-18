import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("financial_data.csv")
df.dropna(inplace=True)  # Remove missing values

# Define features (X) and target (y)
X = df.drop(columns=["price_of_item"])
y = (df["price_of_item"] <= 0.2 * df["income"]).astype(int)  # 1 if affordable, 0 if not

# Check label distribution
print(y.value_counts())  # Debugging line

# Ensure dataset has both 0s and 1s
if len(y.unique()) < 2:
    raise ValueError("Dataset must contain both 0 and 1 labels. Adjust the threshold or add more data.")

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Fix: Ensure train-test split works even if dataset is small
test_size = min(0.2, max(1 / len(y), 0.1))  # Ensures test_size is not smaller than 1 sample

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=test_size, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save model and scaler
joblib.dump(model, "AI_models/budget_ai_model.pkl")
joblib.dump(scaler, "AI_models/scaler.pkl")
