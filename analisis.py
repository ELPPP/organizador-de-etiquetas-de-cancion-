import pandas as pd

# === CONFIGURACIÓN ===
file_path = "Canciones UWU.xlsx"  # si el script está junto al Excel

# Leer hoja
df = pd.read_excel(file_path, sheet_name="Sheet")
titulos = df["Titulo"].dropna().astype(str)

# Contar guiones con espacios alrededor (ej: "Artista - Canción")
guion_con_espacios = titulos.str.contains(r"\s-\s", regex=True).sum()

# Contar guiones pegados entre letras/palabras (ej: "back-in-black")
guion_sin_espacios = titulos.str.contains(r"\w-\w", regex=True).sum()

# Total de títulos con algún guion
total_con_guion = titulos.str.contains(r"-", regex=True).sum()

print("📊 Resultados del análisis de guiones en títulos:")
print(f"- Guiones con espacios (' - '): {guion_con_espacios}")
print(f"- Guiones pegados ('palabra-palabra'): {guion_sin_espacios}")
print(f"- Total de títulos que contienen guiones: {total_con_guion}")

# === Mostrar ejemplos de los guiones pegados ===
titulos_guion_pegado = titulos[titulos.str.contains(r"\w-\w", regex=True)]

print("\n📋 Títulos con guiones pegados (ejemplo de sustitución de espacios):\n")
for t in titulos_guion_pegado:
    print(t)
