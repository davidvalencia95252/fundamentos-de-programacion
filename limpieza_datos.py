import pandas as pd

#cargar datos
ruta = "https://raw.githubusercontent.com/VMjavier/claseAnalisisDatos/refs/heads/main/veterinaria_colombia.csv"
df = pd.read_csv(ruta)

print("="*50)
print(df.head())
print("="*50)

print("="*50)
print(df.info())
print("="*50)

print("="*50)
print(df.describe())
print("="*50)

print("="*50)
print(df.columns())
print("="*50)

print("="*50)
print(df.isnull().sum())
print("="*50)

print("="*50)
print(df.shape) #filas columnas)
print("="*50)

print("="*50)
print(df["raza"])
print("="*50)

print("="*50)
print(df[["raza","especie"]])
print("="*50)

print("="*50)
print(df[df["raza"] == "criollo"])
print("="*50)
