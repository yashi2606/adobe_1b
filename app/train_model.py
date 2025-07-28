import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import onnx
import skl2onnx
from skl2onnx.common.data_types import FloatTensorType

# Sample feature data: [font_size, is_bold, text_length, y_position]
data = pd.DataFrame([
    {"font_size": 24, "is_bold": 1, "length": 10, "y": 100, "label": 1},
    {"font_size": 18, "is_bold": 1, "length": 20, "y": 200, "label": 2},
    {"font_size": 14, "is_bold": 0, "length": 25, "y": 300, "label": 3},
    {"font_size": 12, "is_bold": 0, "length": 100, "y": 400, "label": 0},
])

X = data[["font_size", "is_bold", "length", "y"]]
y = data["label"]

model = RandomForestClassifier(n_estimators=10)
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

# Convert to ONNX
initial_type = [("float_input", FloatTensorType([None, 4]))]
onnx_model = skl2onnx.convert_sklearn(model, initial_types=initial_type)
with open("heading_classifier.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())
