import pandas as pd
import joblib


from src.preprocessing import preprocess_data

def load_model():
    return joblib.load('models/modelo_atraso_voos.pkl')


def load_columns():
    return joblib.load('models/columns.pkl')


def predict(input_data: dict):

    model = load_model()
    columns = load_columns()

    # transformar entrada em DataFrame
    df = pd.DataFrame([input_data])

    # ⚠️ aplicar mesmas transformações de tempo
    df['ScheduledDeparture'] = pd.to_datetime(df['ScheduledDeparture'])

    df['hour'] = df['ScheduledDeparture'].dt.hour
    df['day'] = df['ScheduledDeparture'].dt.day
    df['month'] = df['ScheduledDeparture'].dt.month
    df['is_weekend'] = df['ScheduledDeparture'].dt.dayofweek >= 5
    df['is_weekend'] = df['is_weekend'].astype(int)

    # selecionar mesmas features do treino
    features = [
        'Airline', 'Origin', 'Destination',
        'hour', 'day', 'month',
        'Distance', 'is_weekend'
    ]

    df = df[features]

    # encoding
    df = pd.get_dummies(df)

    # 🔥 alinhar colunas com treino
    df = df.reindex(columns=columns, fill_value=0)

    prediction = model.predict(df)

    return int(prediction[0])