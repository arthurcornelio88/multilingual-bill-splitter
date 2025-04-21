import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from traducoes import textos, explicacoes, idiomas, paginas

st.set_page_config(page_title="Divisão de Contas", layout="centered")

# Idioma e moeda
lang = st.sidebar.selectbox("Idioma / Language / Langue", options=list(idiomas.keys()), format_func=lambda x: idiomas[x])
pagina = st.sidebar.radio("Navegação", paginas[lang])
moeda_escolhida = st.sidebar.selectbox("Moeda", ["R$ Real", "€ Euro", "$ Dollar"])

# Função para formatar valores monetários
simbolos = {"R$ Real": "R$", "€ Euro": "€", "$ Dollar": "$"}
def moeda(valor):
    simbolo = simbolos.get(moeda_escolhida, "€")
    return f"{valor:.2f} {simbolo}"

# Função para salvar o PDF
def salvar_em_pdf(df_gastos, df_transacoes, textos, lang, nome_arquivo="transacoes.pdf"):
    def quebrar_texto(texto, max_chars=18):
        palavras = str(texto).split()
        linhas, linha = [], ""
        for palavra in palavras:
            if len(linha + palavra) + 1 > max_chars:
                linhas.append(linha.strip())
                linha = palavra + " "
            else:
                linha += palavra + " "
        linhas.append(linha.strip())
        return "\n".join(linhas)

    df_gastos = df_gastos.copy()
    df_transacoes = df_transacoes.copy()

    df_gastos["Nome"] = df_gastos["Nome"].apply(quebrar_texto)
    df_transacoes[textos["devedor"][lang]] = df_transacoes[textos["devedor"][lang]].apply(quebrar_texto)
    df_transacoes[textos["recebedor"][lang]] = df_transacoes[textos["recebedor"][lang]].apply(quebrar_texto)

    with PdfPages(nome_arquivo) as pdf:
        fig, ax = plt.subplots(figsize=(12, 8))
        fig, ax = plt.subplots(figsize=(12, 8))

        ax.axis('off')
        plt.rcParams["font.family"] = "DejaVu Sans"

        tabela_gastos = ax.table(
            cellText=df_gastos.values,
            colLabels=df_gastos.columns,
            cellLoc='center',
            loc='center',
            bbox=[0.05, 0.15, 0.4, 0.75]
        )
        tabela_gastos.set_fontsize(10)

        tabela_transacoes = ax.table(
            cellText=df_transacoes.values,
            colLabels=df_transacoes.columns,
            cellLoc='center',
            loc='center',
            bbox=[0.55, 0.15, 0.4, 0.75]
        )
        tabela_transacoes.set_fontsize(10)

        # Cabeçalhos em negrito
        for tabela in [tabela_gastos, tabela_transacoes]:
            for (row, _), cell in tabela.get_celld().items():
                if row == 0:
                    cell.set_text_props(weight='bold')

        plt.suptitle("Relatório de Gastos e Transações", fontsize=18, y=0.95)
        pdf.savefig()
        plt.close()

    return nome_arquivo

# Inicializa estados
for chave in ["nomes", "gastos", "df_resultado", "df_transacoes"]:
    if chave not in st.session_state:
        st.session_state[chave] = [] if chave in ["nomes", "gastos"] else None

# Página de cálculo
if pagina == paginas[lang][0]:
    st.title(textos["titulo"][lang])
    num_pessoas = st.number_input(textos["quantas_pessoas"][lang], min_value=1, max_value=20,
                                  value=len(st.session_state.nomes) or 3, step=1)

    st.session_state.nomes = st.session_state.nomes[:num_pessoas] + [""] * (num_pessoas - len(st.session_state.nomes))
    st.session_state.gastos = st.session_state.gastos[:num_pessoas] + [0.0] * (num_pessoas - len(st.session_state.gastos))

    for i in range(num_pessoas):
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.nomes[i] = st.text_input(f"{textos['nome_pessoa'][lang]} {i + 1}", value=st.session_state.nomes[i], key=f"nome_{i}")
        with col2:
            st.session_state.gastos[i] = st.number_input(f"{textos['gasto_pessoa'][lang]} {i + 1}", min_value=0.0,
                                                          format="%.2f", value=st.session_state.gastos[i], key=f"gasto_{i}")

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
                devedores = devedores.sort_values("Saldo", ascending=False)
                recebedores = recebedores.sort_values("Saldo", ascending=False)
                devedor, recebedor = devedores.iloc[0], recebedores.iloc[0]
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
            if st.download_button("📅 Gerar PDF", file_name="transacoes.pdf", mime="application/pdf",
                                  data=open(salvar_em_pdf(
                                    df_fmt[["Nome", textos["gasto_label"][lang], textos["saldo_label"][lang]]],
                                    st.session_state.df_transacoes,
                                    textos,
                                    lang
                                ), "rb").read()):
                st.success("PDF gerado com sucesso!")
        else:
            st.info(textos["todos_ok"][lang])

else:
    st.title(paginas[lang][1])
    st.markdown(explicacoes[lang]["texto"])
    st.latex(explicacoes[lang]["formula"])
    st.markdown(explicacoes[lang]["final"])