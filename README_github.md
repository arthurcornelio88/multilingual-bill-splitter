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

## 🚀 Tester tout de suite

[![Try on Hugging Face Spaces](https://img.shields.io/badge/🤗%20Try%20on-Hugging%20Face-blue?logo=huggingface)](https://huggingface.co/spaces/arthurcornelio88/divisao_contas_multilingue)

---

## 🎥 Demo

<img src="demo.gif" width="100%" alt="Demo de l'appli de division de frais multilangue">

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
- Matplotlib
- Docker (facultatif)

---

## 📄 Licence

Ce projet est sous licence MIT.  
Vous êtes libre de l’utiliser, le modifier et le partager ! 🚀
