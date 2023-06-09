# ufam-bd-tp3

**Leia atentamente o passo a passo abaixo para executar o trabalho:**

## Definindo a senha Sudo

Como o jupyter notebook não permite que o usuário coloque suas senhas em comando `sudo`, **salve sua senha sudo no arquivo texto `mypassword.txt`.** Isso pois, todos os comandos que utilizam `sudo` irão buscar a senha nesse arquivo.

## Python e Virtualenv

No diretório da pasta do trabalho, configure uma virtualenv do python para não instalar as bibliotecas no seu python do sistema:

```bash
python3 -m venv venv
```

Entre na virtualenv:

```bash
source venv/bin/activate
```

Em seguida, instale os pacotes do python: 

```bash
pip install -r requirements.txt
```

## Rodando o docker

Dentro do ambiente virtual, construa a imagem:

```bash
sudo docker build . -t tp3
```

Em seguida, rode o docker assim:

```bash
sudo docker run --name tp3 -p 5433:5432 -p 8888:8888 -v $(pwd)/notebooks/:/app/notebooks -v $(pwd)/datadir/:/app/datadir tp3
```

Como no **Dockerfile** temos o comando `CMD service postgresql start && tail -f /dev/null`, o container já estará iniciado e ficará rodando na janela do terminal em que você digitou o comando.

Agora, sem fechar essa janela, abra outra janela no terminal e execute o seguinte comando para abrir o jupyter notebook: 

```python
sudo docker exec tp3 jupyter notebook --notebook-dir=/app/notebooks/ --allow-root --ip 0.0.0.0 --no-browser
```

Após isso, vá até http://localhost:8888/ no seu navegador. 

Será pedido o token, basta você colocar o token fornecido pelo terminal:

![image](https://github.com/NathSantos/tp3_Nathalia_Alice_Igor/assets/63311872/010c3880-bbf5-417c-8201-f49e1d864eeb)

Em seguida, você já estará dentro da pasta *notebooks* no jupyter e pode executar as células do(s) notebook(s).
