import mlflow
import mlflow.sklearn
import os
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score, recall_score

# --- Configuration ---
MLFLOW_TRACKING_URI = os.environ['MLFLOW_TRACKING_URI']
REGISTERED_MODEL_NAME = "IrisClassifierProduction"
# --- 1. Set up MLflow Tracking ---
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
# --- 2. Load Data ---
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)
# --- 3. Start an MLflow Experiment Run ---
with mlflow.start_run(run_name="Production_Candidate_Training") as run:
    print("Starting MLflow run with ID:", run.info.run_id)
    # --- 4. Log Hyperparameters ---
    n_estimators = 150
    max_depth = 10
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    # --- 5. Train the Model ---
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    model.fit(X_train, y_train)
    # --- 6. Evaluate and Log Metrics ---
    predictions = model.predict(X_test) #y_pred
    predictions_score= model.predict_proba(X_test)[:, 1] #y_score

    accuracy = accuracy_score(y_test, predictions)
    print("Model Accuracy:", accuracy)
    mlflow.log_metric("accuracy", accuracy)
    
    recall = recall_score(y_test, predictions)
    print("Model Recall:", recall)
    mlflow.log_metric("recall", recall)
    
    f1 = f1_score(y_test, predictions)
    print("Model F1 Score:", f1)
    mlflow.log_metric("f1_score", f1)
    
    auc = roc_auc_score(y_test, predictions_score)
    print("Model ROC AUC:", auc)
    mlflow.log_metric("auc", auc)


    # --- 7. Log and Register the Model ---
    # The `registered_model_name` argument creates a new version in the Model Registry
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name=REGISTERED_MODEL_NAME,
    )
print("\n--- Script Finished ---")