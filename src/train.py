# libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

# 1. INIZIALIZZIAMO MLFLOW
mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("Comparazione Modello Iris")

print("Caricamento dati...")
# 2. Carico i dati
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = pd.Series(iris.target, name="target")

# Manteniamo un set di test per la matrice di confusione
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print("Dati pronti.")

# 3. Definiamo i modelli
models = {
    "LogisticRegression": LogisticRegression(max_iter=200),
    "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
}

# 4. Addestriamo e valutiamo ogni modello
for name, model in models.items():
    print(f"--- Valutazione del modello: {name} ---")

    with mlflow.start_run(run_name=name) as run:

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # A. Calcoliamo e registriamo le metriche sul singolo test set
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average="weighted")
        recall = recall_score(y_test, y_pred, average="weighted")
        f1 = f1_score(y_test, y_pred, average="weighted")

        print(
            f"Accuracy (Test Set): {accuracy:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}, F1-Score: {f1:.4f}"
        )

        mlflow.log_metric("accuracy_test", accuracy)
        mlflow.log_metric("precision_test", precision)
        mlflow.log_metric("recall_test", recall)
        mlflow.log_metric("f1_score_test", f1)

        # Cross-Validation per notare cambiamenti di scelta
        cv_scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
        mean_cv_accuracy = np.mean(cv_scores)
        std_cv_accuracy = np.std(cv_scores)

        print(
            f"Accuratezza Media da CV: {mean_cv_accuracy:.4f} (+/- {std_cv_accuracy:.4f})"
        )
        # new
        mlflow.log_metric("cv_accuracy_mean", mean_cv_accuracy)
        mlflow.log_metric("cv_accuracy_std", std_cv_accuracy)

        mlflow.log_params(model.get_params())

        cm = confusion_matrix(y_test, y_pred)
        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm, display_labels=iris.target_names
        )
        fig, ax = plt.subplots()
        disp.plot(ax=ax)
        mlflow.log_figure(fig, "confusion_matrix.png")
        # save
        mlflow.sklearn.log_model(model, "model")

        print(f"Modello {name} e metriche salvate su MLflow.")

print("\n--- Training dei mod completato! ---")
