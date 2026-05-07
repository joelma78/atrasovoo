import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

import mlflow
import mlflow.sklearn

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from preprocessing import preprocess_data


def train():

    # MLflow 
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("flight-delay-model")

    # pasta modelos
    os.makedirs("models", exist_ok=True)

    # carregar dados
    df = pd.read_parquet("data/processed/flights.parquet")
    df = preprocess_data(df)

    # features
    features = [
        "Airline", "Origin", "Destination",
        "hour", "day", "month",
        "Distance", "is_weekend"
    ]

    X = df[features]
    y = df["delay"]

    X = pd.get_dummies(X, drop_first=True)

    # salvar colunas
    joblib.dump(list(X.columns), "models/columns.pkl")

    # split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # modelos
    models = {
        "RandomForest": RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            random_state=42,
            class_weight="balanced"
        ),

        "LogisticRegression": LogisticRegression(max_iter=1000),

        "XGBoost": XGBClassifier(
            n_estimators=150,
            max_depth=6,
            learning_rate=0.1,
            eval_metric="logloss"
        )
    }

    best_acc = 0
    best_model = None
    best_name = None

    # 🔥 LOOP ÚNICO E CORRETO
    for name, model in models.items():

        with mlflow.start_run(run_name=name):

            # treino
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            # métricas
            acc = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            # log MLflow
            mlflow.log_param("model_name", name)

            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.log_metric("f1", f1)

            mlflow.sklearn.log_model(model, "model")

            print(f"{name} -> Accuracy: {acc:.4f}")

            # melhor modelo
            if acc > best_acc:
                best_acc = acc
                best_model = model
                best_name = name

    # salvar melhor modelo
    joblib.dump(best_model, "models/best_model.pkl")

    print("\n====================")
    print("🏆 MELHOR MODELO FINAL")
    print("====================")
    print("Modelo:", best_name)
    print("Accuracy:", round(best_acc, 4))

    return best_model


if __name__ == "__main__":
    train()