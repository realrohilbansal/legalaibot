import mlflow

def log_experiment_params(params):
    for key, value in params.items():
        mlflow.log_param(key, value)

def log_experiment_metrics(metrics):
    for key, value in metrics.items():
        mlflow.log_metric(key, value)
