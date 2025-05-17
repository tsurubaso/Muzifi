import yfinance as yf
import mplfinance as mpf
import pandas as pd
import os
from datetime import datetime
from mido import MidiFile, MidiTrack, Message, MetaMessage
import re

# ─────────────────────────────
# 🧠 PARAMÈTRES BASÉS SUR L'ENTREPRISE
# ─────────────────────────────
def extract_founding_year(description, default_year=1985):
    match = re.search(r"(founded|incorporated) in (\d{4})", description.lower())
    if match:
        return int(match.group(2))
    return default_year

def get_company_timing_parameters(info):
    current_year = datetime.now().year
    founded = extract_founding_year(info.get("longBusinessSummary", ""), 1985)
    age = current_year - founded

    pitch_shift = max(0, min(30, 30 - age // 3))      # jeunes = sons plus aigus
    tempo = int(700000 - min(500000, age * 5000))     # jeunes = tempo plus rapide

    return pitch_shift, tempo

def assign_instrument_by_age(info):
    current_year = datetime.now().year
    founded = extract_founding_year(info.get("longBusinessSummary", ""), 1985)
    age = current_year - founded

    instrument_by_age = [
        (100, [32, 33, 34]),  # Basses (vieux)
        (60, [24, 25, 26]),   # Guitares
        (30, [0, 1, 2]),      # Pianos
        (15, [40, 41, 42]),   # Violons
        (0, [72, 73, 74])     # Flûtes (jeunes)
    ]

    for limit, instruments in reversed(instrument_by_age):
        if age >= limit:
            return instruments[age % len(instruments)]
    return 0

# ─────────────────────────────
# 🎯 PARAMÈTRES UTILISATEUR
# ─────────────────────────────
ticker = input("🎹 Code de l'entreprise (ex: AAPL, MSFT, TSLA) : ").upper()
period = input("⏱️ Période (ex: 1mo, 3mo, 6mo, 1y) : ").lower()
show_chart = input("Afficher le graphique ? (o/n) : ").strip().lower() == "o"

# ─────────────────────────────
# 📈 RÉCUPÉRATION DES DONNÉES
# ─────────────────────────────
print(f"\n📥 Téléchargement des données pour {ticker} sur {period}...")
df = yf.download(ticker, period=period)

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

if df.empty:
    print("❌ Aucune donnée reçue.")
    exit()

required_cols = ["Open", "High", "Low", "Close", "Volume"]
df.dropna(inplace=True)

if not all(col in df.columns for col in required_cols):
    print("❌ Colonnes manquantes :", df.columns.tolist())
    exit()

df[required_cols] = df[required_cols].astype(float)

try:
    info = yf.Ticker(ticker).info
    company_name = info.get("longName", ticker)
except Exception:
    info = {}
    company_name = ticker

# ─────────────────────────────
# 📊 AFFICHAGE DU GRAPHIQUE
# ─────────────────────────────
if show_chart:
    mpf.plot(df, type="candle", style="charles", volume=True,
             title=f"{company_name} - {period}", figscale=1.5)
else:
    print("\n⏩ Graphique ignoré, passage direct à la musique...")

# ─────────────────────────────
# 🔄 NORMALISATION
# ─────────────────────────────
min_price, max_price = df["Close"].min(), df["Close"].max()
min_vol, max_vol = df["Volume"].min(), df["Volume"].max()
min_range, max_range = (df["High"] - df["Low"]).min(), (df["High"] - df["Low"]).max()

def normalize_price_to_midi(price):
    return int(40 + (price - min_price) / (max_price - min_price) * (80 - 40))

def normalize_volume_to_duration(volume):
    return int(240 + (volume - min_vol) / (max_vol - min_vol) * (960 - 240))

def normalize_range_to_velocity(price_range):
    return int(20 + (price_range - min_range) / (max_range - min_range) * (100 - 20))

# ─────────────────────────────
# 🎼 CRÉATION MIDI
# ─────────────────────────────
pitch_shift, tempo = get_company_timing_parameters(info)
instrument = assign_instrument_by_age(info)

start_date = df.index[0].strftime("%Y-%m-%d")
end_date = df.index[-1].strftime("%Y-%m-%d")
music_title = f"{company_name} ({start_date} to {end_date})"

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(MetaMessage('track_name', name=music_title, time=0))
track.insert(0, MetaMessage('set_tempo', tempo=tempo, time=0))
track.insert(0, Message('program_change', program=instrument, time=0))

for index, row in df.iterrows():
    note = normalize_price_to_midi(row["Close"]) + pitch_shift
    duration = normalize_volume_to_duration(row["Volume"])
    velocity = normalize_range_to_velocity(row["High"] - row["Low"])

    track.append(Message('note_on', note=note, velocity=velocity, time=0))
    track.append(Message('note_off', note=note, velocity=velocity, time=duration))

# ─────────────────────────────
# 💾 SAUVEGARDE SUR BUREAU
# ─────────────────────────────
desktop_onedrive = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
desktop_local = os.path.join(os.path.expanduser("~"), "Desktop")
desktop_path = desktop_onedrive if os.path.exists(desktop_onedrive) else desktop_local

safe_title = f"{company_name}_{start_date}_to_{end_date}.mid".replace(" ", "_").replace(",", "")
midi_path = os.path.join(desktop_path, safe_title)

mid.save(midi_path)
print(f"\n✅ Fichier MIDI enregistré sur le bureau :\n{midi_path}")
