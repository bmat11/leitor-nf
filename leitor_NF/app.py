import streamlit as st
import pdfplumber
import re
from datetime import datetime

st.set_page_config(
    page_title="Leitor de Datas NF",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Leitor de Datas da Nota Fiscal")

st.markdown("Faça upload do **PDF da NF** para calcular o prazo de pagamento (DDL).")

arquivo = st.file_uploader("📎 Anexar PDF da NF", type="pdf")

if arquivo:

    texto = ""

    with pdfplumber.open(arquivo) as pdf:
        for pagina in pdf.pages:
            conteudo = pagina.extract_text()
            if conteudo:
                texto += conteudo

    datas = re.findall(r"\d{2}/\d{2}/\d{4}", texto)

    if len(datas) >= 2:

        data_emissao = datas[0]
        data_vencimento = datas[1]

        emissao = datetime.strptime(data_emissao, "%d/%m/%Y")
        vencimento = datetime.strptime(data_vencimento, "%d/%m/%Y")

        ddl = (vencimento - emissao).days

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("📅 Emissão", data_emissao)

        with col2:
            st.metric("💰 Vencimento", data_vencimento)

        with col3:
            st.metric("⏳ Prazo (DDL)", f"{ddl} dias")

        st.success("Datas extraídas com sucesso!")

    else:
        st.error("Não foi possível encontrar duas datas no PDF.")