import streamlit as st
import os

# Este bloco deve ser o PRIMEIRO do app.py!
if "GOOGLE_APPLICATION_CREDENTIALS" in st.secrets:
    with open("gcloud-key.json", "w") as f:
        f.write(st.secrets["GOOGLE_APPLICATION_CREDENTIALS"])
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud-key.json"
else:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ocr-desktop-460002-e6ee797c7953.json"
import streamlit as st
from PIL import Image
import os
import io
import re

from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ocr-desktop-460002-e6ee797c7953.json"

st.set_page_config(page_title="Numerador Esportivo Web", layout="centered")

st.title("Numerador Esportivo Web")

tab_manual, tab_ocr = st.tabs(["Numerador Manual", "Numerador OCR Automático"])

# ------------- Numerador Manual -----------------

with tab_manual:
    st.header("Numerador Manual (com atalhos de teclado)")
    uploaded_files = st.file_uploader("Selecione as imagens", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True, key="manual")
    if uploaded_files:
        if "manual_index" not in st.session_state:
            st.session_state.manual_index = 0
            st.session_state.numeros = [""] * len(uploaded_files)
            st.session_state.ordem = list(range(len(uploaded_files)))
            st.session_state.invertido = False

        idx = st.session_state.manual_index
        ordem = st.session_state.ordem

        def focus_number():
            st.session_state.number_focus = True

        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            img_bytes = uploaded_files[ordem[idx]].getvalue()
            st.image(img_bytes, width=360, caption=f"{uploaded_files[ordem[idx]].name}")

        numero = st.text_input("Digite o número:", st.session_state.numeros[ordem[idx]],
                               key=f"number_{ordem[idx]}", on_change=focus_number, max_chars=16)

        # Atualiza sempre que campo muda
        st.session_state.numeros[ordem[idx]] = numero

        col4, col5, col6, col7 = st.columns([1,1,1,1])
        with col4:
            if st.button("← Anterior", key="btn_ant") and idx > 0:
                st.session_state.manual_index -= 1
        with col5:
            if st.button("Copiar ↑", help="Copia número da imagem anterior", key="btn_copiar") and idx > 0:
                st.session_state.numeros[ordem[idx]] = st.session_state.numeros[ordem[idx-1]]
                st.experimental_rerun()
        with col6:
            if st.button("Próxima →", key="btn_prox") and idx < len(uploaded_files)-1:
                st.session_state.manual_index += 1
        with col7:
            if st.button("Inverter Ordem (Ctrl+R)", key="btn_inverter"):
                st.session_state.ordem = list(reversed(st.session_state.ordem))
                st.session_state.invertido = not st.session_state.invertido
                st.session_state.manual_index = 0

        # Atalhos de teclado (botões visíveis para uso rápido)
        st.info("Atalhos: Enter = próxima | ←/→ = navegar | ↑ = copiar anterior | Ctrl+R = inverter ordem")

        # Baixar CSV
        linhas = [f"{uploaded_files[i].name};{st.session_state.numeros[i]}" for i in ordem if st.session_state.numeros[i]]
        if linhas:
            csv_content = "\n".join(linhas)
            st.download_button("Baixar CSV", data=csv_content, file_name="numerador_manual.csv", mime="text/csv")

# ------------- OCR Automático Esportivo -----------------
import random

def esporte_svg(progresso, total, modalidade):
    pct = int((progresso/total)*400)
    atleta = {"Corrida":"🏃‍♂️", "Ciclismo":"🚴", "Natação":"🏊"}.get(modalidade, "🏃‍♂️")
    cor = "#4caf50"
    fundo = "#e0e0e0"
    svg = f'''
    <svg width="440" height="70">
      <rect x="20" y="40" width="400" height="14" rx="7" fill="{fundo}"/>
      <rect x="20" y="40" width="{pct}" height="14" rx="7" fill="{cor}"/>
      <circle cx="{20+pct}" cy="47" r="20" fill="#ffeb3b" stroke="#444" stroke-width="2"/>
      <text x="{20+pct}" y="53" font-size="24" text-anchor="middle">{atleta}</text>
    </svg>
    '''
    return svg

with tab_ocr:
    st.header("Numerador OCR Automático (Google Vision)")
    uploaded_files_ocr = st.file_uploader("Selecione imagens para OCR", type=['jpg','jpeg','png'], accept_multiple_files=True, key="ocr")
    modalidade = st.selectbox("Modalidade esportiva para animação:", ["Corrida", "Ciclismo", "Natação"])
    if uploaded_files_ocr:
        client = vision.ImageAnnotatorClient()
        ocr_results = []
        total = len(uploaded_files_ocr)
        barra = st.empty()
        for i, img_file in enumerate(uploaded_files_ocr):
            svg = esporte_svg(i+1, total, modalidade)
            barra.markdown(svg, unsafe_allow_html=True)
            content = img_file.read()
            image = vision.Image(content=content)
            response = client.text_detection(image=image)
            texts = response.text_annotations
            numeros = []
            if texts:
                encontrados = re.findall(r'\d+', texts[0].description)
                if encontrados:
                    numeros = encontrados
            linha = f"{img_file.name};{' '.join(numeros)}" if numeros else f"{img_file.name};"
            ocr_results.append(linha)
            st.image(Image.open(io.BytesIO(content)), caption=f"OCR: {linha}", width=320)
        barra.markdown(esporte_svg(total, total, modalidade), unsafe_allow_html=True)
        if st.button("Baixar CSV com resultados OCR", key="ocr_download") and ocr_results:
            csv_content = "\n".join(ocr_results)
            st.download_button(
                label="Download CSV",
                data=csv_content,
                file_name="numerador_ocr.csv",
                mime="text/csv"
            )


