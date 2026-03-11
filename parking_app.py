# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import datetime
import random
import pydeck as pdk
import numpy as np

st.set_page_config(page_title="ParkoPrévision - Mini-zones", layout="wide")
st.title("🚗 ParkoPrévision - Mini-zones interactives")

# -----------------------------
# Zones principales
# -----------------------------
zones = [
    {"Zone": "Plateau", "Lat": 45.525, "Lon": -73.5817, "Prix": 3.5, "Places_totales": 20},
    {"Zone": "Centre-ville", "Lat": 45.5017, "Lon": -73.5673, "Prix": 5.0, "Places_totales": 30},
    {"Zone": "Vieux-Montréal", "Lat": 45.5075, "Lon": -73.5540, "Prix": 6.0, "Places_totales": 15},
    {"Zone": "Mile-End", "Lat": 45.5270, "Lon": -73.5900, "Prix": 3.0, "Places_totales": 25},
    {"Zone": "Griffintown", "Lat": 45.4949, "Lon": -73.5550, "Prix": 4.5, "Places_totales": 18},
    {"Zone": "Hochelaga", "Lat": 45.5600, "Lon": -73.5400, "Prix": 2.5, "Places_totales": 22},
    {"Zone": "Rosemont", "Lat": 45.5500, "Lon": -73.6000, "Prix": 3.0, "Places_totales": 20},
    {"Zone": "NDG", "Lat": 45.4700, "Lon": -73.6500, "Prix": 2.0, "Places_totales": 15},
    {"Zone": "Ahuntsic", "Lat": 45.5800, "Lon": -73.6500, "Prix": 2.5, "Places_totales": 18},
    {"Zone": "Lachine", "Lat": 45.4500, "Lon": -73.6250, "Prix": 2.0, "Places_totales": 12},
    {"Zone": "Verdun", "Lat": 45.4700, "Lon": -73.5800, "Prix": 2.5, "Places_totales": 14},
    {"Zone": "Westmount", "Lat": 45.4900, "Lon": -73.5840, "Prix": 4.0, "Places_totales": 10},
    {"Zone": "Villeray", "Lat": 45.5500, "Lon": -73.6200, "Prix": 3.0, "Places_totales": 20},
    {"Zone": "Saint-Henri", "Lat": 45.4750, "Lon": -73.5900, "Prix": 3.5, "Places_totales": 16},
    {"Zone": "Pointe-Claire", "Lat": 45.4500, "Lon": -73.7560, "Prix": 2.5, "Places_totales": 12},
]

# -----------------------------
# Créer mini-zones autour de chaque zone
# -----------------------------
mini_zones = []
for z in zones:
    n_subzones = 6  # 6 mini-zones par zone
    for i in range(n_subzones):
        lat_jitter = z["Lat"] + np.random.normal(scale=0.003)
        lon_jitter = z["Lon"] + np.random.normal(scale=0.003)
        places_libres = random.randint(0, max(1, z["Places_totales"] // n_subzones))
        mini_zones.append({
            "Zone": z["Zone"],
            "Lat": lat_jitter,
            "Lon": lon_jitter,
            "Prix": z["Prix"],
            "Places_libres": places_libres,
            "Places_totales": z["Places_totales"] // n_subzones,
            "Proba_libre": places_libres / max(1, z["Places_totales"] // n_subzones)
        })

mini_df = pd.DataFrame(mini_zones)

# -----------------------------
# Heatmap continu
# -----------------------------
st.subheader("Carte interactive - Heatmap + Mini-zones")

# Heatmap basé sur toutes les mini-zones
heat_layer = pdk.Layer(
    "HeatmapLayer",
    data=mini_df,
    get_position=["Lon", "Lat"],
    get_weight="Proba_libre",
    radiusPixels=80,
    intensity=2,
    threshold=0.05,
    color_range=[
        [0,255,0,80],    # vert
        [255,255,0,120], # jaune
        [255,0,0,180]    # rouge
    ]
)

# Scatterplot pour cliquer et montrer places dispo
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=mini_df,
    get_position=["Lon","Lat"],
    get_fill_color=[0,128,255,200],
    get_radius=200,
    pickable=True
)

# Tooltip avec nombre de places dispo
tooltip = {
    "html": "<b>{Zone}</b><br>Prix: {Prix}$ /h<br>Places libres: {Places_libres} / {Places_totales}<br>Proba libre: {Proba_libre}",
    "style":{"color":"white"}
}

view_state = pdk.ViewState(latitude=45.52, longitude=-73.57, zoom=11, pitch=0)
deck = pdk.Deck(
    layers=[heat_layer, scatter_layer],
    initial_view_state=view_state,
    tooltip=tooltip
)
st.pydeck_chart(deck)

# -----------------------------
# Tableau résumé des zones
# -----------------------------
st.subheader("Résumé par mini-zone")
mini_display = mini_df[["Zone","Prix","Places_libres","Places_totales","Proba_libre"]].copy()
mini_display["Proba_libre (%)"] = (mini_display["Proba_libre"]*100).round(0)
st.dataframe(mini_display)
