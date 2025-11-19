import streamlit as st
import pandas as pd
import base64

# --- 1. DATOS ESTRUCTURALES (FIJOS) ---
# Basado en nuestro análisis de los pactos municipales 2024 (~11.22M votos válidos)
BLOQUE_L_BASE = 3_670_000  # "Izquierda Unida" (Contigo Chile Mejor + afines)
BLOQUE_R_BASE = 3_970_000  # "Derecha Dura/Soft" (Chile Vamos + Rep + PSC + afines)
BLOQUE_C_BASE = 3_580_000  # "Bisagra" (PDG + Independientes puros + Centro)

# --- 2. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="Simulador Balotaje 2025")
st.title("🗳️ ELECTORALÍSTICO: Simulador de Escenarios de Segunda Vuelta")
st.markdown("Basado en la estructura de bloques de la Elección Municipal 2024 para Alcaldes (con voto obligatorio).")

# --- 3. PANEL LATERAL (SIDEBAR) CON PARÁMETROS FIJOS ---
st.sidebar.header("Modelo Estructural (Municipal 2024 para Alcaldes)")
st.sidebar.markdown(f"""
Este simulador usa como ancla los resultados de la elección municipal 2024 por pactos:

* **Bloque Izquierda (Base Jara):** `{BLOQUE_L_BASE:,.0f}` votos
* **Bloque Derecha (Base Opositora):** `{BLOQUE_R_BASE:,.0f}` votos
* **Bloque Bisagra (Centro/Indep.):** `{BLOQUE_C_BASE:,.0f}` votos

**Hipótesis:** La elección se gana movilizando la base propia y capturando la mayor parte del bloque Bisagra.

**Supuestos Metodológicos a Considerar**: El razonamiento descansa en articular tres piezas: encuestas recientes bajo voto obligatorio, resultados municipales 2024 como distribución empírica de preferencias y un modelo explícito de bloques ideológicos y transferencias.

**Primero**, las encuestas CEP, UDD, Cadem, AtlasIntel y La Cosa Nostra convergen en algo básico: Jeannette Jara lidera o co-lidera la primera vuelta, mientras la derecha aparece fragmentada entre Kast, Matthei y Kaiser, con diferencias en magnitud pero no en la estructura del campo. Estas mediciones, pese a sesgos de muestra online o telefónica, tienden a ordenar la competencia más que a fijar porcentajes exactos. La propia CEP subraya la centralidad del nuevo electorado obligado, más volátil, menos ideologizado y difícil de capturar bajo marcos muestrales clásicos. 

**Segundo**, reconocemos que desde 2022 el voto obligatorio reconfigura el electorado: amplía masivamente la base, incrementa nulos/blancos y debilita la capacidad predictiva de encuestas diseñadas para un votante más politizado. Por ello se introduce la elección municipal 2024 de alcaldes como ancla estructural: participación alta, padrón obligatorio y resultados verificables Servel. Los análisis de DecideChile, LyD y Nuso coinciden en tres rasgos: buen desempeño de Chile Vamos y aliados, avance significativo republicano en representación, y resistencia relativa del oficialismo; no hay, sin embargo, hegemonía incontestable de la derecha ni avalancha ultra. 

**Tercero**, sobre esa base se construyen bloques ideológicos usando tus criterios. Reagregando votos de municipales 2024, el bloque “Izquierda unida” (desde DC hasta la izquierda radical) ronda un tercio del electorado válido; la “Derecha dura” (RN–UDI–Republicanos–PSC y afines) la supera levemente; la “Derecha soft” (centro pro-orden hasta la derecha extrema) se sitúa algo por encima; la “Derecha ultra” (núcleo republicano-socialcristiano y fracciones más radicales de RN/Evópoli) se mantiene como minoría intensa. Los datos por partido muestran un empate casi perfecto entre izquierda orgánica ampliada y derecha soft orgánica, evidenciando que la ventaja real no reside en los partidos sino en la enorme franja independiente/bisagra revelada por el voto obligatorio. Estos cálculos se apoyan en los cómputos oficiales y tipologías de pactos de Servel y DecideChile, aunque la asignación fina a bloques es necesariamente analítica, no jurídica. 

A partir de ello, los escenarios de segunda vuelta se modelan no desde encuestas hipotéticas, sino desde la combinación “bloques municipales + coeficientes de transferencia” del centro hacia cada candidato: con Matthei, la derecha maximiza la captura del bloque blando y se configura una ventaja estructural frente a Jara; con Kast, la capacidad de seducir centro cae y emerge un escenario abierto donde el “cordón sanitario” anti-extrema derecha puede tornar competitiva a Jara; con Kaiser, la dependencia del voto ultra estrecha aún más el campo, volviendo plausible una mayoría para Jara. Así, tu hipótesis queda afinada: las encuestas son útiles para ordenar la primera vuelta, pero su capacidad para anticipar la segunda es limitada si no se recalibran con la estructura real del electorado bajo voto obligatorio. El insumo robusto hoy no es el porcentaje puntual de cada sondeo, sino la cartografía de bloques revelada en 2024 y su interacción con la identidad específica del candidato de derechas que logre llegar al balotaje.

**NOTA: Programa asistido por Gemini 2.5 Pro**
Fuente de datos: SERVEL, Atlas Intel, La Cosa Nostra, Encuesta CEP.

""")

# --- 4. SELECCIÓN DE ESCENARIO (CANDIDATO) ---
st.header("1. Defina el Escenario de Balotaje")

candidato_L = "Jeannete Jara"
candidato_R = st.selectbox(
    "Seleccione el/la candidato/a de Derecha:",
    ["Evelyn Matthei", "José Antonio Kast", "Johannes Kaiser"]
)

# --- 5. LÓGICA DE PRESETS (Según tu hipótesis) ---
if candidato_R == "Evelyn Matthei":
    default_transfer_R = 60
elif candidato_R == "José Antonio Kast":
    default_transfer_R = 30
else:  # Johannes Kaiser
    default_transfer_R = 15

# --- 6. CONTROLES INTERACTIVOS (SLIDERS) ---
st.header("2. Ajuste Parámetros de Simulación")

col1, col2 = st.columns(2)

with col1:
    st.subheader("A. Participación (Elasticidad)")
    st.markdown("¿Qué % de cada bloque base irá a votar?")
    part_L = st.slider(f"% Participación Bloque Izquierda ({candidato_L})", 50, 100, 90)
    part_R = st.slider(f"% Participación Bloque Derecha ({candidato_R})", 50, 100, 90)
    part_C = st.slider(f"% Participación Bloque Bisagra", 30, 100, 70)

with col2:
    st.subheader("B. Transferencia (Voto Bisagra)")
    st.markdown(f"De los votantes 'Bisagra' que participan, ¿cómo se dividen?")
    transfer_C_to_R = st.slider(f"% Bisagra para {candidato_R}", 0, 100, default_transfer_R)

    # El resto del bloque bisagra se asigna a Jara
    transfer_C_to_L = 100 - transfer_C_to_R
    st.info(f"El {transfer_C_to_L}% restante del Bloque Bisagra se asigna a {candidato_L}.")

# --- 7. CÁLCULO DE RESULTADOS ---
votos_L_efectivos = BLOQUE_L_BASE * (part_L / 100)
votos_R_efectivos = BLOQUE_R_BASE * (part_R / 100)
votos_C_efectivos = BLOQUE_C_BASE * (part_C / 100)

# Votos finales por candidato
votos_Jara = votos_L_efectivos + (votos_C_efectivos * (transfer_C_to_L / 100))
votos_Candidato_R = votos_R_efectivos + (votos_C_efectivos * (transfer_C_to_R / 100))

total_votos = votos_Jara + votos_Candidato_R
pct_Jara = (votos_Jara / total_votos) * 100
pct_Candidato_R = (votos_Candidato_R / total_votos) * 100

# --- 8. VISUALIZACIÓN DE RESULTADOS ---
st.header("3. Resultados de la Simulación")
st.markdown("---")

res1, res2 = st.columns(2)
res1.metric(
    label=f"{candidato_L}",
    value=f"{pct_Jara:.1f}%",
    delta=f"{votos_Jara:,.0f} votos totales"
)
res2.metric(
    label=f"{candidato_R}",
    value=f"{pct_Candidato_R:.1f}%",
    delta=f"{votos_Candidato_R:,.0f} votos totales"
)

# Preparar datos para el gráfico
chart_data = pd.DataFrame({
    "Candidato": [candidato_L, candidato_R],
    "Porcentaje": [pct_Jara, pct_Candidato_R],
    "Votos": [votos_Jara, votos_Candidato_R]
})

# Gráfico de barras
st.subheader("Resultado Porcentual")
st.bar_chart(chart_data.set_index("Candidato")["Porcentaje"])

# Expansor para ver el detalle del cálculo
with st.expander("Ver detalle de la composición del voto"):
    st.markdown(f"""
    **Votos para {candidato_L}:**
    * Votos Bloque Izquierda: `{votos_L_efectivos:,.0f}`
    * Votos Bloque Bisagra: `{(votos_C_efectivos * (transfer_C_to_L / 100)):,.0f}`
    * **Total: `{votos_Jara:,.0f}`**

    **Votos para {candidato_R}:**
    * Votos Bloque Derecha: `{votos_R_efectivos:,.0f}`
    * Votos Bloque Bisagra: `{(votos_C_efectivos * (transfer_C_to_R / 100)):,.0f}`
    * **Total: `{votos_Candidato_R:,.0f}`**
    """)

#Imagen de Doctor Strange
st.image("strange.jpeg", caption="Escasas posibilidades, pero no imposibles")
