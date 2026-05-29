import requests
import pandas as pd
import streamlit as st

def extraer_datos_xm(endpoint, metric_id, entity, start_date, end_date):
    url = f"https://servapibi.xm.com.co/{endpoint}"
    payload = {
        "MetricId": metric_id,
        "Entity": entity,
        "StartDate": start_date.strftime("%Y-%m-%d"),
        "EndDate": end_date.strftime("%Y-%m-%d")
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        items = data.get("Items", [])
        if not items:
            return pd.DataFrame() 
            
        registros = []
        for item in items:
            fecha_str = item.get("Date")
            llave_entidad = "HourlyEntities" if endpoint == "hourly" else "DailyEntities"
            entidades = item.get(llave_entidad, [])
            
            for ent in entidades:
                nombre_entidad = ent.get("Entity")
                valores = ent.get("Values", [])
                for val in valores:
                    registros.append({
                        "Fecha": fecha_str,
                        "Entidad": nombre_entidad,
                        "Hora": val.get("Hour", None),
                        "Valor": val.get("Value", 0)
                    })
        return pd.DataFrame(registros)
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión con la API de XM: {e}")
        return pd.DataFrame()