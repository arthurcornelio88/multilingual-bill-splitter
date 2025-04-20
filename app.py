
import streamlit as st
import pandas as pd
from traducoes import textos, explicacoes, idiomas, paginas

st.set_page_config(page_title="Divisão de Contas", layout="centered")

# Idioma
lang = st.sidebar.selectbox("Idioma / Language / Langue", options=list(idiomas.keys()), format_func=lambda x: idiomas[x])
pagina = st.sidebar.radio("Navegação", paginas[lang])

def moeda(valor):
    return f"{valor:.2f} €"

if pagina == paginas[lang][0]:
    st.title(textos["titulo"][lang])

    num_pessoas = st.number_input(textos["quantas_pessoas"][lang], min_value=1, max_value=20, value=3, step=1)
    st.subheader(textos["quantas_pessoas"][lang])

    nomes = []
    gastos = []

    for i in range(num_pessoas):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input(f"{textos['nome_pessoa'][lang]} {i + 1}", key=f"nome_{i}")
        with col2:
            gasto = st.number_input(f"{textos['gasto_pessoa'][lang]} {i + 1}", min_value=0.0, format="%.2f", key=f"gasto_{i}")
        nomes.append(nome)
        gastos.append(gasto)

    if st.button(textos["calcular"][lang]):
        if "" in nomes:
            st.warning(textos["preencha_nomes"][lang])
        else:
            df = pd.DataFrame({"Nome": nomes, "Gastos": gastos})
            media = df["Gastos"].mean()
            df["Saldo"] = df["Gastos"] - media

            devedores = df[df["Saldo"] < 0].copy()
            recebedores = df[df["Saldo"] > 0].copy()
            devedores["Saldo"] = devedores["Saldo"].abs()

            transacoes = []
            while not devedores.empty and not recebedores.empty:
                devedores = devedores.sort_values(by="Saldo", ascending=False)
                recebedores = recebedores.sort_values(by="Saldo", ascending=False)
                devedor = devedores.iloc[0]
                recebedor = recebedores.iloc[0]
                valor = min(devedor["Saldo"], recebedor["Saldo"])

                transacoes.append({
                    textos["devedor"][lang]: devedor["Nome"],
                    textos["recebedor"][lang]: recebedor["Nome"],
                    textos["valor"][lang]: moeda(valor)
                })

                devedores.loc[devedores["Nome"] == devedor["Nome"], "Saldo"] -= valor
                recebedores.loc[recebedores["Nome"] == recebedor["Nome"], "Saldo"] -= valor
                devedores = devedores[devedores["Saldo"] > 0]
                recebedores = recebedores[recebedores["Saldo"] > 0]

            st.subheader(textos["resumo"][lang])
            df_fmt = df.copy()
            df_fmt[textos["gasto_label"][lang]] = df_fmt["Gastos"].map(moeda)
            df_fmt[textos["saldo_label"][lang]] = df_fmt["Saldo"].map(moeda)
            st.dataframe(df_fmt[["Nome", textos["gasto_label"][lang], textos["saldo_label"][lang]]], use_container_width=True)

            st.subheader(textos["transacoes"][lang])
            if transacoes:
                st.dataframe(pd.DataFrame(transacoes), use_container_width=True)
            else:
                st.info(textos["todos_ok"][lang])

else:
    st.title(paginas[lang][1])
    st.markdown(explicacoes[lang])
