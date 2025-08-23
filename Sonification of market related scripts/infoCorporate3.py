import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import textwrap

def plot_candlestick_with_info(ticker, period):
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period=period)

    # Infos utiles
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

    # Figure à 3 zones : chandeliers, volume, texte
    fig = plt.figure(figsize=(13, 14))
    gs = GridSpec(3, 1, height_ratios=[3, 1, 2])

    ax_candle = fig.add_subplot(gs[0])
    ax_volume = fig.add_subplot(gs[1], sharex=ax_candle)
    ax_text = fig.add_subplot(gs[2])

    # Tracer chandeliers + volume avec les axes explicitement fournis
    mpf.plot(hist, type='candle', style='yahoo', ax=ax_candle, volume=ax_volume)

    # Texte en bas
    ax_text.text(
        0.02, 0.98, combined_text,
        fontsize=10, va="top", ha="left", wrap=True,
        linespacing=1.4, bbox=dict(boxstyle="round,pad=0.6", facecolor="#f0f0f0", edgecolor="black")
    )
    ax_text.axis("off")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    ticker = input("Entrez un ticker boursier (ex: AAPL, NVDA) : ").strip().upper()
    print("Périodes possibles : 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max")
    period = input("Entrez la période à afficher : ").strip()
    plot_candlestick_with_info(ticker, period)
