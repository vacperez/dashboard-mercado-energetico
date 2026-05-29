import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from api_client import extraer_datos_xm

st.set_page_config(page_title="Dashboard Energético XM", layout="wide")
st.title("⚡ Dashboard Mercado Energético (XM)")

# --- CARGA DE CATÁLOGOS LOCALES ---
@st.cache_data
def cargar_catalogos():
    try:
        df_agentes = pd.read_csv("agentes.xlsx - Listado_Agentes.csv", skiprows=3)
        df_recursos = pd.read_csv("recursos.xlsx - Listado_Recursos_Generacion.csv", skiprows=3)
        return df_agentes, df_recursos
    except Exception as e:
        st.warning("Nota: No se encontraron los archivos CSV locales para los filtros avanzados.")
        return pd.DataFrame(), pd.DataFrame()

df_agentes, df_recursos = cargar_catalogos()

# --- MENÚ LATERAL ---
st.sidebar.header("Navegación")
opciones = ["1. Panel de Precios", "2. Panel de Producción", "3. Panel de Consumo", "4. Panel del Agua"]
seleccion = st.sidebar.radio("Secciones:", opciones)

# --- PANEL 1: PRECIOS ---
if seleccion == "1. Panel de Precios":
    st.header("💵 Precio de Bolsa Nacional")
    fecha = st.date_input("Selecciona un día", datetime.date(2023, 10, 1))
    
    if st.button("Consultar Precios"):
        with st.spinner("Descargando datos..."):
            df = extraer_datos_xm("hourly", "PrecBolsNaci", "Sistema", fecha, fecha)
            if not df.empty:
                promedio = df["Valor"].mean()
                st.metric("Precio de Bolsa Promedio", f"${promedio:.2f} COP")
                fig = px.box(df, y="Valor", title=f"Box Plot: Picos de Precio ({fecha})", points="all")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Sin datos para esta fecha.")

# --- PANEL 2: PRODUCCIÓN ---
elif seleccion == "2. Panel de Producción":
    st.header("🏭 Top 10 Plantas Despachadas Centralmente (DC)")
    hoy = datetime.date.today()
    f_inicio = st.date_input("Fecha Inicio", hoy - datetime.timedelta(days=7))
    f_fin = st.date_input("Fecha Fin", hoy - datetime.timedelta(days=1))
    
    if st.button("Consultar Producción"):
        with st.spinner("Procesando..."):
            df_gen = extraer_datos_xm("hourly", "Gene", "Recurso", f_inicio, f_fin)
            if not df_gen.empty and not df_recursos.empty:
                # Filtrar solo Plantas DC
                plantas_dc = df_recursos[df_recursos['Tipo Despacho'] == 'DC']['Código SIC'].tolist()
                df_dc = df_gen[df_gen['Entidad'].isin(plantas_dc)]
                
                # Agrupar y graficar
                top_10 = df_dc.groupby("Entidad")["Valor"].sum().reset_index().nlargest(10, "Valor").sort_values(by="Valor")
                fig = px.bar(top_10, x="Valor", y="Entidad", orientation='h', title="Generación Total (kWh)")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Faltan datos de la API o el catálogo de recursos.")

# --- PANEL 3: CONSUMO ---
elif seleccion == "3. Panel de Consumo":
    st.header("📈 Demanda Comercial por Agente")
    if not df_agentes.empty:
        # Filtrar solo comercializadores
        comercializadores = df_agentes[df_agentes['Actividad'].str.contains('COMERCIALIZA', na=False, case=False)]
        agente = st.selectbox("Selecciona Comercializador:", comercializadores['Nombre Agente'].tolist())
        
        f_fin = datetime.date.today()
        f_inicio = f_fin - datetime.timedelta(days=30)
        
        if st.button("Ver Curva de Demanda"):
            cod_agente = comercializadores[comercializadores['Nombre Agente'] == agente]['Código SIC'].values[0]
            with st.spinner(f"Consultando últimos 30 días para {cod_agente}..."):
                df_demanda = extraer_datos_xm("hourly", "DemaCome", "Agente", f_inicio, f_fin)
                if not df_demanda.empty:
                    df_filtrado = df_demanda[df_demanda['Entidad'] == cod_agente].copy()
                    df_filtrado['Datetime'] = pd.to_datetime(df_filtrado['Fecha']) + pd.to_timedelta(df_filtrado['Hora'], unit='h')
                    df_filtrado = df_filtrado.sort_values('Datetime')
                    
                    fig = px.line(df_filtrado, x="Datetime", y="Valor", title=f"Demanda: {agente}")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Sin datos en este periodo.")

# --- PANEL 4: AGUA ---
elif seleccion == "4. Panel del Agua":
    st.header("💧 Nivel de Embalses Críticos")
    fecha_agua = st.date_input("Fecha", datetime.date.today() - datetime.timedelta(days=1))
    
    if st.button("Consultar Embalses"):
        with st.spinner("Consultando..."):
            df_agua = extraer_datos_xm("daily", "PorcVoluUtilDiar", "Embalse", fecha_agua, fecha_agua)
            if not df_agua.empty:
                df_agua['Entidad'] = df_agua['Entidad'].str.upper()
                criticos = df_agua[df_agua['Entidad'].isin(['GUATAPE', 'TOPOCORO', 'EL PEÑOL'])][['Entidad', 'Valor']]
                criticos.columns = ['Embalse', '% Volumen Útil']
                
                def pintar(val):
                    return 'color: red; font-weight: bold' if isinstance(val, (int, float)) and val < 30 else 'color: green'
                
                st.dataframe(criticos.style.applymap(pintar, subset=['% Volumen Útil']), hide_index=True, use_container_width=True)
            else:
                st.warning("Sin datos de embalses para hoy.")