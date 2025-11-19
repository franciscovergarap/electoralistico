# ANTES (error):
resultados = simular_segunda_vuelta_mejorado(candidato_R)
# ... luego intentaba usar transferencias que no existían

# AHORA (corregido):
resultados, transferencias = simular_segunda_vuelta_mejorado(candidato_R)
# transferencias está ahora disponible para el análisis
