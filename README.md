# DetoxifyAI

to run MLFlow + Azure:

1.) activate virtual environemnt
2.) cd to MLFlow/experiments
3.) First have the mlflow dashboard running by entering 'the command' (in Zuhair's sticky note on desktop)
4.) Then, you'll have the dashboard running. Now you can safely begin testing runs by the command:

    $env:MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
    mlflow run . --env-manager=local --experiment-name xg_models

    for xgboost model experiments, or alternatively

    $env:MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
    mlflow run . --env-manager=local --experiment-name lr_models

    for logistic regression model experiements

5.) Once run is complete, it should show up on the mlflow dashboard, and the stored model, vectorizer, and the metrics recorded will inshaAllah be on the Azure blob storage.



to run Prometheus + Grafana:
1.) At the root of your project folder, run docker compose up --build
2.) This may take a while at first, at it is loading the three images.
3.) Once docker loads them up, your fastapi, prometheus, and grafana should be running on the following three links respectively:

    http://localhost:8000/metrics
    http://localhost:9090
    http://localhost:3000/

4.) now you do the stuff you're supposed to do with prometheus and grafana