import yfinance as yf
import pandas as pd
import os
from datetime import datetime
from mido import MidiFile, MidiTrack, Message, MetaMessage
import re

def extract_founding_year(description, default_year=1985):
    match = re.search(r"(founded|incorporated) in (\d{4})", description.lower())
    if match:
        return int(match.group(2))
    return default_year

def get_company_timing_parameters(info):
    current_year = datetime.now().year
    founded = extract_founding_year(info.get("longBusinessSummary", ""), 1985)
    age = current_year - founded
    pitch_shift = max(0, min(30, 30 - age // 3))
    tempo = int(700000 - min(500000, age * 5000))
    start_delay = max(0, (100 - age) * 10)
    return pitch_shift, tempo, start_delay

def assign_instrument_by_age(info):
    current_year = datetime.now().year
    founded = extract_founding_year(info.get("longBusinessSummary", ""), 1985)
    age = current_year - founded

    instrument_by_age = [
        (100, [32, 33, 34]),  # Basses
        (60, [24, 25, 26]),   # Guitares
        (30, [0, 1, 2]),      # Pianos
        (15, [40, 41, 42]),   # Violons
        (0, [72, 73, 74])     # Flûtes
    ]

    for limit, instruments in reversed(instrument_by_age):
        if age >= limit:
            return instruments[age % len(instruments)]
    return 0

companies = input("📊 Entrez une liste de codes (ex: AAPL, MSFT, NVDA) : ").upper().split(',')
companies = [c.strip() for c in companies[:20]]
period = input("⏱️ Période (ex: 1mo, 3mo, 6mo, 1y) : ").lower()

output_folder = os.path.join(os.getcwd(), "midis_generated")
os.makedirs(output_folder, exist_ok=True)

midi_files = []

for ticker in companies:
    print(f"\n📥 Téléchargement des données pour {ticker} sur {period}...")
    df = yf.download(ticker, period=period)

    if df.empty or not all(col in df.columns for col in ["Open", "High", "Low", "Close", "Volume"]):
        print(f"❌ Aucune donnée valable pour {ticker}.")
        continue

    try:
        info = yf.Ticker(ticker).info
    except Exception:
        info = {}

    pitch_shift, tempo, start_delay = get_company_timing_parameters(info)
    instrument = assign_instrument_by_age(info)

    min_price, max_price = df["Close"].min(), df["Close"].max()
    min_vol, max_vol = df["Volume"].min(), df["Volume"].max()
    price_range = df["High"] - df["Low"]
    min_range, max_range = price_range.min(), price_range.max()

    volatility = price_range.std().item()
    interval = 4 if volatility < 2 else 5 if volatility < 5 else 7

    print(f"📊 Volatility for {ticker}: {volatility:.2f} → Interval: {interval} semitones")

    def normalize_price_to_midi(price):
        return int(40 + (price - min_price).iloc[0] / (max_price - min_price).iloc[0] * (80 - 40))

    def normalize_volume_to_duration(volume):
        return int((240 + (volume - min_vol) / (max_vol - min_vol) * (960 - 240)).iloc[0])
 
    def normalize_range_to_velocity(price_range):
        return int(20 + (price_range - min_range).iloc[0] / (max_range - min_range).iloc[0] * (100 - 20))



    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(MetaMessage('track_name', name=ticker, time=0))
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
    track.append(Message('program_change', program=instrument, time=0))

    current_time = start_delay

    for _, row in df.iterrows():
        note = normalize_price_to_midi(row["Close"]) + pitch_shift
        duration = normalize_volume_to_duration(row["Volume"])
        velocity = normalize_range_to_velocity(row["High"] - row["Low"])
        harmony_note = min(note + interval, 127)

        track.append(Message('note_on', note=note, velocity=velocity, time=current_time))
        track.append(Message('note_on', note=harmony_note, velocity=max(velocity - 10, 0), time=0))
        track.append(Message('note_off', note=note, velocity=velocity, time=duration))
        track.append(Message('note_off', note=harmony_note, velocity=max(velocity - 10, 0), time=0))

        current_time = 0

    midi_path = os.path.join(output_folder, f"{ticker}.mid")
    mid.save(midi_path)
    midi_files.append((midi_path, instrument))
    print(f"✅ Fichier MIDI créé : {midi_path}")

# ─────────────────────────────
# 🔗 Fusion des fichiers MIDI
# ─────────────────────────────

combined = MidiFile()
combined.ticks_per_beat = 480

for path, instrument in midi_files:
    midi = MidiFile(path)
    new_track = MidiTrack()
    combined.tracks.append(new_track)

    new_track.append(MetaMessage('track_name', name=os.path.basename(path).replace(".mid", ""), time=0))
    new_track.append(Message('program_change', program=instrument, time=0))

    for msg in midi.tracks[0]:
        if not msg.is_meta and msg.type != 'program_change':
            new_track.append(msg.copy(time=msg.time))

output_path = os.path.join(output_folder, "fusion_midis_output.mid")
combined.save(output_path)
print(f"\n✅ Fichier combiné enregistré : {output_path}")
