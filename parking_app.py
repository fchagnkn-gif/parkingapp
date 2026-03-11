# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import datetime
import random
import pydeck as pdk

st.set_page_config(page_title="ParkoPrévision - Quartiers", layout="wide")
st.title("🚗 ParkoPrévision - Prototype Heatmap Quartiers")

# -----------------------------
# Zones / Quartiers (ajout de nouvelles zones pour couvrir toute la ville)
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
    # Nouvelles zones pour couverture complète
    {"Zone": "Senneville", "Lat": 45.4200, "Lon": -73.8500, "Prix": 2.0, "Places_totales": 10},
    {"Zone": "Saint-Laurent", "Lat": 45.5000, "Lon": -73.7000, "Prix": 2.5, "Places_totales": 25},
    {"Zone": "Anjou", "Lat": 45.5700, "Lon": -73.5500, "Prix": 2.0, "Places_totales": 18},
    {"Zone": "Mont-Royal", "Lat": 45.5200, "Lon": -73.6300, "Prix": 3.0, "Places_totales": 12},
]

# -----------------------------
# Simuler places libres et proba
# -----------------------------
for z in zones:
    z["Places_libres"] = random.randint(max(1, int(z["Places_totales"]*0.1)), z["Places_totales"])
    z["Proba_libre"] = z["Places_libres"] / z["Places_totales"]

parking_data = pd.DataFrame(zones)

# -----------------------------
# Polygones approximatifs pour chaque quartier
# -----------------------------
def create_polygon(lat, lon, size=0.004):
    """Crée un carré approximatif autour du centre"""
    return [
        [lon - size, lat - size],
        [lon - size, lat + size],
        [lon + size, lat + size],
        [lon + size, lat - size]
    ]

parking_data["polygon"] = parking_data.apply(lambda r: create_polygon(r["Lat"], r["Lon"]), axis=1)

# -----------------------------
# Couleur semi-transparente vert → jaune → rouge
# -----------------------------
def color_from_proba(p):
    r = int(255*(1-p))
    g = int(255*p)
    return [r, g, 0, 120]  # alpha 120 pour semi-transparence

parking_data["color"] = parking_data["Proba_libre"].apply(color_from_proba)

# -----------------------------
# Pydeck Layer Polygon
# -----------------------------
st.subheader("Carte des quartiers - Heatmap")

layer = pdk.Layer(
    "PolygonLayer",
    data=parking_data,
    get_polygon="polygon",
    get_fill_color="color",
    pickable=True,
    auto_highlight=True,
    extruded=False,
    get_line_color=[0,0,0],
)

# Pour afficher les places libres sur le hover
tooltip = {
    "html": "<b>{Zone}</b><br>Prix: {Prix}$ /h<br>Places libres: {Places_libres}/{Places_totales}<br>Proba libre: {Proba_libre}",
    "style": {"backgroundColor": "white", "color": "black"}
}

view_state = pdk.ViewState(latitude=45.52, longitude=-73.57, zoom=11)
r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
st.pydeck_chart(r)

# -----------------------------
# Tableau résumé
# -----------------------------
st.subheader("Résumé des quartiers")
parking_data_display = parking_data[["Zone","Prix","Places_libres","Places_totales","Proba_libre"]].copy()
parking_data_display["Proba_libre (%)"] = (parking_data_display["Proba_libre"]*100).round(0)
st.dataframe(parking_data_display.rename(columns={
    "Prix":"Prix ($/h)",
    "Places_libres":"Places libres",
    "Places_totales":"Places totales"
}))

# -----------------------------
# Choix zone et durée
# -----------------------------
st.subheader("Choisir un quartier et durée")
zone = st.selectbox("Quartier", parking_data["Zone"])
zone_info = parking_data[parking_data["Zone"]==zone].iloc[0]

st.write(f"💰 Prix : {zone_info['Prix']} $ / heure")
st.write(f"🅿️ Places libres : {zone_info['Places_libres']} / {zone_info['Places_totales']}")

duree = st.slider("Durée du stationnement (minutes)", 15, 180, 60)
prix_total = zone_info["Prix"]*(duree/60)
st.write(f"💵 Prix estimé : {round(prix_total,2)} $")

# -----------------------------
# Commencer stationnement
# -----------------------------
if "fin_stationnement" not in st.session_state:
    st.session_state.fin_stationnement = None

if st.button("▶️ Commencer le stationnement"):
    st.session_state.fin_stationnement = datetime.datetime.now() + datetime.timedelta(minutes=duree)
    st.success("Stationnement activé !")

# -----------------------------
# Timer
# -----------------------------
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

# -----------------------------
# Extension
# -----------------------------
if st.session_state.fin_stationnement:
    if st.button("➕ Ajouter 30 minutes"):
        st.session_state.fin_stationnement += datetime.timedelta(minutes=30)
        st.success("Temps ajouté !")

# -----------------------------
# Simulation paiement
# -----------------------------
st.subheader("Paiement")
if st.button("💳 Payer"):
    st.success("Paiement simulé réussi ✅")

# -----------------------------
# Historique
# -----------------------------
st.subheader("Historique (simulation)")
history = pd.DataFrame({
    "Quartier":[z["Zone"] for z in zones[:5]],
    "Durée":["60 min","45 min","90 min","30 min","120 min"],
    "Prix":["3.50$","3.75$","4.50$","2.50$","4.00$"]
})
st.table(history)
