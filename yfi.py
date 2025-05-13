import yfinance as yf
import mplfinance as mpf
import pandas as pd
import os
from datetime import datetime
from mido import MidiFile, MidiTrack, Message, MetaMessage

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
required_cols = ["Open", "High", "Low", "Close"]
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
# 🎼 CRÉATION DU FICHIER MIDI
# ─────────────────────────────
print("\n🎵 Création de la séquence musicale...")

closes = df["Close"].values
min_price = closes.min()
max_price = closes.max()

# Normalisation : prix → note MIDI (entre 40 et 80)
def normalize_price_to_midi(price):
    return int(40 + (price - min_price) / (max_price - min_price) * (80 - 40))

# Dates pour le titre
start_date = df.index[0].strftime("%Y-%m-%d")
end_date = df.index[-1].strftime("%Y-%m-%d")

# Création du fichier MIDI
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Ajout du titre (Audacity le lit parfois)
music_title = f"{company_name} ({start_date} to {end_date})"
track.append(MetaMessage('track_name', name=music_title, time=0))

# Tempo fixe pour mélange (ex: 120 BPM = 500000 microsec)
TEMPO = 500000  # 120 BPM
track.insert(0, MetaMessage('set_tempo', tempo=TEMPO, time=0))

# Notes MIDI : une par cours de clôture
for price in closes:
    note = normalize_price_to_midi(price)
    track.append(Message('note_on', note=note, velocity=64, time=0))
    track.append(Message('note_off', note=note, velocity=64, time=480))  # durée = 1 noire

# ─────────────────────────────
# 💾 ENREGISTREMENT SUR LE BUREAU
# ─────────────────────────────
desktop_onedrive = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
desktop_local = os.path.join(os.path.expanduser("~"), "Desktop")
desktop_path = desktop_onedrive if os.path.exists(desktop_onedrive) else desktop_local
os.makedirs(desktop_path, exist_ok=True)

# Nom du fichier
safe_title = f"{company_name}_{start_date}_to_{end_date}.mid".replace(" ", "_").replace(",", "")
midi_path = os.path.join(desktop_path, safe_title)

mid.save(midi_path)
print(f"\n✅ Fichier MIDI enregistré sur le bureau :\n{midi_path}")
