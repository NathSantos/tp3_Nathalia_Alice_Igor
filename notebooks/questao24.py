import matplotlib.pyplot as plt


import numpy as np
# Abrir o arquivo .txt
with open('saida_parte5.txt', 'r') as file:
    content = file.read()

# Dividir o conteúdo em linhas
lines = content.split('\n')

# Lista para armazenar os tempos
tempos = []

# Variável de contagem
count = 0

# Percorrer as linhas e extrair os tempos
for line in lines:
    if 'Tempo' in line:
        tempo = float(line.split(': ')[1].split(' segundos')[0])
        tempos.append(tempo)
        count += 1

        # Verificar se já foram lidas 6 simulações
        if count % 6 == 0:
            count = 0

num_sublistas = 4

sublistas = np.array_split(tempos, num_sublistas)
times_a_rc = sublistas[0]
times_a_s = sublistas[1]
times_b_rc = sublistas[2]
times_b_s = sublistas[3]

# Valores de k (número de agentes)
num_agents = [1, 2, 4, 6, 8, 10]

# Plotar gráfico para a versão 'a' com isolamento 'READ COMMITTED'
plt.plot(num_agents, times_a_rc, marker='o', label='Versão a - READ COMMITTED')

# Configurações do gráfico
plt.xlabel('Número de Agentes (k)')
plt.ylabel('Tempo necessário (segundos)')
plt.title('Tempo (Versão a - READ COMMITTED)')
plt.legend()
plt.grid(True)

# Salvar o gráfico em um arquivo
plt.savefig('grafico_a_rc.png')

# Limpar o gráfico atual
plt.clf()

# Plotar gráfico para a versão 'a' com isolamento 'SERIALIZABLE'
plt.plot(num_agents, times_a_s, marker='o', label='Versão a - SERIALIZABLE')

# Configurações do gráfico
plt.xlabel('Número de Agentes (k)')
plt.ylabel('Tempo necessário (segundos)')
plt.title('Tempo reservas (Versão a - SERIALIZABLE)')
plt.legend()
plt.grid(True)

# Salvar o gráfico em um arquivo
plt.savefig('grafico_a_s.png')

# Limpar o gráfico atual
plt.clf()

# Plotar gráfico para a versão 'b' com isolamento 'READ COMMITTED'
plt.plot(num_agents, times_b_rc, marker='o', label='Versão b - READ COMMITTED')

# Configurações do gráfico
plt.xlabel('Número de Agentes (k)')
plt.ylabel('Tempo necessário (segundos)')
plt.title('Tempo reservas (Versão b - READ COMMITTED)')
plt.legend()
plt.grid(True)

# Salvar o gráfico em um arquivo
plt.savefig('grafico_b_rc.png')

# Limpar o gráfico atual
plt.clf()

# Plotar gráfico para a versão 'a' com isolamento 'SERIALIZABLE'
plt.plot(num_agents, times_b_s, marker='o', label='Versão b - SERIALIZABLE')

# Configurações do gráfico
plt.xlabel('Número de Agentes (k)')
plt.ylabel('Tempo necessário (segundos)')
plt.title('Tempo (Versão b - SERIALIZABLE)')
plt.legend()
plt.grid(True)

# Salvar o gráfico em um arquivo
plt.savefig('grafico_b_s.png')

# Limpar o gráfico atual
plt.clf()

