import pandas as pd

# cargar datos
ruta = "https://github.com/davidvalencia95252/fundamentos-de-programacion/raw/refs/heads/main/Datos_Concreto.xlsx"
df = pd.read_excel(ruta, sheet_name="Ensayos")

print("-"*50)
print(df.head())
print("-"*50)

print("-"*50)
print(df.info())
print("-"*50)

print("-"*50)
print(df.describe())
print("-"*50)

print("-"*50)
print(df.columns)
print("-"*50)

print("-"*50)
print(df.isnull().sum())
print("-"*50)

print("-"*50)
print(df.shape) # filas columnas
print("-"*50)

print("-"*50)
print(df["Cemento (kg/m³)"])
print("-"*50)

print("-"*50)
print(df[["Cemento (kg/m³)", "Agua (kg/m³)"]])
print("-"*50)

print("-"*50)
print(df[df["Edad (días)"] == 28])
print("-"*50)