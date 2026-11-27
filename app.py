import streamlit as st
import pandas as pd
import plotly.express as px


DATA_PATH = r"data_base\Valor_de_Matricula_-_Programas_Universidad_Colegio_Mayor_de_Cundinamarca_20261126.csv"

COL_PROGRAMA = "PROGRAMA"
COL_INGRESO = "NIVEL DE INGRESOS"
COL_INGRESO_MAX = "NIVEL DE INGRESO MAXIMO"
COL_MATRICULA = "VALOR DE MATRICULA"
COL_SMLMV = "Valor en SMLMV"

COLORS = ["#131B2B", "#2F4A63", "#5B91A3", "#CFEAE0"]

st.set_page_config(
    page_title="Dashboard de Matrículas",
    page_icon="🎓",
    layout="wide",
)


@st.cache_data
def cargar_datos():
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()

    df[COL_MATRICULA] = (
        df[COL_MATRICULA]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
        .pipe(pd.to_numeric, errors="coerce")
    )

    for columna in [COL_PROGRAMA, COL_INGRESO, COL_INGRESO_MAX]:
        df[columna] = df[columna].astype("string").str.strip()

    return df


def opciones_filtradas(df, columna):
    return sorted(df[columna].dropna().astype(str).unique().tolist())


def estilo_grafico(fig, titulo):
    fig.update_layout(
        title={"text": titulo, "x": 0.02, "xanchor": "left", "font": {"size": 18, "color": COLORS[0]}},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Arial", "color": COLORS[0]},
        margin={"l": 20, "r": 20, "t": 70, "b": 35},
        legend={"orientation": "h", "y": -0.18},
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#DDE5E8", zeroline=False)
    return fig


st.markdown(
    f"""
    <style>
    .stApp {{ background: linear-gradient(135deg, #F7FAF9 0%, #EAF3F1 100%); }}
    [data-testid="stSidebar"] {{ background: {COLORS[0]}; }}
    [data-testid="stSidebar"] * {{ color: #FFFFFF; }}
    [data-testid="stSidebar"] .stSelectbox label {{ font-weight: 600; }}
    h1, h2, h3 {{ color: {COLORS[0]}; }}
    .metric-card {{
        background: white;
        border-left: 5px solid {COLORS[2]};
        border-radius: 8px;
        padding: 14px;
        box-shadow: 0 3px 12px rgba(19,27,43,0.08);
    }}
    .review {{
        background: {COLORS[3]};
        color: {COLORS[0]};
        border-left: 5px solid {COLORS[1]};
        border-radius: 8px;
        padding: 14px 16px;
        margin-top: 8px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

try:
    df = cargar_datos()
except Exception as error:
    st.error(f"No fue posible cargar la base de datos: {error}")
    st.stop()

st.title("Dashboard de valor de matrícula")
st.caption("Universidad Colegio Mayor de Cundinamarca")

st.sidebar.header("Filtros de consulta")

# Cada filtro se construye sobre el resultado del filtro anterior.
df_f1 = df.copy()
opciones_programa = opciones_filtradas(df_f1, COL_PROGRAMA)
programa = st.sidebar.selectbox("PROGRAMA", ["Todos"] + opciones_programa)
if programa != "Todos":
    df_f1 = df_f1[df_f1[COL_PROGRAMA] == programa]

opciones_ingreso = opciones_filtradas(df_f1, COL_INGRESO)
ingreso = st.sidebar.selectbox("NIVEL DE INGRESO", ["Todos"] + opciones_ingreso)
if ingreso != "Todos":
    df_f1 = df_f1[df_f1[COL_INGRESO] == ingreso]

opciones_ingreso_max = opciones_filtradas(df_f1, COL_INGRESO_MAX)
ingreso_max = st.sidebar.selectbox("NIVEL DE INGRESO MAXIMO", ["Todos"] + opciones_ingreso_max)
if ingreso_max != "Todos":
    df_f1 = df_f1[df_f1[COL_INGRESO_MAX] == ingreso_max]

opciones_matricula = opciones_filtradas(df_f1, COL_MATRICULA)
opciones_matricula_fmt = [f"$ {int(valor):,.0f}".replace(",", ".") for valor in opciones_matricula if pd.notna(valor)]
matricula_opciones = ["Todos"] + opciones_matricula_fmt
matricula = st.sidebar.selectbox("VALOR DE MATRICULA", matricula_opciones)
if matricula != "Todos":
    valor_seleccionado = int(matricula.replace("$", "").replace(".", "").strip())
    df_f1 = df_f1[df_f1[COL_MATRICULA] == valor_seleccionado]

st.sidebar.divider()
mostrar_tabla = st.sidebar.toggle("Mostrar tabla", value=False)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Programas", df_f1[COL_PROGRAMA].nunique())
with col2:
    st.metric("Niveles de ingreso", df_f1[COL_INGRESO].nunique())
with col3:
    st.metric("Matrícula promedio", f"$ {df_f1[COL_MATRICULA].mean():,.0f}".replace(",", ".") if df_f1[COL_MATRICULA].notna().any() else "N/D")

st.divider()

tab_programa, tab_ingreso, tab_ingreso_max, tab_matricula = st.tabs([
    "Programa",
    "Nivel de ingreso",
    "Nivel de ingreso máximo",
    "Valor de matrícula",
])

with tab_programa:
    conteo = df_f1.groupby(COL_PROGRAMA).size().reset_index(name="Cantidad")
    conteo = conteo.sort_values("Cantidad", ascending=True)
    fig = px.bar(
        conteo,
        x="Cantidad",
        y=COL_PROGRAMA,
        orientation="h",
        color="Cantidad",
        color_continuous_scale=[COLORS[3], COLORS[2], COLORS[1], COLORS[0]],
        text="Cantidad",
    )
    fig.update_traces(textposition="outside", marker_line_width=0)
    fig.update_layout(coloraxis_showscale=False)
    fig = estilo_grafico(fig, "Distribución de registros por programa")
    fig.update_xaxes(title="Registros")
    fig.update_yaxes(title="")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="review"><b>Programa:</b> identifica qué ofertas académicas aparecen en el alcance seleccionado y permite comparar su frecuencia dentro de la base.</div>', unsafe_allow_html=True)

with tab_ingreso:
    conteo = df_f1.groupby(COL_INGRESO).size().reset_index(name="Cantidad").sort_values("Cantidad", ascending=False)
    fig = px.bar(conteo, x=COL_INGRESO, y="Cantidad", color="Cantidad", color_continuous_scale=[COLORS[3], COLORS[2], COLORS[1]], text="Cantidad")
    fig.update_traces(textposition="outside", marker_line_width=0)
    fig.update_layout(coloraxis_showscale=False)
    fig = estilo_grafico(fig, "Cantidad de registros por nivel de ingreso")
    fig.update_xaxes(title="Nivel de ingreso")
    fig.update_yaxes(title="Registros")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="review"><b>Nivel de ingreso:</b> muestra cómo se distribuyen los límites inferiores del ingreso anual entre los registros filtrados.</div>', unsafe_allow_html=True)

with tab_ingreso_max:
    conteo = df_f1.groupby(COL_INGRESO_MAX).size().reset_index(name="Cantidad").sort_values("Cantidad", ascending=False)
    fig = px.bar(conteo, x=COL_INGRESO_MAX, y="Cantidad", color="Cantidad", color_continuous_scale=[COLORS[3], COLORS[2], COLORS[1]], text="Cantidad")
    fig.update_traces(textposition="outside", marker_line_width=0)
    fig.update_layout(coloraxis_showscale=False)
    fig = estilo_grafico(fig, "Cantidad de registros por ingreso máximo")
    fig.update_xaxes(title="Nivel de ingreso máximo")
    fig.update_yaxes(title="Registros")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="review"><b>Nivel de ingreso máximo:</b> resume los rangos superiores de ingreso asociados a cada matrícula en la selección activa.</div>', unsafe_allow_html=True)

with tab_matricula:
    matricula_promedio = df_f1.groupby(COL_PROGRAMA, as_index=False)[COL_MATRICULA].mean()
    matricula_promedio = matricula_promedio.sort_values(COL_MATRICULA, ascending=True)
    fig = px.bar(
        matricula_promedio,
        x=COL_MATRICULA,
        y=COL_PROGRAMA,
        orientation="h",
        color=COL_MATRICULA,
        color_continuous_scale=[COLORS[3], COLORS[2], COLORS[1], COLORS[0]],
        text=COL_MATRICULA,
    )
    fig.update_traces(texttemplate="$%{text:,.0f}".replace(".", ","), textposition="outside", marker_line_width=0)
    fig.update_layout(coloraxis_showscale=False)
    fig = estilo_grafico(fig, "Matrícula promedio por programa")
    fig.update_xaxes(title="Valor promedio", tickprefix="$ ", tickformat=",.0f")
    fig.update_yaxes(title="")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="review"><b>Valor de matrícula:</b> compara el costo promedio asociado a cada programa según los rangos de ingreso seleccionados.</div>', unsafe_allow_html=True)

st.divider()
st.subheader("Análisis cruzado por programa")
st.caption("Comparaciones entre cada programa y las variables económicas principales")

cruce1, cruce2, cruce3, cruce4 = st.tabs([
    "Programa vs. ingreso",
    "Programa vs. ingreso máximo",
    "Programa vs. matrícula",
    "Programa vs. SMLMV",
])

with cruce1:
    cruzado = pd.crosstab(df_f1[COL_PROGRAMA], df_f1[COL_INGRESO])
    fig = px.imshow(
        cruzado,
        text_auto=True,
        color_continuous_scale=[COLORS[3], COLORS[2], COLORS[1], COLORS[0]],
        aspect="auto",
    )
    fig = estilo_grafico(fig, "Frecuencia entre programa y nivel de ingreso")
    fig.update_xaxes(title="Nivel de ingreso", tickangle=-35)
    fig.update_yaxes(title="Programa")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="review"><b>Lectura:</b> las celdas más intensas muestran los niveles de ingreso con mayor presencia dentro de cada programa.</div>', unsafe_allow_html=True)

with cruce2:
    cruzado = pd.crosstab(df_f1[COL_PROGRAMA], df_f1[COL_INGRESO_MAX])
    fig = px.imshow(
        cruzado,
        text_auto=True,
        color_continuous_scale=[COLORS[3], COLORS[2], COLORS[1], COLORS[0]],
        aspect="auto",
    )
    fig = estilo_grafico(fig, "Frecuencia entre programa y nivel de ingreso máximo")
    fig.update_xaxes(title="Nivel de ingreso máximo", tickangle=-35)
    fig.update_yaxes(title="Programa")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="review"><b>Lectura:</b> permite identificar los rangos superiores de ingreso asociados con mayor frecuencia a cada oferta académica.</div>', unsafe_allow_html=True)

with cruce3:
    cruzado = df_f1.groupby(COL_PROGRAMA, as_index=False)[COL_MATRICULA].mean()
    cruzado = cruzado.sort_values(COL_MATRICULA, ascending=True)
    fig = px.bar(
        cruzado,
        x=COL_MATRICULA,
        y=COL_PROGRAMA,
        orientation="h",
        color=COL_MATRICULA,
        color_continuous_scale=[COLORS[3], COLORS[2], COLORS[1], COLORS[0]],
        text=COL_MATRICULA,
    )
    fig.update_traces(texttemplate="$%{text:,.0f}".replace(".", ","), textposition="outside", marker_line_width=0)
    fig.update_layout(coloraxis_showscale=False)
    fig = estilo_grafico(fig, "Valor promedio de matrícula por programa")
    fig.update_xaxes(title="Matrícula promedio", tickprefix="$ ", tickformat=",.0f")
    fig.update_yaxes(title="")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="review"><b>Lectura:</b> compara el costo medio de matrícula entre programas bajo los filtros económicos seleccionados.</div>', unsafe_allow_html=True)

with cruce4:
    smlmv_numerico = (
        df_f1[COL_SMLMV]
        .astype(str)
        .str.replace("SMLMV", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
        .pipe(pd.to_numeric, errors="coerce")
    )
    cruzado = df_f1.assign(SMLMV=smlmv_numerico).dropna(subset=["SMLMV"])
    cruzado = cruzado.groupby([COL_PROGRAMA, "SMLMV"], as_index=False).size()

    fig = px.line(
        cruzado,
        x="SMLMV",
        y="size",
        color=COL_PROGRAMA,
        markers=True,
        color_discrete_sequence=[COLORS[0], COLORS[1], COLORS[2], COLORS[3]],
    )
    fig.update_traces(marker={"size": 7}, line={"width": 2})
    fig = estilo_grafico(fig, "Frecuencia por programa y valor en SMLMV")
    fig.update_xaxes(title="Valor en SMLMV")
    fig.update_yaxes(title="Cantidad de registros")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="review"><b>Lectura:</b> relaciona la exigencia de matrícula expresada en SMLMV con la frecuencia de registros de cada programa.</div>', unsafe_allow_html=True)

if mostrar_tabla:
    st.subheader("Tabla filtrada")
    tabla = df_f1.copy()
    tabla[COL_MATRICULA] = tabla[COL_MATRICULA].apply(lambda valor: f"$ {valor:,.0f}".replace(",", ".") if pd.notna(valor) else "")
    st.dataframe(tabla, use_container_width=True, hide_index=True)
