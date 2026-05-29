
# Dashboard de Mercado Energético (XM)

Aplicación web interactiva desarrollada para el consumo y visualización de datos de la API de XM. Este dashboard permite consultar indicadores clave del mercado eléctrico colombiano, incluyendo precios de bolsa, generación por recursos, demanda comercial y niveles de embalses.

## Características principales
- **Panel de Precios:** Visualización de precios horarios de bolsa con análisis estadístico (*box plot*).
- **Panel de Producción:** Top 10 de plantas con mayor generación (Despachadas Centralmente).
- **Panel de Consumo:** Consulta de demanda histórica por agente comercializador.
- **Panel del Agua:** Monitoreo del nivel de embalses críticos con alertas visuales.

## Tecnologías utilizadas
- **Python 3.14.5**
- **Streamlit**: Framework para la interfaz de usuario.
- **Pandas**: Procesamiento y manipulación de datos.
- **Requests**: Consumo de servicios REST API.
- **Plotly**: Visualización de gráficos interactivos.

## Instrucciones de instalación
Para ejecutar este proyecto en tu entorno local, sigue estos pasos:

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DE_TU_REPOSITORIO>
   cd <NOMBRE_DEL_PROYECTO>
2. Crear y activar un entorno virtual:
   # Windows
    python -m venv venv
    venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate

3. Instalar dependencias:
    pip install -r requirements.txt

4. Ejecutar la aplicación:
    streamlit run app.py

##  Estructura del proyecto
- **app.py**: Lógica principal de la aplicación y diseño de los paneles.
- **api_client.py**: Módulo especializado en la conexión y transformación de datos de la API de XM.
- **requirements.txt**: Lista de librerías necesarias.
- **agentes.csv / recursos.csv**: Catálogos locales para filtrado de datos.
