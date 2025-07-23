import shap
import joblib
import pandas as pd
import matplotlib.pyplot as plt

# Load trained model
model = joblib.load("model.pkl")

# Example input (same structure as your training data)
data = pd.DataFrame([{
    "temperature": 27,
    "co2": 400,
    "tvoc": 120,
    "sound_level": 45
}])

# Create SHAP explainer
explainer = shap.Explainer(model, data)
shap_values = explainer(data)

# Plot explanation
shap.plots.waterfall(shap_values[0], max_display=4)  # or .force_plot
plt.savefig("shap_waterfall.png")  # save for frontend
plt.show()
