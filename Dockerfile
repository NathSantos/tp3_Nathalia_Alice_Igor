# Defina qual distro do linux vc quer usar
FROM ubuntu:22.04

# Instale as dependencias do SISTEMA OPERACIONAL
# Exemplo de como seria no ubuntu: RUN apt update && apt install -y python3 python3-pip libpq-dev
RUN apt update && apt install -y python3 python3-pip libpq-dev git wget unzip sudo

# Defina as variáveis de ambiente para evitar interação do usuário durante a instalação do postgresql
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Instale o PostgreSQL 14
RUN apt-get install -y postgresql-14

WORKDIR /app
COPY . /app

# Sua imagem deve ter o python 3.8+ instalado e o pip
RUN pip install -r requirements.txt

# Inicie o serviço do PostgreSQL e mantenha o container rodando
CMD service postgresql start && tail -f /dev/null