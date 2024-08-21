import mlflow
from mlflow import log_metric, log_param, log_artifact

def setup_mlflow():
    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("legalai_experiment")
