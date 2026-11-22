"""Nimbus Cement: pull 2040 climate projections for the nine plants.

Run on your own computer (needs Python 3 only, no packages):
    python3 pull_projections.py

Writes projections.json next to the script. Upload that file to the chat.
Source: Open-Meteo Climate API (CMIP6 HighResMIP models, daily, 1950-2050). Free, no key.
It computes, per plant and per model, for two windows (2006-2025 and 2031-2050):
  - mean days per year with daily max temperature >= 40 C
  - mean annual rainfall (mm)
  - mean annual maximum one-day rainfall (mm)
"""
import json
import time
import urllib.parse
import urllib.request

PLANTS = {
    "P01": (24.8887, 74.6269), "P02": (24.6005, 80.8322), "P03": (19.9615, 79.2961),
    "P04": (17.0575, 79.2671), "P05": (11.1401, 79.0786), "P06": (21.6566, 82.1606),
    "P07": (22.839, 69.7219), "P08": (20.3165, 86.6114), "P09": (23.5204, 87.3119),
}
MODELS = ["MRI_AGCM3_2_S", "EC_Earth3P_HR", "CMCC_CM2_VHR4"]
WINDOWS = {"2006-2025": (2006, 2025), "2031-2050": (2031, 2050)}


def fetch(lat, lon, model):
    q = "https://climate-api.open-meteo.com/v1/climate?" + urllib.parse.urlencode({
        "latitude": lat, "longitude": lon, "start_date": "2006-01-01", "end_date": "2050-12-31",
        "models": model, "daily": "temperature_2m_max,precipitation_sum"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(q, timeout=120) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001
            print("   retry", attempt + 1, repr(e)[:100])
            time.sleep(5 * (attempt + 1))
    return None


def col(daily, name):
    for k, v in daily.items():
        if k.startswith(name):
            return v
    return None


out = {}
for pid, (lat, lon) in PLANTS.items():
    out[pid] = {}
    for model in MODELS:
        print(pid, model)
        j = fetch(lat, lon, model)
        time.sleep(2)
        if not j or "daily" not in j:
            out[pid][model] = {"error": str(j)[:200]}
            continue
        t, p, days = col(j["daily"], "temperature_2m_max"), col(j["daily"], "precipitation_sum"), j["daily"]["time"]
        res = {}
        for wname, (y0, y1) in WINDOWS.items():
            hot, rain, rmax = {}, {}, {}
            for d, tv, pv in zip(days, t, p):
                y = int(d[:4])
                if y0 <= y <= y1:
                    hot[y] = hot.get(y, 0) + (1 if tv is not None and tv >= 40 else 0)
                    rain[y] = rain.get(y, 0) + (pv or 0)
                    rmax[y] = max(rmax.get(y, 0), pv or 0)
            n = len(hot) or 1
            res[wname] = {"days_ge40": round(sum(hot.values()) / n, 1),
                          "annual_mm": round(sum(rain.values()) / n),
                          "max_1day_mm": round(sum(rmax.values()) / n, 1), "years": len(hot)}
        out[pid][model] = res
with open("projections.json", "w") as f:
    json.dump(out, f, indent=1)
print("Done. Upload projections.json to the chat.")
