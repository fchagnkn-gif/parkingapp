# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import datetime
import random

st.set_page_config(page_title="ParkoPrévision", layout="wide")
st.title("🚗 ParkoPrévision - Prototype")

# -----------------------------
# Données simulées de stationnement (plus de zones)
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

# Ajouter Places libres simulées
for z in zones:
    # Places libres entre 10% et 100% des places totales
    z["Places_libres"] = random.randint(max(1, int(z["Places_totales"]*0.1)), z["Places_totales"])

parking_data = pd.DataFrame(zones)

# -----------------------------
# Carte
# -----------------------------
st.subheader("Carte des zones de stationnement")
st.map(parking_data.rename(columns={"Lat":"lat", "Lon":"lon"}))

# -----------------------------
# Tableau des zones
# -----------------------------
st.subheader("Résumé des zones de stationnement")
st.dataframe(parking_data[["Zone","Prix","Places_libres","Places_totales"]].rename(
    columns={"Prix":"Prix ($/h)", "Places_libres":"Places libres", "Places_totales":"Places totales"}
))

# -----------------------------
# Choix de zone
# -----------------------------
st.subheader("Choisir une zone")
zone = st.selectbox("Zone de stationnement", parking_data["Zone"])
zone_info = parking_data[parking_data["Zone"]==zone].iloc[0]

st.write(f"💰 Prix : {zone_info['Prix']} $ / heure")
st.write(f"🅿️ Places libres : {zone_info['Places_libres']} / {zone_info['Places_totales']}")

# -----------------------------
# Prévision de disponibilité
# -----------------------------
st.subheader("Prévision de disponibilité (simulation)")

# On simule une prévision à 1h
tendance = random.choice(["stable", "plus de places", "moins de places"])
st.write(f"Dans 1h, la tendance sera : **{tendance}**")

# -----------------------------
# Durée et prix
# -----------------------------
st.subheader("Durée du stationnement")
duree = st.slider("Choisir la durée (minutes)", 15, 180, 60)
prix_total = zone_info["Prix"] * (duree/60)
st.write(f"💵 Prix estimé : {round(prix_total,2)} $")

# -----------------------------
# Démarrer stationnement
# -----------------------------
if "fin_stationnement" not in st.session_state:
    st.session_state.fin_stationnement = None

if st.button("▶️ Commencer le stationnement"):
    st.session_state.fin_stationnement = datetime.datetime.now() + datetime.timedelta(minutes=duree)
    st.success("Stationnement activé !")

# -----------------------------
# Timer actif
# -----------------------------
if st.session_state.fin_stationnement:
    st.subheader("⏱ Stationnement actif")
    restant = st.session_state.fin_stationnement - datetime.datetime.now()
    minutes_restantes = int(restant.total_seconds() / 60)
    if minutes_restantes > 0:
        st.metric("Temps restant (minutes)", minutes_restantes)
        if minutes_restantes < 10:
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
# Simulation de paiement
# -----------------------------
st.subheader("Paiement")
if st.button("💳 Payer"):
    st.success("Paiement simulé réussi ✅")

# -----------------------------
# Historique
# -----------------------------
st.subheader("Historique (simulation)")
history = pd.DataFrame({
    "Zone":[z["Zone"] for z in zones[:5]],
    "Durée":["60 min","45 min","90 min","30 min","120 min"],
    "Prix":["3.50$","3.75$","4.50$","2.50$","4.00$"]
})
st.table(history)