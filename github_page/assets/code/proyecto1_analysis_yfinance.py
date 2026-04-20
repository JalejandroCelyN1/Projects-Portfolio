import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def main():
    out_dir = os.path.dirname(__file__)
    tickers = ["GOOG", "MSFT"]
    start = "2019-01-01"
    end = "2021-01-01"

    results = {}

    for t in tickers:
        df = yf.download(t, start=start, end=end, progress=False)
        df.to_csv(os.path.join(out_dir, f"{t}_ohlcv.csv"))

        stats = df.describe().transpose()
        stats.to_csv(os.path.join(out_dir, f"{t}_stats.csv"))

        tk = yf.Ticker(t)
        divs = tk.dividends
        if not divs.empty:
            start_ts = pd.to_datetime(start)
            end_ts = pd.to_datetime(end)
            if getattr(divs.index, "tz", None) is not None:
                start_ts = start_ts.tz_localize(divs.index.tz)
                end_ts = end_ts.tz_localize(divs.index.tz)
            divs_in_range = divs[(divs.index >= start_ts) & (divs.index < end_ts)]
        else:
            divs_in_range = divs
        divs_in_range.to_csv(os.path.join(out_dir, f"{t}_dividends.csv"))

        mv = float(df["Volume"].mean()) if ("Volume" in df.columns and not df.empty) else float("nan")
        results[t] = {"df": df, "mean_volume": mv}

    msft_df = results["MSFT"]["df"]
    if not msft_df.empty and "Volume" in msft_df.columns:
        if getattr(msft_df.index, "tz", None) is not None:
            msft_df.index = msft_df.index.tz_convert(None)
        plt.figure(figsize=(12, 6))
        plt.plot(msft_df.index, msft_df["Volume"], color="tab:blue", linewidth=0.8)
        plt.title("MSFT - Daily Trading Volume (2019-01-01 to 2021-01-01)")
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, "MSFT_daily_volume.png"), dpi=150)
        plt.close()


if __name__ == "__main__":
    main()
