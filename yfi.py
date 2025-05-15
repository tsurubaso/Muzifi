import yfinance as yf
import mplfinance as mpf
import pandas as pd
import os
from datetime import datetime
from mido import MidiFile, MidiTrack, Message, MetaMessage
import time

# ─────────────────────────────
# 🎯 PARAMÈTRES UTILISATEUR
# ─────────────────────────────
ticker = input("🎹 Code de l'entreprise (ex: AAPL, MSFT, TSLA) : ").upper()
period = input("⏱️ Période (ex: 1mo, 3mo, 6mo, 1y) : ").lower()
show_chart = input("Afficher le graphique ? (o/n) : ").strip().lower() == "o"

# ─────────────────────────────
# 🏢 NOM DE L'ENTREPRISE
# ─────────────────────────────
try:
    company_info = yf.Ticker(ticker).info
    company_name = company_info.get("longName", ticker)
except Exception:
    company_name = ticker

# ─────────────────────────────
# 📈 RÉCUPÉRATION DES DONNÉES
# ─────────────────────────────
print(f"\n📥 Téléchargement des données pour {company_name} ({ticker}) sur {period}...")
df = yf.download(ticker, period=period)

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

if df.empty:
    print("❌ Aucune donnée reçue.")
    exit()

# ─────────────────────────────
# ✅ NETTOYAGE
# ─────────────────────────────
required_cols = ["Open", "High", "Low", "Close", "Volume"]
df.dropna(inplace=True)

if not all(col in df.columns for col in required_cols):
    print("❌ Colonnes manquantes :", df.columns.tolist())
    exit()

try:
    df[required_cols] = df[required_cols].astype(float)
except Exception as e:
    print("❌ Erreur de conversion :", e)
    exit()

# ─────────────────────────────
# 🖼️ AFFICHAGE GRAPHIQUE
# ─────────────────────────────
period_scale_map = {
    "1d": 1.0, "5d": 1.2, "1mo": 1.3, "3mo": 1.5, "6mo": 1.8,
    "1y": 2.0, "2y": 2.3, "5y": 2.5, "10y": 3.0, "ytd": 2.0, "max": 3.5
}
figscale = period_scale_map.get(period, 1.5)

if show_chart:
    print("\n📊 Affichage du graphique...")
    mpf.plot(df, type="candle", style="charles", volume=True,
             title=f"{company_name} - {period}", figscale=figscale)
else:
    print("\n⏩ Graphique ignoré, passage direct à la musique...")

# ─────────────────────────────
# 🔄 NORMALISATION DES DONNÉES MUSICALES
# ─────────────────────────────
closes = df["Close"].values
min_price, max_price = closes.min(), closes.max()
min_vol, max_vol = df["Volume"].min(), df["Volume"].max()
min_range, max_range = (df["High"] - df["Low"]).min(), (df["High"] - df["Low"]).max()

def normalize_price_to_midi(price):
    return int(40 + (price - min_price) / (max_price - min_price) * (80 - 40))

def normalize_volume_to_duration(volume):
    return int(240 + (volume - min_vol) / (max_vol - min_vol) * (960 - 240))  # durée en ticks MIDI

def normalize_range_to_velocity(price_range):
    return int(20 + (price_range - min_range) / (max_range - min_range) * (100 - 20))

# ─────────────────────────────
# 🎼 CRÉATION DU FICHIER MIDI
# ─────────────────────────────
print("\n🎵 Création de la séquence musicale...")

# Dates pour le titre
start_date = df.index[0].strftime("%Y-%m-%d")
end_date = df.index[-1].strftime("%Y-%m-%d")
music_title = f"{company_name} ({start_date} to {end_date})"

# Création du fichier MIDI
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Ajout du titre
track.append(MetaMessage('track_name', name=music_title, time=0))

# Tempo fixe (ex: 120 BPM = 500000 microsec)
TEMPO = 500000  
track.insert(0, MetaMessage('set_tempo', tempo=TEMPO, time=0))

# Notes MIDI : durée et intensité dynamiques
for index, row in df.iterrows():
    note = normalize_price_to_midi(row["Close"])
    duration = normalize_volume_to_duration(row["Volume"])  
    velocity = normalize_range_to_velocity(row["High"] - row["Low"])  

    track.append(Message('note_on', note=note, velocity=velocity, time=0))
    track.append(Message('note_off', note=note, velocity=velocity, time=duration))

# ─────────────────────────────
# 💾 ENREGISTREMENT SUR LE BUREAU
# ─────────────────────────────
desktop_onedrive = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
desktop_local = os.path.join(os.path.expanduser("~"), "Desktop")
desktop_path = desktop_onedrive if os.path.exists(desktop_onedrive) else desktop_local
os.makedirs(desktop_path, exist_ok=True)

safe_title = f"{company_name}_{start_date}_to_{end_date}.mid".replace(" ", "_").replace(",", "")
midi_path = os.path.join(desktop_path, safe_title)

mid.save(midi_path)
print(f"\n✅ Fichier MIDI enregistré sur le bureau :\n{midi_path}")
