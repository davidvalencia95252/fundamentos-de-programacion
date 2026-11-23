import streamlit as st
import pandas as pd

st.title("🏗️ Análisis de Resistencia a la Compresión del Concreto")

st.header("⚡ 1. Contexto e Importancia en Obra")
st.write(
    "En la construcción civil, el concreto es el material estructural más utilizado, y su propiedad "
    "principal es la resistencia a la compresión (medida en Megapascales, MPa). Conocer cómo evoluciona "
    "esa resistencia permite garantizar la seguridad de columnas, vigas y losas, además de optimizar "
    "costos en el diseño de mezclas sin desperdiciar cemento."
)

st.subheader("¿Qué variables influyen en la mezcla?")
st.write(
    "La resistencia no depende de un solo material, sino de la proporción entre sus componentes y el "
    "tiempo de fraguado: cemento (kg/m³), agua, agregado grueso (grava), agregado fino (arena), "
    "aditivos (como superplastificantes o cenizas) y la edad de curado en días (siendo los 28 días "
    "la referencia estándar en obra)."
)

st.header("⚡ 2. Metodología y Exploración de Datos")
st.write(
    "Se partió de una base de datos de laboratorio con ensayos de cilindros de concreto. Antes de "
    "analizar, realizamos una limpieza con Python (Pandas) eliminando registros duplicados y verificando "
    "que no existieran valores nulos o erróneos, dejando una base confiable lista para consultar."
)

# 3 pestañas organizadas para ir mostrando durante la exposición
tab1, tab2, tab3 = st.tabs([
    "📊 Base de Datos Limpia",
    "🔍 Consulta: Edad vs. Cemento",
    "📈 Gráfica de Resistencia"
])

with tab1:
    st.subheader("Registros Depurados del Laboratorio")
    st.write(
        "Esta tabla contiene todos los ensayos válidos después de la limpieza. Cada fila representa una "
        "mezcla distinta con la cantidad exacta de cada material por metro cúbico y la resistencia final "
        "alcanzada en el ensayo de compresión."
    )
    df_limpio = pd.read_excel("concreto_limpio.xlsx")
    st.dataframe(df_limpio)

with tab2:
    st.subheader("Relación entre Edad de Curado y Cantidad de Cemento")
    st.write(
        "Aquí filtramos y ordenamos los ensayos por días de curado (desde 1 día hasta 365 días) y "
        "contenido de cemento (kg/m³), para comparar cómo varían las dosificaciones según el tiempo "
        "en que se falla el cilindro."
    )
    df_consulta = pd.read_excel("consulta_concreto.xlsx")
    st.dataframe(df_consulta)

with tab3:
    st.subheader("Resistencia Promedio según los Días de Curado")
    st.write(
        "En esta gráfica se observa claramente la curva de ganancia de resistencia del concreto: "
        "sube rápidamente durante los primeros 28 días y luego continúa ganando resistencia de forma "
        "más gradual hasta el año."
    )
    # Detecta automáticamente las columnas de edad y resistencia para graficar sin errores
    col_edad = [c for c in df_limpio.columns if "edad" in c.lower()][0]
    col_res = [c for c in df_limpio.columns if "res" in c.lower() or "mpa" in c.lower() or "comp" in c.lower()][0]
    promedio_edad = df_limpio.groupby(col_edad)[col_res].mean()
    st.bar_chart(promedio_edad)

st.header("⚡ 3. Conclusiones Principales")
st.write(
    "1. La limpieza de datos es indispensable antes de cualquier análisis técnico, ya que los registros "
    "repetidos pueden alterar los promedios de resistencia.\n\n"
    "2. El tiempo de curado es determinante: el concreto gana la mayor parte de su resistencia en los "
    "primeros 28 días, lo que explica por qué en obra se respetan estos tiempos antes de desencofra o cargar estructuras.\n\n"
    "3. Una mayor dosificación de cemento aumenta la resistencia final, pero debe equilibrarse con la "
    "relación agua/cemento para lograr mezclas eficientes y económicas."
) 