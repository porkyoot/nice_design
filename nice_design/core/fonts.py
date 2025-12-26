import os
from pathlib import Path
from typing import List, Dict
from nicegui import ui, app

# A curated list of popular Google Fonts. 
# In a real-world app, this could be fetched from Google Fonts API or a static JSON.
GOOGLE_FONTS = [
    "Inter", "Roboto", "Open Sans", "Lato", "Montserrat", "Oswald", "Raleway", "PT Sans", 
    "Ubuntu", "Lora", "Merriweather", "Playfair Display", "Poppins", "Noto Sans", 
    "Source Sans Pro", "Source Serif Pro", "Source Code Pro", "Inconsolata", "Fira Sans",
    "Quicksand", "Josefin Sans", "Nunito", "Dancing Script", "Pacifico", "Amatic SC",
    "Muli", "Arvo", "Exo 2", "Crimson Text", "Alegreya", "Cabin", "Oxygen", "Anton",
    "Zilla Slab", "Karla", "Spectral", "Teko", "Kanit", "Hind", "Rajdhani", "Barlow",
    "Mukta", "Titillium Web", "Work Sans", "Libre Franklin", "Heebo", "Overpass",
    "Manrope", "Outfit", "Space Grotesk", "Sora", "Plus Jakarta Sans", "Be Vietnam Pro",
    "Public Sans", "IBM Plex Sans", "IBM Plex Serif", "IBM Plex Mono", "Syne", "Urbanist",
    "Schibsted Grotesk", "Fraunces", "Young Serif", "Bricolage Grotesk", "Instrument Sans",
    "Figtree", "Geologica", "Reddit Sans", "Afacad", "Onest", "Golos Text", "Uncut Sans", "Recursive",
]

# Adding more to make it "all" feel real
MORE_GOOGLE_FONTS = [
    "Abril Fatface", "Alfa Slab One", "Alice", "Almarai", "Amaranth", "Architects Daughter",
    "Archivo", "Archivo Black", "Archivo Narrow", "Asap", "Asap Condensed", "Assistant",
    "Bangers", "Bebas Neue", "Bitter", "Bree Serif", "Cairo", "Catamaran", "Caveat",
    "Chakra Petch", "Chivo", "Comfortaa", "Cookie", "Courgette", "Crete Round", "Dosis",
    "EB Garamond", "Encode Sans", "Exo", "Fira Code", "Fredoka One", "Gelasio", "Great Vibes",
    "Hammersmith One", "Hind Madurai", "Hind Siliguri", "Inknut Antiqua", "Indie Flower",
    "Jost", "Kalam", "Kaushan Script", "Kumbh Sans", "League Spartan", "Libre Baskerville",
    "Lobster", "Lobster Two", "Mako", "Mandali", "Marck Script", "Maven Pro", "Metrophobic",
    "Michroma", "Molecule", "Nanum Gothic", "News Cycle", "Niconne", "Noto Serif", "Old Standard TT",
    "Orbitron", "Overlock", "Pangolin", "Passion One", "Patua One", "Permanent Marker",
    "Philosopher", "Play", "Playball", "Prata", "Prompt", "PT Sans Narrow", "PT Serif",
    "Questrial", "Quattrocento", "Quattrocento Sans", "Ranchers", "Righteous", "Rokkitt",
    "Rubik", "Ruda", "Sacramento", "Sanchez", "Shadows Into Light", "Sigmar One", "Signika",
    "Sintony", "Slabo 27px", "Special Elite", "Squada One", "Staatliches", "Tangerine",
    "Tenor Sans", "Tinos", "Varela Round", "Vidaloka", "Volkhov", "Vollkorn", "Yellowtail", "Yeseva One"
]

ALL_GOOGLE_FONTS = sorted(list(set(GOOGLE_FONTS + MORE_GOOGLE_FONTS)))

class FontManager:
    _loaded_fonts = set()

    @staticmethod
    def load_font(font_name: str):
        """Injects the Google Font CSS into the head if it's a Google Font."""
        if font_name in ALL_GOOGLE_FONTS and font_name not in FontManager._loaded_fonts:
            # Prepare URL (replace spaces with +)
            url_name = font_name.replace(" ", "+")
            url = f"https://fonts.googleapis.com/css2?family={url_name}:wght@100;200;300;400;500;600;700;800;900&display=swap"
            font_id = f"font-{url_name.lower().replace('+', '-')}"
            
            # Using run_javascript to ensure it's injected even after page load
            ui.run_javascript(f'''
                if (!document.getElementById("{font_id}")) {{
                    const link = document.createElement("link");
                    link.id = "{font_id}";
                    link.href = "{url}";
                    link.rel = "stylesheet";
                    document.head.appendChild(link);
                    console.log("Loaded Google Font: {font_name}");
                }}
            ''')
            FontManager._loaded_fonts.add(font_name)
            
    @staticmethod
    def get_font_options(local_fonts: List[str]):
        """Returns a combined list of local and google fonts for the select component."""
        opts = {}
        
        # Local Fonts (Priority)
        for f in local_fonts:
            opts[f] = {'label': f, 'value': f, 'font': f, 'icon': 'mdi-folder-outline', 'color': 'primary'}
            
        # Google Fonts
        for f in ALL_GOOGLE_FONTS:
            if f not in opts:
                opts[f] = {'label': f, 'value': f, 'font': f, 'icon': 'mdi-google', 'color': 'accent'}
                
        return opts
