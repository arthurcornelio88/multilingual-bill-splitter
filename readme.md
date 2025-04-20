# 💸 Division des Dépenses Multilingue

Une application simple en **Streamlit** pour répartir équitablement les dépenses entre amis — avec prise en charge du **Français 🇫🇷**, **Português 🇧🇷** et **English 🇬🇧**.

---

## 🧠 À propos du projet

Cette application permet de saisir les noms et les montants dépensés par chaque personne, puis calcule automatiquement les transactions nécessaires pour équilibrer les comptes.

### 🇧🇷 Em português

Este app permite inserir os nomes e os valores gastos por cada pessoa, e calcula automaticamente quem deve pagar quem até que todos tenham contribuído igualmente.

### 🇬🇧 In English

This app lets you enter the names and amounts spent by each person, and automatically computes who owes whom until everyone has paid equally.

---

## 🚀 Exécution de l'application

### 🖥️ En local (avec pip)

```bash
git clone https://github.com/seu-usuario/divisao_contas_multilingue.git
cd divisao_contas_multilingue
pip install -r requirements.txt
streamlit run app.py
```

### 🐳 Avec Docker

```bash
docker build -t app-contas .
docker run -p 8501:8501 app-contas
```

Accès : [http://localhost:8501](http://localhost:8501)

---

## 🤗 Version en ligne

> Vous voulez tester sans rien installer ?

Essayez directement sur **Hugging Face Spaces** :

🔗 [https://huggingface.co/spaces/arthurcornelio88/divisao_contas_multilingue](https://huggingface.co/spaces/arthurcornelio88/divisao_contas_multilingue)  
*(lien fictif — à remplacer après le déploiement)*

---

## 🌍 Prise en charge des langues

Vous pouvez choisir votre langue préférée dans le menu latéral :

- 🇫🇷 **Français**
- 🇧🇷 **Português**
- 🇬🇧 **English**

---

## ✨ Technologies utilisées

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- Python 3.8+
- Docker (facultatif)

---

## 📚 Ce que j’ai appris en développant cette app

Ce projet a été une excellente occasion d’approfondir mes compétences avec **Streamlit**, en explorant à la fois des fonctionnalités simples et avancées. J’ai appris à créer des **interfaces interactives sur plusieurs pages**, avec navigation latérale et contenu dynamique. L’un des aspects les plus importants a été d’implémenter une **session persistante avec `st.session_state`**, qui permet de conserver les données même en changeant de page. J’ai également intégré la **génération de fichiers PDF dynamiques avec Matplotlib**, transformant les tableaux en rapports téléchargeables. Enfin, ce projet m’a permis de structurer mon code de manière modulaire, avec un système de traduction multilingue.

### 🇧🇷 Em português

Este projeto foi uma ótima oportunidade para me aprofundar em Streamlit, criando interfaces com múltiplas páginas e menus laterais. Aprendi a usar `st.session_state` para manter os dados entre interações, e implementei geração de PDFs dinâmicos com Matplotlib. Também organizei o código de forma modular e multilíngue.

### 🇬🇧 In English

This project was a great opportunity to go deeper with Streamlit, building a multi-page UI with sidebar navigation. I learned how to use `st.session_state` to persist data across interactions, and added dynamic PDF generation with Matplotlib. I also organized the code modularly and included multilingual support.

---

## 📄 Licence

Ce projet est sous licence MIT.  
Vous êtes libre de l’utiliser, le modifier et le partager ! 🚀
