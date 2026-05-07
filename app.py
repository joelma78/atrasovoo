import streamlit as st
import datetime

st.subheader("✈️ Dados do voo")

# -----------------------
# COMPANHIA
# -----------------------
Airline = st.selectbox("Companhia aérea", ["GOL", "LATAM", "AZUL"])

# -----------------------
# AEROPORTOS
# -----------------------
aeroportos = ["GRU", "CGH", "BSB", "VIX", "SDU", "REC", "SSA"]

col1, col2 = st.columns(2)

with col1:
    Origin = st.selectbox("Origem", aeroportos)

with col2:
    Destination = st.selectbox("Destino", aeroportos)

# -----------------------
# DATA COMPLETA (mais profissional)
# -----------------------
data = st.date_input("Data do voo", datetime.date.today())

day = data.day
month = data.month

# -----------------------
# HORA (melhor que number_input)
# -----------------------
hour = st.slider("Hora do voo", 0, 23, 12)

# -----------------------
# DISTÂNCIA AUTOMÁTICA (simples e inteligente)
# -----------------------
distancias = {
    ("GRU", "VIX"): 1200,
    ("GRU", "BSB"): 850,
    ("GRU", "REC"): 2100,
    ("CGH", "BSB"): 900,
    ("BSB", "VIX"): 1000,
    ("SDU", "SSA"): 1600,
}

if Origin == Destination:
    Distance = 0
    st.warning("Origem e destino são iguais")
else:
    Distance = distancias.get((Origin, Destination)) or distancias.get((Destination, Origin), 1500)

st.info(f"Distância estimada: {Distance} km")

# -----------------------
# FIM DE SEMANA AUTOMÁTICO
# -----------------------
is_weekend = 1 if data.weekday() >= 5 else 0