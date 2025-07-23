import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib

# 1. Generate dummy data
np.random.seed(42)
n = 500

data = pd.DataFrame({
    'temperature': np.random.normal(28, 3, n),
    'co2': np.random.normal(500, 100, n),
    'tvoc': np.random.normal(150, 30, n),
    'sound_level': np.random.normal(60, 10, n)
})

# 2. Create target: stress_level (1 = High stress, 0 = Low)
data['stress_level'] = ((data['temperature'] > 30) | 
                        (data['co2'] > 600) | 
                        (data['tvoc'] > 180) | 
                        (data['sound_level'] > 70)).astype(int)

# 3. Train model
X = data[['temperature', 'co2', 'tvoc', 'sound_level']]
y = data['stress_level']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

model = LogisticRegression()
model.fit(X_train, y_train)

# 4. Save model
joblib.dump(model, "model.pkl")
print("✅ Model saved as model.pkl")
