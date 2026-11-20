import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Cargar datos
ruta = "https://github.com/davidvalencia95252/fundamentos-de-programacion/raw/refs/heads/main/Datos_Concreto.xlsx"
df = pd.read_excel(ruta, sheet_name="Ensayos")

print("-"*70)
print("Muestra la informacion del tipo de dato")
print("-"*70)
print(df.head())
print(df.info())
print("-"*70)

# 2. Limpieza de nombres de columnas
print("Columnas originales:", df.columns)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
df.rename(columns={"resistencia_a_la_compresión_(mpa)": "resistencia_mpa"}, inplace=True)
print("Columnas limpias:", df.columns)
print("-"*70)

# Eliminar filas o columnas completamente vacias
df.dropna(axis=0, how="all", inplace=True)
df.dropna(axis=1, how="all", inplace=True)

# Quitar duplicados
df.drop_duplicates(inplace=True)
print("Shape despues de quitar duplicados:", df.shape)

# Datos nulos
print(df.isnull().sum())
print("-"*70)

# Exportar el dataset limpio
df.to_excel("concreto_limpio.xlsx", index=False)
df.to_csv("concreto_limpio.csv", index=False)

# 3. Graficas (Histograma y Boxplot)
plt.figure(figsize=(8, 5))
sns.set_style("whitegrid")
sns.histplot(
    df["resistencia_mpa"],
    kde=True,
    color="#62109F",
    alpha=0.7
)
plt.title("Distribucion de resistencia a la compresion (MPa)", fontsize=16)
plt.xlabel("Resistencia (MPa)")
plt.ylabel("Frecuencia")
plt.show()

plt.figure(figsize=(8, 5))
sns.boxplot(df["resistencia_mpa"], color="#62109F")
plt.title("Boxplot resistencia a la compresion (MPa)", fontsize=16)
plt.show()

# 4. Filtros y consultas
consulta_concreto = df[["cemento_(kg/m³)", "agua_(kg/m³)", "resistencia_mpa"]]
consulta_concreto.to_excel("consulta_concreto.xlsx", index=False)

print(df[df["resistencia_mpa"] > 50])
print("-"*50)
print(df[df["edad_(días)"] == 28])
print("-"*50)
print(df[df["edad_(días)"].isin([7, 28])])
print("-"*50)

# Valores unicos e intervalos numericos
print("Edades unicas:", df["edad_(días)"].unique())
print(df[df["cemento_(kg/m³)"].between(300, 400)])
print("-"*50)
print(df[["cemento_(kg/m³)", "agua_(kg/m³)", "resistencia_mpa"]][df["cemento_(kg/m³)"].between(300, 400)])
print("-"*50)

# Conteo y agrupacion
print(df["edad_(días)"].value_counts())
print("-"*50)

resultado = df.groupby("edad_(días)").agg(
    promedio_resistencia=("resistencia_mpa", "mean"),
    max_cemento=("cemento_(kg/m³)", "max")
).reset_index()
print(resultado)
print("-"*50)

# Tabla ordenada sin duplicados
resultado_ordenado = (
    df[["edad_(días)", "cemento_(kg/m³)"]]
    .drop_duplicates()
    .sort_values(["edad_(días)", "cemento_(kg/m³)"])
    .reset_index(drop=True)
)
print(resultado_ordenado)