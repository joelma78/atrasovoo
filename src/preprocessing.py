import pandas as pd

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:

    # converter data
    df['ScheduledDeparture'] = pd.to_datetime(df['ScheduledDeparture'])

    # features de tempo
    df['hour'] = df['ScheduledDeparture'].dt.hour
    df['day'] = df['ScheduledDeparture'].dt.day
    df['month'] = df['ScheduledDeparture'].dt.month

    df['is_weekend'] = df['ScheduledDeparture'].dt.dayofweek >= 5
    df['is_weekend'] = df['is_weekend'].astype(int)

    # label (caso não exista ainda)
    if 'delay' not in df.columns:
        df['delay'] = (df['DelayMinutes'] > 15).astype(int)

    # remover colunas com vazamento (se existirem)
    df = df.drop(columns=[
        'DelayReason',
        'ActualDeparture',
        'ActualArrival',
        'ScheduledArrival'
    ], errors='ignore')

    # remover nulos
    df = df.dropna()

    return df