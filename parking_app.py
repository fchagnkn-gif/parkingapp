# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random
import pydeck as pdk

st.set_page_config(page_title="ParkoPrévision - Full City Heatmap", layout="wide")
st.title("🚗 ParkoPrévision - Heatmap complète et interactive")

# -----------------------------
# Définition des bornes de Montréal pour maillage
# -----------------------------
lat_min, lat_max = 45.44, 45.58
lon_min, lon_max = -73.76, -73.54

# Nombre de divisions (mini-zones)
n_lat, n_lon = 20, 25  # ajuste pour plus ou moins de mini-zones

lat_vals = np.linspace(lat_min, lat_max, n_lat)
lon_vals = np.linspace(lon_min, lon_max, n_lon)

mini_zones = []

for lat in lat_vals:
    for lon in lon_vals:
        # Simuler prix et places (randomisé pour prototype)
        prix = round(random.uniform(2.0, 6.0), 2)
        places_totales = random.randint(5, 25)
        places_libres = random.randint(0, places_totales)
        mini_zones.append({
            "Lat": lat + np.random.normal(scale=0.0005),  # léger jitter
            "Lon": lon + np.random.normal(scale=0.0005),
            "Prix": prix,
            "Places_totales": places_totales,
            "Places_libres": places_libres,
            "Proba_libre": places_libres / max(1, places_totales)
        })

mini_df = pd.DataFrame(mini_zones)

# -----------------------------
# Heatmap
# -----------------------------
st.subheader("Carte interactive - Heatmap + Mini-zones")

heat_layer = pdk.Layer(
    "HeatmapLayer",
    data=mini_df,
    get_position=["Lon","Lat"],
    get_weight="Proba_libre",
    radiusPixels=100,  # plus grand rayon pour rester visible au zoom
    intensity=3,
    threshold=0.05
)

# Scatterplot pour les mini-zones (cliquable)
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=mini_df,
    get_position=["Lon","Lat"],
    get_fill_color=[0,128,255,200],
    get_radius=150,
    pickable=True
)

tooltip = {
    "html": "Prix: {Prix}$ /h<br>Places libres: {Places_libres} / {Places_totales}<br>Proba libre: {Proba_libre}",
    "style": {"color":"white"}
}

view_state = pdk.ViewState(latitude=45.52, longitude=-73.57, zoom=11, pitch=0)
r = pdk.Deck(
    layers=[heat_layer, scatter_layer],
    initial_view_state=view_state,
    tooltip=tooltip
)

st.pydeck_chart(r)

# -----------------------------
# Tableau résumé
# -----------------------------
st.subheader("Résumé des mini-zones")
mini_display = mini_df.copy()
mini_display["Proba_libre (%)"] = (mini_display["Proba_libre"]*100).round(0)
st.dataframe(mini_display[["Lat","Lon","Prix","Places_libres","Places_totales","Proba_libre (%)"]])

# -----------------------------
# Stationnement simulé
# -----------------------------
st.subheader("Simulation stationnement")
duree = st.slider("Durée du stationnement (minutes)", 15, 180, 60)
prix_total = mini_df["Prix"].mean() * (duree / 60)
st.write(f"💵 Prix estimé moyen : {round(prix_total,2)} $")

if "fin_stationnement" not in st.session_state:
    st.session_state.fin_stationnement = None

if st.button("▶️ Commencer le stationnement"):
    st.session_state.fin_stationnement = datetime.datetime.now() + datetime.timedelta(minutes=duree)
    st.success("Stationnement activé !")

if st.session_state.fin_stationnement:
    restant = st.session_state.fin_stationnement - datetime.datetime.now()
    minutes_restantes = int(restant.total_seconds()/60)
    st.subheader("⏱ Stationnement actif")
    if minutes_restantes>0:
        st.metric("Temps restant (minutes)", minutes_restantes)
        if minutes_restantes<10:
            st.warning("⚠️ Stationnement expire bientôt !")
    else:
        st.error("⛔ Stationnement expiré")
