"""
Conciliación mensual de pólizas: sistema interno vs. aseguradora.
Uso: python conciliacion.py
"""
import pandas as pd

RUTA_SISTEMA = "datos/sistema.csv"
RUTA_ASEGURADORA = "datos/aseguradora.csv"
SALIDA = "diferencias_prima.xlsx"

# Cargar datos (utf-8-sig quita el BOM invisible al inicio de los CSV)
s = pd.read_csv(RUTA_SISTEMA, encoding="utf-8-sig")
a = pd.read_csv(RUTA_ASEGURADORA, encoding="utf-8-sig")

# "N/A" o vacío -> NaN, para no inventar montos
s["prima"] = pd.to_numeric(s["prima"], errors="coerce")
a["prima"] = pd.to_numeric(a["prima"], errors="coerce")

# Nivel 1: pólizas activas del sistema
print("=== NIVEL 1: Pólizas activas ===")
print(s[s["estatus"] == "Activa"].to_string(index=False))

# Nivel 2: una sola unión sirve para comparar ambas fuentes
m = s.merge(a, on="id_poliza", how="outer",
            suffixes=("_sistema", "_aseguradora"), indicator=True)

print("\n=== NIVEL 2a: En sistema pero NO en aseguradora ===")
print(m[m["_merge"] == "left_only"][["id_poliza", "nombre_asegurado_sistema"]].to_string(index=False))

print("\n=== NIVEL 2b: En aseguradora pero NO en sistema ===")
print(m[m["_merge"] == "right_only"][["id_poliza", "nombre_asegurado_aseguradora"]].to_string(index=False))

# Nivel 3: primas diferentes entre pólizas que existen en ambas fuentes
# fillna(0) solo para comparar: si falta la prima en un lado, cuenta como diferencia
d = m[(m["_merge"] == "both") &
      (m["prima_sistema"].fillna(0) != m["prima_aseguradora"].fillna(0))]
d = d[["id_poliza", "prima_sistema", "prima_aseguradora"]]

print("\n=== NIVEL 3: Diferencias de prima ===")
print(d.to_string(index=False))

d.to_excel(SALIDA, index=False)
print(f"\nArchivo exportado: {SALIDA}")
