import yfinance as yf
import pandas as pd
import os
from datetime import datetime
from mido import MidiFile, MidiTrack, Message, MetaMessage

# ─────────────────────────────
# 🎯 CHANGEMENT EN FONCTION DES ENTREPRISES
# ─────────────────────────────

def get_company_timing_parameters(info):
    current_year = datetime.now().year
    founded = info.get("founded", 1985)
    # Add a print statement here to see the founded year
    print(f"Company founded year: {founded}")
    
    age = current_year - founded

    # Map age to musical parameters
    pitch_shift = max(0, min(30, 30 - age // 3))      # jeunes = sons plus aigus
    tempo = int(700000 - min(500000, age * 5000))     # jeunes = tempo plus rapide
    start_delay = max(0, (100 - age) * 10)            # vieux = jouent en premier

    return pitch_shift, tempo, start_delay

def assign_instrument_by_age(info):
    current_year = datetime.now().year
    founded = info.get("founded", 1985)
    age = current_year - founded

    instrument_by_age = [
        (100, [32, 33, 34]),  # Basses
        (60, [24, 25, 26]),   # Guitares
        (30, [0, 1, 2]),      # Pianos
        (15, [40, 41, 42]),   # Violons
        (0, [72, 73, 74])     # Flûtes
    ]

    for limit, instruments in instrument_by_age:
        if age >= limit:
            return instruments[age % len(instruments)]  # Choix un peu varié dans la gamme

    return 0  # Piano par défaut




# ─────────────────────────────
# 🎯 LISTE DES ENTREPRISES
# ─────────────────────────────
companies = input("📊 Entrez une liste de codes (ex: AAPL, MSFT, NVDA) : ").upper().split(',')
companies = [c.strip() for c in companies[:20]]  # Limite à 20 entreprises

period = input("⏱️ Période (ex: 1mo, 3mo, 6mo, 1y) : ").lower()

# Dossier de sortie
output_folder = os.path.join(os.getcwd(), "midis_generated")
os.makedirs(output_folder, exist_ok=True)

# ─────────────────────────────
# 📈 RÉCUPÉRATION DES DONNÉES ET CRÉATION MIDI
# ─────────────────────────────
midi_files = []
for ticker in companies:
    print(f"\n📥 Téléchargement des données pour {ticker} sur {period}...")
    
    df = yf.download(ticker, period=period)

    try:
        info = yf.Ticker(ticker).info
    except Exception:
        info = {}

    pitch_shift, tempo, start_delay = get_company_timing_parameters(info)
    instrument = assign_instrument_by_age(info)



    if df.empty or not all(col in df.columns for col in ["Open", "High", "Low", "Close", "Volume"]):
        print(f"❌ Aucune donnée valable pour {ticker}.")
        continue
    
    min_price, max_price = df["Close"].min(), df["Close"].max()
    min_vol, max_vol = df["Volume"].min(), df["Volume"].max()
    min_range, max_range = (df["High"] - df["Low"]).min(), (df["High"] - df["Low"]).max()

    def normalize_price_to_midi(price):
        return int(40 + (price - min_price) / (max_price - min_price) * (80 - 40))

    def normalize_volume_to_duration(volume):
        return int(240 + (volume - min_vol) / (max_vol - min_vol) * (960 - 240))  # ticks MIDI

    def normalize_range_to_velocity(price_range):
        return int(20 + (price_range - min_range).iloc[0] / (max_range - min_range).iloc[0] * (100 - 20))


    # Création du fichier MIDI
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(MetaMessage('track_name', name=ticker, time=0))
    track.insert(0, MetaMessage('set_tempo', tempo=tempo, time=0))

    # Décalage initial pour le start delay
    current_time = start_delay

    for index, row in df.iterrows():
        note = normalize_price_to_midi(row["Close"]) + pitch_shift
        duration = normalize_volume_to_duration(row["Volume"])
        velocity = normalize_range_to_velocity(row["High"] - row["Low"])

        track.append(Message('note_on', note=note, velocity=velocity, time=current_time))
        track.append(Message('note_off', note=note, velocity=velocity, time=duration))
        current_time = 0  # Après la première note, on repasse à time=0 pour les suivantes
    mid.tracks.append(track)

    track.append(MetaMessage('track_name', name=ticker, time=0))
    track.insert(0, MetaMessage('set_tempo', tempo=500000, time=0))

    for index, row in df.iterrows():
        note = normalize_price_to_midi(row["Close"])
        duration = normalize_volume_to_duration(row["Volume"])
        velocity = normalize_range_to_velocity(row["High"] - row["Low"])

        track.append(Message('note_on', note=note, velocity=velocity, time=0))
        track.append(Message('note_off', note=note, velocity=velocity, time=duration))

    midi_path = os.path.join(output_folder, f"{ticker}.mid")
    mid.save(midi_path)
    midi_files.append(midi_path)
    print(f"✅ Fichier MIDI créé : {midi_path}")

# ─────────────────────────────
# 🎼 FUSION DES FICHIERS MIDI
# ─────────────────────────────
combined = MidiFile()
combined.ticks_per_beat = 480  

instrument_list = [0, 24, 32, 40, 48, 56, 64, 73, 80, 88]  # Variété d'instruments

for i, path in enumerate(midi_files):
    midi = MidiFile(path)
    track = MidiTrack()
    combined.tracks.append(track)

    track.append(MetaMessage('track_name', name=os.path.basename(path).replace(".mid", ""), time=0))
    instrument = instrument_list[i % len(instrument_list)]
    
    has_program_change = False  
    for msg in midi.tracks[0]:
        if msg.type == 'program_change':
            has_program_change = True
        if not msg.is_meta:
            track.append(msg.copy(time=msg.time))

    if not has_program_change:
        track.insert(0, Message('program_change', program=instrument, time=0))

output_path = os.path.join(output_folder, "fusion_midis_output.mid")
combined.save(output_path)
print(f"\n✅ Fichier combiné enregistré : {output_path}")
