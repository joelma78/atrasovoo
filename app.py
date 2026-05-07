import streamlit as st
import datetime
import requests

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(
    page_title="Previsão de Atraso de Voos",
    page_icon="✈️",
    layout="centered"
)

st.title("✈️ Previsão de Atraso de Voos")
st.markdown("Planeje sua viagem")

st.markdown("---")

# -----------------------
# COMPANHIA
# -----------------------
airline = st.selectbox(
    "Companhia aérea",
    ["GOL", "LATAM", "AZUL"]
)

# -----------------------
# AEROPORTOS
# -----------------------
aeroportos = [
    "GRU",
    "CGH",
    "BSB",
    "VIX",
    "SDU",
    "REC",
    "SSA"
]

col1, col2 = st.columns(2)

with col1:
    origin = st.selectbox("Origem", aeroportos)

with col2:
    destination = st.selectbox("Destino", aeroportos)

# -----------------------
# DATA
# -----------------------
data = st.date_input(
    "Data do voo",
    datetime.date.today()
)

day = data.day
month = data.month

# -----------------------
# HORA
# -----------------------
hour = st.slider(
    "Hora do voo",
    0,
    23,
    12
)

# -----------------------
# DISTÂNCIAS
# -----------------------
distancias = {
    ("GRU", "VIX"): 1200,
    ("GRU", "BSB"): 850,
    ("GRU", "REC"): 2100,
    ("CGH", "BSB"): 900,
    ("BSB", "VIX"): 1000,
    ("SDU", "SSA"): 1600,
}

if origin == destination:
    distance = 0
    st.warning("Origem e destino são iguais")
else:
    distance = (
        distancias.get((origin, destination))
        or distancias.get((destination, origin))
        or 1500
    )

st.info(f"📏 Distância estimada: {distance} km")

# -----------------------
# FIM DE SEMANA
# -----------------------
is_weekend = 1 if data.weekday() >= 5 else 0

st.markdown("---")

# -----------------------
# BOTÃO PREVISÃO
# -----------------------
if st.button(" Prever atraso", use_container_width=True):

    dados = {
        "Airline": airline,
        "Origin": origin,
        "Destination": destination,
        "hour": hour,
        "day": day,
        "month": month,
        "Distance": distance,
        "is_weekend": is_weekend
    }

    try:

        response = requests.post(
            "https://atraso-voo-api.onrender.com/predict",
            json=dados
        )

        resultado = response.json()["prediction"]

        st.markdown("## Resultado da previsão")

        if resultado >= 0.7:
            st.error(
                f"⚠️ Alta chance de atraso ({resultado:.0%})"
            )

        elif resultado >= 0.4:
            st.warning(
                f"🟡 Risco moderado ({resultado:.0%})"
            )

        else:
            st.success(
                f"🟢 Baixo risco ({resultado:.0%})"
            )

    except Exception as e:
        st.error(f"Erro ao conectar API: {e}")