import os
import yfinance as yf
import matplotlib.pyplot as plt
import mido
from mido import MidiFile, MidiTrack, Message
import pandas as pd
import mplfinance as mpf
from datetime import datetime, timedelta

# Configurations
tickers = ['AAPL', 'MSFT', 'GOOGL']  # Entreprises à traiter
output_midi_file = os.path.expanduser("~/Desktop/multi_stock_output.mid")
start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')
bpm = 120
ticks_per_beat = 480

sector_instruments = {
    "Technology": 81,        # Lead 2 (sawtooth)
    "Healthcare": 52,        # Choir Aahs
    "Financial Services": 1, # Acoustic Grand Piano
    "Consumer Cyclical": 4,  # Electric Piano
    "Industrials": 19,       # Church Organ
    "Energy": 29,            # Overdriven Guitar
    "Utilities": 14,         # Xylophone
    "Communication Services": 72,  # Clarinet
    "Basic Materials": 12,   # Marimba
    "Real Estate": 48        # Strings Ensemble 1
}
default_instrument = 0  # Acoustic Grand Piano

def get_stock_data(ticker):
    data = yf.download(ticker, start=start_date, end=end_date)
    if data.empty:
        return None
    return data

def normalize_series(series, min_val=40, max_val=80):
    normalized = (series - series.min()) / (series.max() - series.min())
    return (normalized * (max_val - min_val) + min_val).astype(int)

def get_company_sector(ticker):
    info = yf.Ticker(ticker).info
    return info.get("sector", "Unknown")

def get_company_market_cap(ticker):
    info = yf.Ticker(ticker).info
    return info.get("marketCap", 1_000_000_000)  # défaut si inconnue

def get_sector_instrument(sector):
    return sector_instruments.get(sector, default_instrument)

def create_midi_track(ticker, df, channel, instrument, velocity):
    pitch_series = normalize_series(df["Close"], min_val=60, max_val=80)
    duration_series = normalize_series(df["High"] - df["Low"], min_val=60, max_val=240)

    track = MidiTrack()
    track.append(mido.Message('program_change', program=instrument, channel=channel, time=0))

    time_per_note = int(ticks_per_beat * 60 / bpm)

    for pitch, duration in zip(pitch_series, duration_series):
        track.append(Message('note_on', note=pitch, velocity=velocity, channel=channel, time=0))
        track.append(Message('note_off', note=pitch, velocity=velocity, channel=channel, time=duration))
    
    return track

def plot_candlestick_chart(df, ticker):
    mpf.plot(df, type='candle', style='yahoo', title=f"Candlestick Chart for {ticker}",
             mav=(3, 6, 9), volume=True, savefig=os.path.expanduser(f"~/Desktop/{ticker}_chart.png"))

def generate_midi_for_tickers(tickers):
    mid = MidiFile(ticks_per_beat=ticks_per_beat)

    for i, ticker in enumerate(tickers):
        df = get_stock_data(ticker)
        if df is None:
            print(f"Erreur : données introuvables pour {ticker}")
            continue

        if i == 0:
            plot_candlestick_chart(df, ticker)  # Un seul graphique pour alléger

        sector = get_company_sector(ticker)
        instrument = get_sector_instrument(sector)
        market_cap = get_company_market_cap(ticker)
        velocity = int(min(127, max(30, market_cap / 10**9)))  # Capitalisation en milliards

        print(f"{ticker}: sector={sector}, instrument={instrument}, velocity={velocity}")

        track = create_midi_track(ticker, df, channel=i % 16, instrument=instrument, velocity=velocity)
        mid.tracks.append(track)

    mid.save(output_midi_file)
    print(f"\n✅ Fichier MIDI enregistré sur le bureau : {output_midi_file}")

generate_midi_for_tickers(tickers)
