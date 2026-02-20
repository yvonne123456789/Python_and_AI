import os
import requests
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 1. Get weather data (example structure)
# -----------------------------
def fetch_weather():
    """Fetch sample weather data from Open-Meteo."""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=48.85&longitude=2.35"
        "&daily=temperature_2m_max,temperature_2m_min"
        "&timezone=auto"
    )

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame({
        "date": data["daily"]["time"],
        "max_temp": data["daily"]["temperature_2m_max"],
        "min_temp": data["daily"]["temperature_2m_min"],
    })

    df["avg_temp"] = (df["max_temp"] + df["min_temp"]) / 2
    return df


# -----------------------------
# 2. Prepare output folder
# -----------------------------
def ensure_data_folder():
    if not os.path.exists("data"):
        os.makedirs("data")


# -----------------------------
# 3. Line chart
# -----------------------------
def plot_temperature_trends(df):
    plt.figure(figsize=(10, 6))

    plt.plot(df["date"], df["max_temp"], "r-o", label="Max")
    plt.plot(df["date"], df["min_temp"], "b-o", label="Min")
    plt.plot(df["date"], df["avg_temp"], "g--", label="Average")

    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.title("Paris Weather - Past Week")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("data/weather_trend.png")
    plt.close()


# -----------------------------
# 4. Histogram (NEW ⭐)
# -----------------------------
def plot_temperature_histogram(df):
    plt.figure(figsize=(8, 5))

    plt.hist(df["avg_temp"], bins=8)
    plt.xlabel("Average Temperature (°C)")
    plt.ylabel("Frequency")
    plt.title("Distribution of Average Temperatures")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig("data/temperature_histogram.png")
    plt.close()


# -----------------------------
# 5. Box plot (NEW ⭐)
# -----------------------------
def plot_temperature_boxplot(df):
    plt.figure(figsize=(6, 5))

    plt.boxplot(df["avg_temp"])
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature Spread (Box Plot)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig("data/temperature_boxplot.png")
    plt.close()


# -----------------------------
# 6. Main workflow
# -----------------------------
def main():
    print("Fetching weather data...")
    df = fetch_weather()

    ensure_data_folder()

    print("Generating charts...")
    plot_temperature_trends(df)
    plot_temperature_histogram(df)
    plot_temperature_boxplot(df)

    # Save CSV
    df.to_csv("data/paris_weather.csv", index=False)

    # Summary stats
    print(f"Average temperature: {df['avg_temp'].mean():.1f}°C")
    print(f"Max temperature: {df['max_temp'].max():.1f}°C")
    print(f"Min temperature: {df['min_temp'].min():.1f}°C")
    print("✅ Files saved in 'data' folder")


# -----------------------------
# Run script
# -----------------------------
if __name__ == "__main__":
    main()
