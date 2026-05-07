from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

# carregar modelo e colunas
model = joblib.load("models/best_model.pkl")
columns = joblib.load("models/columns.pkl")


@app.get("/")
def home():
    return {"message": "API de previsão de atraso de voos está funcionando 🚀"}


@app.post("/predict")
def predict(data: dict):

    # transformar input em DataFrame
    df = pd.DataFrame([data])

    # garantir mesmas colunas do treino
    df = pd.get_dummies(df)
    df = df.reindex(columns=columns, fill_value=0)

    # previsão
    prediction = model.predict(df)[0]

    return {
        "prediction": int(prediction)
    }