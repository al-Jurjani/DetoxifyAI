# generate_evidently_label_drift.py

import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from sklearn.model_selection import train_test_split
import os
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer


def generate_label_drift_report(csv_path="../Data/combined_dataset.csv"):
    print("📂 Loading dataset...")
    data = pd.read_csv(csv_path)
    print(f"✅ Loaded dataset with shape: {data.shape}")

    if "label" not in data.columns:
        raise ValueError("❌ No 'label' column found in dataset!")

    # Only keep label column
    data = data[["label"]]

    # Split into reference (train) and current (test)
    ref, cur = train_test_split(data, test_size=0.2, random_state=42)
    print(f"📊 Reference: {ref.shape}, Current: {cur.shape}")

    # Create report
    print("⚙️ Generating Evidently Data Drift report on 'label' column...")
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=ref, current_data=cur)

    # Save HTML
    os.makedirs("artifacts", exist_ok=True)
    output_path = "artifacts/evidently_label_drift.html"
    report.save_html(output_path)
    print(f"✅ Drift report saved to {output_path}")

    return output_path


def serve_report(port=7000):
    os.chdir("artifacts")
    TCPServer.allow_reuse_address = True
    with TCPServer(("", port), SimpleHTTPRequestHandler) as httpd:
        print(f"🚀 Serving report at: http://localhost:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    html_path = generate_label_drift_report()

    # Optional: Serve report automatically
    serve = input("🌐 Serve report locally? (y/n): ").lower()
    if serve == "y":
        serve_report()
