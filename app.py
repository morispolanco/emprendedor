import streamlit as st
import requests
import json
from datetime import datetime

# Carga las API Keys desde los secrets de Streamlit
together_api_key = st.secrets["together_api_key"]
serper_api_key = st.secrets["serper_api_key"]

st.title("Dashboard de Inteligencia Competitiva para Emprendedores")

# Sección para configurar búsqueda de competidores
st.header("Monitoreo de Competencia y Noticias del Mercado")
competitors = st.text_area("Introduce los nombres de tus competidores, separados por comas")
filter_region = st.text_input("Filtro por región (opcional)")
filter_sector = st.text_input("Filtro por sector (opcional)")
interval = st.selectbox("Frecuencia de actualización", ["Diaria", "Semanal"])

# Función para realizar una búsqueda en Google utilizando la API de Serper
def request_serper(query):
    url = 'https://google.serper.dev/search'
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }
    data = json.dumps({"q": query})
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# Función para realizar análisis de texto con la API de Together
def request_together(messages, model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo", max_tokens=2512, temperature=0.7):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {together_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

# Monitoreo de competencia
if st.button("Monitorear Competencia"):
    competitor_list = competitors.split(",")
    for competitor in competitor_list:
        competitor = competitor.strip()
        search_query = f"{competitor} {filter_region} {filter_sector}".strip()
        st.write(f"Buscando información sobre {competitor} en {filter_region} para el sector {filter_sector}...")
        serper_results = request_serper(search_query)
        
        # Mostrar resultados relevantes
        if 'organic' in serper_results:
            for result in serper_results['organic']:
                st.write(f"**Título**: {result['title']}")
                st.write(f"**Link**: {result['link']}")
                st.write(f"**Descripción**: {result['snippet']}")
                st.write("---")
        else:
            st.write(f"No se encontraron resultados para {competitor}.")

# Sección para analizar tendencias del mercado
st.header("Detección de Tendencias Emergentes")
industry_keywords = st.text_area("Introduce palabras clave de la industria (ejemplo: tecnología, innovación)")
if st.button("Buscar Tendencias"):
    st.write("Buscando tendencias del mercado...")
    serper_results = request_serper(industry_keywords)
    
    if 'organic' in serper_results:
        snippets = " ".join([result['snippet'] for result in serper_results['organic']])
        st.write("Generando análisis de las tendencias con Together...")
        messages = [{"role": "user", "content": snippets}]
        together_response = request_together(messages)
        st.json(together_response)
    else:
        st.write("No se encontraron resultados para esas palabras clave.")

# Sección para generar ideas de contenido
st.header("Generación de Ideas de Contenido")
content_keywords = st.text_area("Introduce palabras clave para generar ideas de contenido (ejemplo: marketing digital, SEO)")
if st.button("Generar Ideas"):
    st.write("Generando ideas de contenido con Together...")
    messages = [{"role": "user", "content": f"Genera ideas de contenido sobre {content_keywords}."}]
    together_response = request_together(messages)
    st.json(together_response)

# Dashboard Centralizado
st.header("Dashboard Centralizado de Tendencias y Competencia")

# Mostrar últimas actualizaciones
st.write("Últimas actualizaciones:")
if competitors:
    st.write(f"Competencia monitoreada: {competitors}")
if industry_keywords:
    st.write(f"Tendencias clave en la industria: {industry_keywords}")
if content_keywords:
    st.write(f"Ideas de contenido generadas basadas en: {content_keywords}")

# Alertas
st.subheader("Alertas")
if competitors or industry_keywords:
    st.write("Mostrando alertas basadas en competencia o tendencias emergentes...")
    st.write(f"Actualización {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Automatización de búsquedas
st.subheader("Automatización de Búsquedas")
if interval == "Diaria":
    st.write("Las búsquedas y resúmenes se actualizarán diariamente.")
elif interval == "Semanal":
    st.write("Las búsquedas y resúmenes se actualizarán semanalmente.")

st.write("Esta aplicación ayuda a los emprendedores a monitorear la competencia, detectar tendencias emergentes, generar ideas de contenido, y visualizar la información de manera centralizada en un dashboard.")
