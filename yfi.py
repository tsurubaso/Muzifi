import yfinance as yf
import mplfinance as mpf
import pandas as pd

# Téléchargement des données
print("Téléchargement des données...")
df = yf.download("MSFT", period="5ycls")

# Corrige les colonnes multi-index
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

if df.empty:
    print("❌ Erreur : aucune donnée reçue pour ce ticker.")
    exit()

# Affiche les 5 premières lignes et les types
print("\n✅ Aperçu brut des données:")
print(df.head())
print("\n✅ Types de colonnes:")
print(df.dtypes)

# Nettoyage
df.dropna(inplace=True)

# Colonnes obligatoires
required_cols = ["Open", "High", "Low", "Close"]

# Vérifie si les colonnes existent
if not all(col in df.columns for col in required_cols):
    print("❌ Erreur : colonnes manquantes.")
    print("Colonnes présentes :", df.columns.tolist())
    exit()

# Tentative de conversion en float
try:
    df[required_cols] = df[required_cols].astype(float)
except Exception as e:
    print("❌ Erreur lors de la conversion des colonnes en float:")
    print(e)
    print("Valeurs problématiques :")
    print(df[required_cols][~df[required_cols].applymap(lambda x: isinstance(x, (int, float)))])
    exit()

# Affichage du graphique
print("\n✅ Données prêtes, affichage du graphique...")
mpf.plot(df, type="candle", style="charles", volume=True, title="AAPL - 1 an")
