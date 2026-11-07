"""
Misma solución usando SQL sobre los CSV con DuckDB.
Instalar: pip install duckdb
"""
import duckdb

con = duckdb.connect()
# nullstr convierte "N/A" y vacíos a NULL al leer
con.sql("CREATE TABLE s AS SELECT * FROM read_csv('datos/sistema.csv', nullstr=['N/A', ''])")
con.sql("CREATE TABLE a AS SELECT * FROM read_csv('datos/aseguradora.csv', nullstr=['N/A', ''])")

print("=== NIVEL 1 ===")
con.sql("SELECT * FROM s WHERE estatus = 'Activa'").show()

print("=== NIVEL 2a: solo en sistema ===")
con.sql("SELECT id_poliza, nombre_asegurado FROM s WHERE id_poliza NOT IN (SELECT id_poliza FROM a)").show()

print("=== NIVEL 2b: solo en aseguradora ===")
con.sql("SELECT id_poliza, nombre_asegurado FROM a WHERE id_poliza NOT IN (SELECT id_poliza FROM s)").show()

print("=== NIVEL 3 ===")
d = con.sql("""SELECT s.id_poliza, s.prima AS prima_sistema, a.prima AS prima_aseguradora
               FROM s JOIN a USING (id_poliza)
               WHERE s.prima IS DISTINCT FROM a.prima
               ORDER BY s.id_poliza""").df()
print(d.to_string(index=False))
d.to_excel("diferencias_prima.xlsx", index=False)
