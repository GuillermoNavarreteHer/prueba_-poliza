# Conciliación de pólizas: sistema vs. aseguradora

Ejercicio de renovaciones. Compara las pólizas registradas en el sistema interno con las reportadas por la aseguradora.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TU_USUARIO/conciliacion-polizas/blob/main/conciliacion.ipynb)

## Qué resuelve

| Nivel | Tarea |
|---|---|
| 1 | Muestra las pólizas del sistema con estatus "Activa" |
| 2 | Identifica pólizas que están solo en el sistema y solo en la aseguradora |
| 3 | Encuentra primas diferentes y exporta `diferencias_prima.xlsx` |

## Estructura

```
conciliacion-polizas/
├── conciliacion.ipynb      # Cuaderno para Google Colab (paso a paso)
├── conciliacion.py         # Misma solución como script
├── alternativa_duckdb.py   # Misma solución escrita en SQL
├── datos/
│   ├── sistema.csv
│   └── aseguradora.csv
├── requirements.txt
└── README.md
```

## Cómo usarlo

**En Google Colab:** da clic en el botón "Abrir en Colab" de arriba y ejecuta las celdas en orden.

**En tu computadora:**

```bash
pip install -r requirements.txt
python conciliacion.py
```

## Decisiones de limpieza

- Las primas con "N/A" o vacías se convierten a nulo (no a 0), para no inventar montos.
- Si una póliza tiene prima en una fuente y nula en la otra, se reporta como diferencia, porque requiere revisión.
- Los CSV traen un BOM al inicio; se leen con `encoding="utf-8-sig"`.

## Resultados esperados

- **Nivel 1:** 14 pólizas activas (POL-015 está vencida).
- **Nivel 2a:** POL-012, POL-015. **Nivel 2b:** POL-099.
- **Nivel 3:** POL-003, POL-007, POL-009.
