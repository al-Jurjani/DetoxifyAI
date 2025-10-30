# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse
# import pandas as pd
# import os

# # Correct imports for Evidently 0.7.15
# from evidently.ui.workspace import Workspace
# from evidently.presets import DataDriftPreset, DataSummaryPreset

# # For Evidently 0.7.x, use the correct Report location
# try:
#     from evidently.report import Report # type: ignore
# except ImportError:
#     try:
#         from evidently.core.report import Report
#     except ImportError:
#         from evidently.legacy.report import Report

# # -------------------------------
# # Setup FastAPI + Evidently Workspace
# # -------------------------------
# app = FastAPI(title="Evidently Dashboard (v0.7.x)")

# # Path for Evidently workspace (stores reports, panels)
# WORKSPACE_PATH = "evidently_workspace"
# os.makedirs(WORKSPACE_PATH, exist_ok=True)

# # Initialize workspace
# try:
#     workspace = Workspace.create(WORKSPACE_PATH)
# except Exception:
#     workspace = Workspace(WORKSPACE_PATH)

# # Global variable to store report
# report_html = None
# report_path = os.path.join(WORKSPACE_PATH, "data_drift_report.html")

# # -------------------------------
# # Function to generate report
# # -------------------------------
# def generate_report():
#     """Generate Evidently report from data"""
#     global report_html

#     # Load and split dataset
#     df = pd.read_csv("Data/combined_dataset.csv")
#     train_df = df.sample(frac=0.8, random_state=42)
#     test_df = df.drop(train_df.index)

#     # Get metrics from presets
#     drift_preset = DataDriftPreset()
#     summary_preset = DataSummaryPreset()

#     # In Evidently 0.7.x, presets can be used directly as metrics
#     # Don't call generate_metrics - just use the preset instances
#     metrics = [drift_preset, summary_preset]

#     # Create report
#     report = Report(metrics=metrics)  # type: ignore

#     # Run the report
#     report.run(reference_data=train_df, current_data=test_df)

#     # Save as HTML - try different methods
#     try:
#         report.save_html(report_path)  # type: ignore
#     except AttributeError:
#         try:
#             # Alternative method for 0.7.x
#             html_str = report.get_html()  # type: ignore
#             with open(report_path, 'w', encoding='utf-8') as f:
#                 f.write(html_str)
#         except AttributeError:
#             # Another alternative
#             report.save(report_path)  # type: ignore

#     # Store in memory
#     with open(report_path, 'r', encoding='utf-8') as f:
#         report_html = f.read()

#     print(f"Report generated successfully at: {report_path}")
#     return report_html

# # Generate initial report on startup
# try:
#     generate_report()
#     print("Initial report generated successfully")
# except Exception as e:
#     print(f"Error generating initial report: {e}")
#     report_html = f"<h1>Error generating report</h1><pre>{str(e)}</pre>"

# # -------------------------------
# # FastAPI routes
# # -------------------------------
# @app.get("/")
# def index():
#     return {
#         "message": "Evidently Dashboard active. Visit /report to view drift results.",
#         "endpoints": {
#             "/": "This info page",
#             "/report": "View the data drift HTML report",
#             "/health": "Health check",
#             "/regenerate": "Regenerate the report (POST)"
#         }
#     }

# @app.get("/report", response_class=HTMLResponse)
# def show_report():
#     """Serve the generated Evidently HTML report"""
#     if report_html is None:
#         return HTMLResponse(
#             content="<h1>Report not generated yet</h1><p>Try calling POST /regenerate</p>",
#             status_code=404
#         )
#     return HTMLResponse(content=report_html, status_code=200)

# @app.get("/health")
# def health_check():
#     """Health check endpoint"""
#     return {
#         "status": "healthy",
#         "workspace_path": WORKSPACE_PATH,
#         "report_exists": os.path.exists(report_path),
#         "report_loaded": report_html is not None
#     }

# @app.post("/regenerate")
# def regenerate_report():
#     """Regenerate the report with fresh data"""
#     try:
#         generate_report()
#         return {
#             "message": "Report regenerated successfully",
#             "path": report_path
#         }
#     except Exception as e:
#         return {"error": str(e)}, 500

# if __name__ == "__main__":
#     import uvicorn
#     # Use 127.0.0.1 for Windows compatibility instead of 0.0.0.0
#     uvicorn.run(app, host="127.0.0.1", port=7000)

# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse
# import pandas as pd
# import os

# # Correct imports for Evidently 0.7.15
# from evidently.ui.workspace import Workspace
# from evidently.presets import DataDriftPreset, DataSummaryPreset

# # For Evidently 0.7.x, use the correct Report location
# try:
#     from evidently.report import Report
# except ImportError:
#     try:
#         from evidently.core.report import Report
#     except ImportError:
#         from evidently.legacy.report import Report

# # -------------------------------
# # Setup FastAPI + Evidently Workspace
# # -------------------------------
# app = FastAPI(title="Evidently Dashboard (v0.7.x)")

# # Path for Evidently workspace (stores reports, panels)
# WORKSPACE_PATH = "evidently_workspace"
# os.makedirs(WORKSPACE_PATH, exist_ok=True)

# # Initialize workspace
# try:
#     workspace = Workspace.create(WORKSPACE_PATH)
# except Exception:
#     workspace = Workspace(WORKSPACE_PATH)

# # Global variable to store report
# report_html = None
# report_path = os.path.join(WORKSPACE_PATH, "data_drift_report.html")

# # -------------------------------
# # Function to generate report
# # -------------------------------
# def generate_report():
#     """Generate Evidently report from data"""
#     global report_html

#     # Load and split dataset
#     df = pd.read_csv("Data/combined_dataset.csv")
#     train_df = df.sample(frac=0.8, random_state=42)
#     test_df = df.drop(train_df.index)

#     # Get metrics from presets
#     drift_preset = DataDriftPreset()
#     summary_preset = DataSummaryPreset()

#     # In Evidently 0.7.x, presets can be used directly as metrics
#     # Don't call generate_metrics - just use the preset instances
#     metrics = [drift_preset, summary_preset]

#     # Create report
#     report = Report(metrics=metrics)  # type: ignore

#     # Run the report
#     report.run(reference_data=train_df, current_data=test_df)

#     # Save as HTML - try different methods
#     try:
#         report.save_html(report_path)  # type: ignore
#     except AttributeError:
#         try:
#             # Alternative method for 0.7.x
#             html_str = report.get_html()  # type: ignore
#             with open(report_path, 'w', encoding='utf-8') as f:
#                 f.write(html_str)
#         except AttributeError:
#             try:
#                 # Try as_dict then render
#                 report_dict = report.as_dict()  # type: ignore
#                 # Use show() which might open in browser or save
#                 report.show(mode='inline')  # type: ignore
#                 # Fallback: just get the JSON and create basic HTML
#                 import json
#                 html_str = f"""
#                 <html>
#                 <head><title>Evidently Report</title></head>
#                 <body>
#                 <h1>Evidently Report</h1>
#                 <pre>{json.dumps(report_dict, indent=2)}</pre>
#                 </body>
#                 </html>
#                 """
#                 with open(report_path, 'w', encoding='utf-8') as f:
#                     f.write(html_str)
#             except Exception as e:
#                 # Last resort: create error HTML
#                 html_str = f"""
#                 <html>
#                 <head><title>Report Error</title></head>
#                 <body>
#                 <h1>Could not generate HTML report</h1>
#                 <p>Error: {str(e)}</p>
#                 <p>Report object methods: {dir(report)}</p>
#                 </body>
#                 </html>
#                 """
#                 with open(report_path, 'w', encoding='utf-8') as f:
#                     f.write(html_str)

#     # Store in memory
#     with open(report_path, 'r', encoding='utf-8') as f:
#         report_html = f.read()

#     print(f"Report generated successfully at: {report_path}")
#     return report_html

# # Generate initial report on startup
# try:
#     generate_report()
#     print("Initial report generated successfully")
# except Exception as e:
#     print(f"Error generating initial report: {e}")
#     report_html = f"<h1>Error generating report</h1><pre>{str(e)}</pre>"

# # -------------------------------
# # FastAPI routes
# # -------------------------------
# @app.get("/")
# def index():
#     return {
#         "message": "Evidently Dashboard active. Visit /report to view drift results.",
#         "endpoints": {
#             "/": "This info page",
#             "/report": "View the data drift HTML report",
#             "/health": "Health check",
#             "/regenerate": "Regenerate the report (POST)"
#         }
#     }

# @app.get("/report", response_class=HTMLResponse)
# def show_report():
#     """Serve the generated Evidently HTML report"""
#     if report_html is None:
#         return HTMLResponse(
#             content="<h1>Report not generated yet</h1><p>Try calling POST /regenerate</p>",
#             status_code=404
#         )
#     return HTMLResponse(content=report_html, status_code=200)

# @app.get("/health")
# def health_check():
#     """Health check endpoint"""
#     return {
#         "status": "healthy",
#         "workspace_path": WORKSPACE_PATH,
#         "report_exists": os.path.exists(report_path),
#         "report_loaded": report_html is not None
#     }

# @app.post("/regenerate")
# def regenerate_report():
#     """Regenerate the report with fresh data"""
#     try:
#         generate_report()
#         return {
#             "message": "Report regenerated successfully",
#             "path": report_path
#         }
#     except Exception as e:
#         return {"error": str(e)}, 500

# if __name__ == "__main__":
#     import uvicorn
#     # Use 127.0.0.1 for Windows compatibility instead of 0.0.0.0
#     uvicorn.run(app, host="127.0.0.1", port=7000)


#############################################################################################
#############################################################################
#####################################################################
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

