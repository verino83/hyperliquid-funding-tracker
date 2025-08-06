import requests
import pandas as pd

# Obtener los datos del mercado de Hyperliquid
url = "https://api.hyperliquid.xyz/info"
response = requests.get(url)
data = response.json()

# Separar tokens en spot y perp
spot_assets = set()
perp_assets = {}

for market in data["universe"]:
    name = market["name"]
    if market["type"] == "spot":
        spot_assets.add(name)
    elif market["type"] == "perp":
        perp_assets[name] = {
            "fundingRate": market.get("fundingRate", 0),
            "price": market.get("markPrice", 0)
        }

# Filtrar tokens que están tanto en spot como en perp
tokens = []
for token in perp_assets:
    if token in spot_assets:
        fr = perp_assets[token]["fundingRate"]
        price = perp_assets[token]["price"]
        apr_1d = fr * 3 * 100
        apr_1m = fr * 3 * 30 * 100
        apr_1y = fr * 3 * 365 * 100

        tokens.append({
            "Token": token,
            "Funding Rate (8h)": f"{fr:.5f}",
            "Price": f"${price:.4f}",
            "APR (1d)": f"{apr_1d:.2f}%",
            "APR (1m)": f"{apr_1m:.2f}%",
            "APR (1y)": f"{apr_1y:.2f}%"
        })

# Crear tabla y mostrar
df = pd.DataFrame(tokens)
df = df.sort_values(by="APR (1y)", ascending=False)

print("\nTokens with Spot + Perp on Hyperliquid:\n")
print(df.to_string(index=False))

