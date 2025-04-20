# Use imagem oficial do Python com Streamlit
FROM python:3.10-slim

# Set UTF-8
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# Criar diretório de trabalho
WORKDIR /app

# Copiar arquivos para dentro da imagem
COPY . /app

# Instalar dependências
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Expor a porta padrão do Streamlit
EXPOSE 8501

# Comando para rodar o app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.runOnSave=true"]

