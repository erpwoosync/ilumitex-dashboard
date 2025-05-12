import requests
import pandas as pd
import streamlit as st

# CONFIGURACIÓN
API_URL = "https://nocodb1.ews-cdn.link/api/v2/tables/mndae458b751b22/records?offset=0&limit=100"
API_TOKEN = "KlV8tM2Psi9Wf-bKufYt8MEfd27ENclCx1bNYtZ1"  # reemplazá por tu token de NocoDB

# OBTENER DATOS
headers = {
    "xc-token": API_TOKEN
}
response = requests.get(API_URL, headers=headers)
data = response.json()['list']  # lista de registros

# CONVERTIR A DATAFRAME
df = pd.DataFrame(data)

# CONVERTIR FECHAS
df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
df['CreatedAt'] = pd.to_datetime(df['CreatedAt'], errors='coerce')

# STREAMLIT DASHBOARD
st.title("📊 Dashboard - Log de Envios")

# FILTROS
canales = df['Canal_Envio'].dropna().unique()
canal_seleccionado = st.selectbox("Filtrar por canal de envío", ["Todos"] + list(canales))
fecha_min = df['Fecha'].min()
fecha_max = df['Fecha'].max()
rango_fecha = st.date_input("Rango de fechas", [fecha_min, fecha_max])

# FILTROS APLICADOS
df_filtrado = df.copy()
if canal_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Canal_Envio'] == canal_seleccionado]
df_filtrado = df_filtrado[
    (df_filtrado['Fecha'] >= pd.to_datetime(rango_fecha[0])) &
    (df_filtrado['Fecha'] <= pd.to_datetime(rango_fecha[1]))
]

# GRÁFICO ENVÍOS POR FECHA
st.subheader("📆 Envíos por Fecha")
envios_por_fecha = df_filtrado.groupby(df_filtrado['Fecha'].dt.date).size()
st.bar_chart(envios_por_fecha)

# ENVÍOS POR CLIENTE
st.subheader("👤 Clientes más activos")
clientes = df_filtrado['Razon_Social'].value_counts().head(10)
st.bar_chart(clientes)

# ENVÍOS POR CANAL
st.subheader("📨 Envíos por Canal")
por_canal = df_filtrado['Canal_Envio'].value_counts()
st.bar_chart(por_canal)

# VISTA DE DATOS
st.subheader("📋 Vista de datos filtrados")
st.dataframe(df_filtrado)
