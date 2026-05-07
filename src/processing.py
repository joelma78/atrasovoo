import duckdb
import duckdb
import pandas as pd
import os

def process_data():

    os.makedirs('data/processed', exist_ok=True)

    con = duckdb.connect()

    # carregar CSV
    df = pd.read_csv('data/raw/flight_delays.csv')

    # registrar tabela
    con.register('flights', df)

    # transformação com SQL (com CAST corrigido)
    result = con.execute("""
        SELECT
            Airline,
            Origin,
            Destination,
            Distance,
            DelayMinutes,

            CAST(ScheduledDeparture AS TIMESTAMP) AS ScheduledDeparture,

            EXTRACT(HOUR FROM CAST(ScheduledDeparture AS TIMESTAMP)) AS hour,
            EXTRACT(DAY FROM CAST(ScheduledDeparture AS TIMESTAMP)) AS day,
            EXTRACT(MONTH FROM CAST(ScheduledDeparture AS TIMESTAMP)) AS month,

            CASE 
                WHEN EXTRACT(DOW FROM CAST(ScheduledDeparture AS TIMESTAMP)) IN (0,6) THEN 1 
                ELSE 0 
            END AS is_weekend,

            CASE 
                WHEN DelayMinutes > 15 THEN 1 
                ELSE 0 
            END AS delay

        FROM flights
    """).df()

    # salvar parquet
    result.to_parquet('data/processed/flights.parquet', index=False)

    print("✅ Dados processados salvos em data/processed/")

if __name__ == "__main__":
    process_data()