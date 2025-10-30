import pandas as pd
from sklearn.model_selection import train_test_split
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import evidently
import numpy

# Print versions for verification
print(f"Evidently version: {evidently.__version__}")  # Should be 0.4.39
print(f"NumPy version: {numpy.__version__}")  # Should be 2.0+

# Load dataset
try:
    data = pd.read_csv("../Data/combined_dataset.csv")
    print(f"Dataset shape: {data.shape}")
except FileNotFoundError:
    print("Error: '../Data/combined_dataset.csv' not found. Please provide the correct path.")
    exit(1)

# Split into train (reference) and test (current)
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
print(f"Train shape: {train_data.shape}, Test shape: {test_data.shape}")

# Only keep the 'label' column for drift detection
train_labels = train_data[['label']]
test_labels = test_data[['label']]

# Create report with DataDriftPreset
report = Report(metrics=[DataDriftPreset()])

try:
    print("Starting drift detection on 'label' column only...")
    print(f"Reference shape: {train_labels.shape}, Current shape: {test_labels.shape}")
    
    report.run(reference_data=train_labels, current_data=test_labels)
    print("Drift detection completed!")
except Exception as e:
    print(f"Error running report: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Save report as HTML
output_path = "artifacts/label_drift_report.html"
report.save_html(output_path)
print(f"Data drift report saved as '{output_path}'")

