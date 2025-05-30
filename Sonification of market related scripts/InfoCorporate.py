import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import textwrap

def plot_candlestick_with_info(ticker, period):
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period=period)

    name = info.get("longName", ticker.upper())
    sector = info.get("sector", "N/A")
    market_cap = info.get("marketCap")
    description = info.get("longBusinessSummary", "Aucune description disponible.")
    market_cap_str = f"{market_cap:,} USD" if market_cap else "N/A"

    header_text = (
    f"{name}\n"  # Just the name on its own line
    f"Secteur: {sector}\n"  # Sector on a new line
    f"Capitalisation: {market_cap_str}\n\n"  # Market cap on another line
)



    # Préparer la figure
    fig, (ax_candle, ax_text) = plt.subplots(2, 1, figsize=(13, 10),
                                             gridspec_kw={'height_ratios': [3.5, 2.5]})

    # Tracer les chandeliers
    ax_candle.set_axis_off()
    mpf.plot(hist, type='candle', ax=ax_candle, volume=False, style='yahoo')

    # Bordure autour des chandeliers
    ax_candle.add_patch(Rectangle(
        (0, 0), 1, 1,
        transform=ax_candle.transAxes,
        fill=False, linewidth=1.2, edgecolor='black'
    ))
    

# Create the header_text independently
    header_text = (
    f"{name}\n"
    f"Secteur: {sector}\n"
    f"Capitalisation: {market_cap_str}\n\n"
)
    
    
# Use only the description for the text box
    wrapped_description = "\n".join(textwrap.wrap(description, width=150))
    # Combine header_text and wrapped_description
    combined_text = header_text + "\n" + wrapped_description

# Add the combined text to the text box
    textbox = ax_text.text(
    0.02, 0.95, combined_text,  # Insert both header and description
    fontsize=10, va="top", ha="left", wrap=True,
    linespacing=1.4, bbox=dict(boxstyle="round,pad=0.6", facecolor="#f0f0f0", edgecolor="black")
)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    ticker = input("Entrez un ticker boursier (ex: AAPL, NVDA) : ").strip().upper()
    print("Périodes possibles : 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max")
    period = input("Entrez la période à afficher : ").strip()
    plot_candlestick_with_info(ticker, period)
