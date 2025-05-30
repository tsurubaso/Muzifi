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
    print("📜 Année de fondation : " + str(founded))
    pitch_shift = max(0, min(30, 30 - age // 3))      # jeunes = sons plus aigus
    tempo = int(400000 - min(300000, age * 2000))   # jeunes = tempo plus rapide
    return pitch_shift, tempo

def normalize_marketcap_to_velocity(marketcap, min_cap=1e9, max_cap=2e12):
    capped = max(min_cap, min(marketcap, max_cap))
    return int(40 + (capped - min_cap) / (max_cap - min_cap) * (100 - 40))

def assign_instrument(info):
    sector_to_instrument = {
        "Technology": 81,            # Lead 1 (square)
        "Healthcare": 48,            # Strings
        "Financial Services": 0,     # Piano
        "Energy": 17,                # Drawbar Organ
        "Consumer Cyclical": 24,     # Guitar
        "Industrials": 26,           # Steel Guitar
        "Utilities": 73,             # Flute
        "Real Estate": 46,           # Harp
        "Communication Services": 56,# Trumpet
        "Materials": 52              # Choir Aahs
    }
    sector = info.get("sector", "")
    if sector in sector_to_instrument:
        print(f"🏷️ Secteur détecté : {sector} → Instrument {sector_to_instrument[sector]}")
        return sector_to_instrument[sector]
    else:
        print(f"⚠️ Secteur inconnu : {sector} → Instrument par âge")
        return assign_instrument_by_age(info)

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
# FONCTION POUR ACCORD MAJEUR/MINEUR
# ─────────────────────────────
def build_chord(root_note, chord_type="major"):
    if chord_type == "major":
        return [root_note, root_note + 4, root_note + 7]
    else:
        return [root_note, root_note + 3, root_note + 7]

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
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    import textwrap

    # Récupération d'infos complémentaires
    name = info.get("longName", ticker.upper())
    sector = info.get("sector", "N/A")
    industry = info.get("industry", "N/A")
    country = info.get("country", "N/A")
    employees = info.get("fullTimeEmployees", "N/A")
    market_cap = info.get("marketCap")
    dividend_yield = info.get("dividendYield")
    website = info.get("website", "N/A")
    description = info.get("longBusinessSummary", "Aucune description disponible.")
    market_cap_str = f"{market_cap:,} USD" if market_cap else "N/A"
    dividend_str = f"{dividend_yield*100:.2f} %" if dividend_yield else "N/A"

    header_text = (
        f"{name}\n"
        f"Secteur : {sector}\n"
        f"Industrie : {industry}\n"
        f"Pays : {country}\n"
        f"Employés : {employees}\n"
        f"Capitalisation : {market_cap_str}\n"
        f"Dividende : {dividend_str}\n"
        f"Site Web : {website}\n\n"
    )
    wrapped_description = "\n".join(textwrap.wrap(description, width=150))
    combined_text = header_text + "\n" + wrapped_description

    # Affichage du graphique avec texte
    fig = plt.figure(figsize=(13, 14))
    gs = GridSpec(3, 1, height_ratios=[3, 1, 2])

    ax_candle = fig.add_subplot(gs[0])
    ax_volume = fig.add_subplot(gs[1], sharex=ax_candle)
    ax_text = fig.add_subplot(gs[2])

    mpf.plot(df, type='candle', style='yahoo', ax=ax_candle, volume=ax_volume)

    ax_text.text(
        0.02, 0.98, combined_text,
        fontsize=10, va="top", ha="left", wrap=True,
        linespacing=1.4, bbox=dict(boxstyle="round,pad=0.6", facecolor="#f0f0f0", edgecolor="black")
    )
    ax_text.axis("off")

    plt.tight_layout()
    plt.show()


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
instrument = assign_instrument(info)
market_cap = info.get("marketCap", 1e10)
velocity_boost = normalize_marketcap_to_velocity(market_cap)

start_date = df.index[0].strftime("%Y-%m-%d")
end_date = df.index[-1].strftime("%Y-%m-%d")
music_title = f"{company_name} ({start_date} to {end_date})"

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(MetaMessage('track_name', name=music_title, time=0))
track.insert(0, MetaMessage('set_tempo', tempo=tempo, time=0))
track.insert(0, Message('program_change', program=instrument, time=0))

previous_volume = None

for index, row in df.iterrows():
    note = normalize_price_to_midi(row["Close"]) + pitch_shift
    
    chord_type = "major"
    if previous_volume is not None:
        if row["Volume"] < previous_volume:
            chord_type = "minor"
    previous_volume = row["Volume"]
    
    chord_notes = build_chord(note, chord_type)
    
    duration = normalize_volume_to_duration(row["Volume"])
    velocity = min(127, normalize_range_to_velocity(row["High"] - row["Low"]) + velocity_boost // 4)
    
    # jouer toutes les notes de l'accord simultanément
    for n in chord_notes:
        track.append(Message('note_on', note=n, velocity=velocity, time=0))
    for n in chord_notes:
        track.append(Message('note_off', note=n, velocity=velocity, time=duration))

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
