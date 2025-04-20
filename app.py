
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from traducoes import textos, explicacoes, idiomas, paginas

st.set_page_config(page_title="Divisão de Contas", layout="centered")

# Idioma
lang = st.sidebar.selectbox("Idioma / Language / Langue", options=list(idiomas.keys()), format_func=lambda x: idiomas[x])
pagina = st.sidebar.radio("Navegação", paginas[lang])

def moeda(valor):
    return f"{valor:.2f} €"

def salvar_em_pdf(df_gastos, df_transacoes, nome_arquivo="transacoes.pdf"):
    with PdfPages(nome_arquivo) as pdf:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.axis('tight')
        ax.axis('off')

        col1_x, col2_x = 0.05, 0.55

        tabela_gastos = ax.table(
            cellText=df_gastos.values,
            colLabels=df_gastos.columns,
            loc='center',
            bbox=[col1_x, 0.1, 0.4, 0.8],
            cellLoc='center'
        )
        tabela_gastos.auto_set_font_size(False)
        tabela_gastos.set_fontsize(12)

        for key, cell in tabela_gastos.get_celld().items():
            if key[0] == 0:
                cell.set_text_props(weight='bold')

        tabela_transacoes = ax.table(
            cellText=df_transacoes.values,
            colLabels=df_transacoes.columns,
            loc='center',
            bbox=[col2_x, 0.1, 0.4, 0.8],
            cellLoc='center'
        )
        tabela_transacoes.auto_set_font_size(False)
        tabela_transacoes.set_fontsize(12)

        for key, cell in tabela_transacoes.get_celld().items():
            if key[0] == 0:
                cell.set_text_props(weight='bold')

        plt.suptitle("Relatório de Gastos e Transações", fontsize=18, y=0.95)
        pdf.savefig()
        plt.close()

    return nome_arquivo

# Inicializar session_state
if "nomes" not in st.session_state:
    st.session_state.nomes = []
if "gastos" not in st.session_state:
    st.session_state.gastos = []
if "df_resultado" not in st.session_state:
    st.session_state.df_resultado = None
if "df_transacoes" not in st.session_state:
    st.session_state.df_transacoes = None

if pagina == paginas[lang][0]:
    st.title(textos["titulo"][lang])

    num_pessoas = st.number_input(textos["quantas_pessoas"][lang], min_value=1, max_value=20, value=len(st.session_state.nomes) or 3, step=1)

    st.session_state.nomes = st.session_state.nomes[:num_pessoas] + [""] * (num_pessoas - len(st.session_state.nomes))
    st.session_state.gastos = st.session_state.gastos[:num_pessoas] + [0.0] * (num_pessoas - len(st.session_state.gastos))

    for i in range(num_pessoas):
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.nomes[i] = st.text_input(f"{textos['nome_pessoa'][lang]} {i + 1}", value=st.session_state.nomes[i], key=f"nome_{i}")
        with col2:
            st.session_state.gastos[i] = st.number_input(f"{textos['gasto_pessoa'][lang]} {i + 1}", min_value=0.0, format="%.2f", value=st.session_state.gastos[i], key=f"gasto_{i}")

    if st.button(textos["calcular"][lang]):
        if "" in st.session_state.nomes:
            st.warning(textos["preencha_nomes"][lang])
        else:
            df = pd.DataFrame({"Nome": st.session_state.nomes, "Gastos": st.session_state.gastos})
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

            st.session_state.df_resultado = df.copy()
            st.session_state.df_transacoes = pd.DataFrame(transacoes)

    if st.session_state.df_resultado is not None:
        df_fmt = st.session_state.df_resultado.copy()
        df_fmt[textos["gasto_label"][lang]] = df_fmt["Gastos"].map(moeda)
        df_fmt[textos["saldo_label"][lang]] = df_fmt["Saldo"].map(moeda)
        st.subheader(textos["resumo"][lang])
        st.dataframe(df_fmt[["Nome", textos["gasto_label"][lang], textos["saldo_label"][lang]]], use_container_width=True)

    if st.session_state.df_transacoes is not None:
        st.subheader(textos["transacoes"][lang])
        if not st.session_state.df_transacoes.empty:
            st.dataframe(st.session_state.df_transacoes, use_container_width=True)
            if st.download_button("📥 Gerar PDF", file_name="transacoes.pdf", mime="application/pdf",
                                  data=open(salvar_em_pdf(df_fmt[["Nome", textos["gasto_label"][lang], textos["saldo_label"][lang]]],
                                                          st.session_state.df_transacoes), "rb").read()):
                st.success("PDF gerado com sucesso!")
        else:
            st.info(textos["todos_ok"][lang])

else:
    st.title(paginas[lang][1])
    st.markdown(explicacoes[lang]["texto"])
    st.latex(explicacoes[lang]["formula"])
    st.markdown(explicacoes[lang]["final"])
