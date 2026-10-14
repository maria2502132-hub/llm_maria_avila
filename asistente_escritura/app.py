import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Asistente de Escritura",
    page_icon="✍️",
    layout="centered"
)

st.title("✍️ Asistente de Escritura Automática")
st.write(
    "¡Hola! Soy tu asistente de escritura. Puedo ayudarte a corregir "
    "tu gramática, mejorar tu estilo, sugerir continuaciones o "
    "redactar textos completos."
)

# Configurar Gemini
api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not api_key:
    st.error(
        "No se encontró GEMINI_API_KEY. "
        "Agrega tu clave al archivo .env."
    )
    st.stop()

client = genai.Client(api_key=api_key)


# Función para generar respuestas
def generar_respuesta(prompt):
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config={
            "system_instruction": (
                "Eres un asistente de escritura profesional que responde "
                "en español. Corrige la ortografía, mejora la redacción "
                "y crea textos claros, naturales y coherentes. "
                "Respeta la intención original del usuario."
            )
        }
    )

    if not response.text:
        raise ValueError("El modelo no devolvió texto.")

    return response.text


# Seleccionar tarea
tarea = st.selectbox(
    "¿En qué te puedo ayudar hoy?",
    (
        "Mejorar redacción y ortografía",
        "Sugerir continuación",
        "Escribir un texto desde cero"
    )
)


# OPCIÓN 1: Mejorar redacción y ortografía
if tarea == "Mejorar redacción y ortografía":

    texto_usuario = st.text_area(
        "Pega aquí tu texto:",
        height=150
    )

    if st.button("Mejorar texto"):
        if texto_usuario.strip():
            with st.spinner("Revisando tu texto..."):
                try:
                    prompt = (
                        "Corrige la ortografía, la gramática y la redacción "
                        "del siguiente texto. Conserva su significado y "
                        "devuelve solamente la versión corregida:\n\n"
                        f"{texto_usuario}"
                    )

                    resultado = generar_respuesta(prompt)

                    st.subheader("Texto mejorado")
                    st.write(resultado)

                except Exception as e:
                    st.error(
                        f"No se pudo procesar el texto: "
                        f"{type(e).__name__}: {e}"
                    )
        else:
            st.warning("Por favor, ingresa un texto para mejorar.")


# OPCIÓN 2: Sugerir continuación
elif tarea == "Sugerir continuación":

    texto_usuario = st.text_area(
        "Escribe el inicio de tu texto aquí:",
        height=150
    )

    if st.button("Sugerir continuación"):
        if texto_usuario.strip():
            with st.spinner("Pensando en ideas..."):
                try:
                    prompt = (
                        "Continúa el siguiente texto de forma coherente "
                        "y creativa. Agrega un párrafo que conecte "
                        "naturalmente con lo escrito, sin repetirlo:\n\n"
                        f"{texto_usuario}"
                    )

                    resultado = generar_respuesta(prompt)

                    st.subheader("Sugerencia")
                    st.write(resultado)

                except Exception as e:
                    st.error(
                        f"No se pudo generar la continuación: "
                        f"{type(e).__name__}: {e}"
                    )
        else:
            st.warning("Por favor, ingresa el inicio de tu texto.")


# OPCIÓN 3: Escribir un texto desde cero
elif tarea == "Escribir un texto desde cero":

    tema = st.text_input(
        "¿Sobre qué tema quieres escribir?"
    )

    tono = st.selectbox(
        "Elige el tono del texto:",
        ("Profesional", "Casual", "Creativo", "Persuasivo")
    )

    if st.button("Generar texto"):
        if tema.strip():
            with st.spinner("Escribiendo..."):
                try:
                    prompt = (
                        f"Escribe un texto sobre: {tema}. "
                        f"Utiliza un tono {tono.lower()}. "
                        "Organiza las ideas con claridad y adapta "
                        "el contenido al tema solicitado."
                    )

                    resultado = generar_respuesta(prompt)

                    st.subheader("Texto generado")
                    st.write(resultado)

                except Exception as e:
                    st.error(
                        f"No se pudo generar el texto: "
                        f"{type(e).__name__}: {e}"
                    )
        else:
            st.warning("Por favor, ingresa un tema.")
