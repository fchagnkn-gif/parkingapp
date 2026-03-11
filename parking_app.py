# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="ParkoPrévision - Map Zones", layout="wide")
st.title("🚗 ParkoPrévision - Carte interactive des zones")

# -----------------------------
# Zones et places totales (fixes)
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
# Simuler places libres et proba
# -----------------------------
for z in zones:
    z["Places_libres"] = random.randint(max(1,int(z["Places_totales"]*0.1)), z["Places_totales"])
    z["Proba_libre"] = z["Places_libres"] / z["Places_totales"]

parking_data = pd.DataFrame(zones)

# -----------------------------
# Fonction pour couleur (rouge → vert)
# -----------------------------
def color_from_proba(p):
    r = int(255*(1-p))
    g = int(255*p)
    return f"#{r:02x}{g:02x}00"

# -----------------------------
# Carte folium
# -----------------------------
m = folium.Map(location=[45.52, -73.57], zoom_start=11)

for _, row in parking_data.iterrows():
    folium.CircleMarker(
        location=[row["Lat"], row["Lon"]],
        radius=30,
        color=color_from_proba(row["Proba_libre"]),
        fill=True,
        fill_color=color_from_proba(row["Proba_libre"]),
        fill_opacity=0.6,
        popup=folium.Popup(f"<b>{row['Zone']}</b><br>Prix: {row['Prix']}$ /h<br>Places libres: {row['Places_libres']} / {row['Places_totales']}<br>Proba: {round(row['Proba_libre']*100)}%", max_width=300)
    ).add_to(m)

# Affiche carte dans Streamlit
st_folium(m, width=700, height=500)

# -----------------------------
# Tableau
# -----------------------------
st.subheader("Résumé des zones")
parking_data_display = parking_data[["Zone","Prix","Places_libres","Places_totales","Proba_libre"]].copy()
parking_data_display["Proba_libre (%)"] = (parking_data_display["Proba_libre"]*100).round(0)
st.dataframe(parking_data_display.rename(columns={"Prix":"Prix ($/h)","Places_libres":"Places libres","Places_totales":"Places totales"}))