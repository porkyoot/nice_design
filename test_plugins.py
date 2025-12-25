from nice_design.core.engine import ThemeEngine

engine = ThemeEngine()
palettes = engine.registry.list_palettes()
skins = engine.registry.list_skins()

print(f"Discovered Palettes: {palettes}")
print(f"Discovered Skins: {skins}")

if "solarized-dark-ext" in palettes:
    print("SUCCESS: solarized-dark-ext palette discovered!")
else:
    print("FAILURE: solarized-dark-ext palette NOT discovered!")

if "solarized-premium" in skins:
    print("SUCCESS: solarized-premium skin discovered!")
else:
    print("FAILURE: solarized-premium skin NOT discovered!")
