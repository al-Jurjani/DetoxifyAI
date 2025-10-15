import mlflow
import os
import dotenv

dotenv.load_dotenv()
os.getenv("MLFLOW_TRACKING_URI")

mlflow.set_experiment("local_test_azure_5")
with mlflow.start_run():
    mlflow.log_param("test_param", 13)
    mlflow.log_metric("accuracy", 0.1234)
    with open("upload_test_azure3.txt", "w") as f:
        f.write("this should appear in azure blob, third test")
    mlflow.log_artifact("upload_test_azure3.txt")
