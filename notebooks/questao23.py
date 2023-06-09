import psycopg2
import random
import threading
import time

# Configurações do banco de dados
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'tpchdb'
DB_USER = 'tpch'
DB_PASSWORD = 'test123'

# Configurações da simulação
NUM_VOOS = 200
NUM_CLIENTES = 200
TEMPO_ESCOLHA = 1  # em segundos

# Abre o arquivo em modo de escrita
arquivo = open('saida_parte5.txt', 'w')

# Classe para representar um agente de viagens
class AgenteViagens(threading.Thread):
    def __init__(self, thread_id, conn, version, isolation_level):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.conn = conn
        self.version = version
        self.isolation_level = isolation_level

    def run(self):
        print(f'Iniciando thread {self.thread_id}')
        for cliente in range(NUM_CLIENTES):
            while True:
                # Passo 1: Recupera a lista de assentos disponíveis
                cursor = self.conn.cursor()
                cursor.execute(f'SELECT num_voo FROM Assentos WHERE disp = true')
                assentos_disponiveis = cursor.fetchall()
                cursor.close()

                if len(assentos_disponiveis) == 0:
                    break  # Todos os assentos foram reservados

                # Passo 2: Escolhe um assento aleatoriamente
                num_voo = random.choice(assentos_disponiveis)[0]
                time.sleep(TEMPO_ESCOLHA)

                # Passo 3: Registra a reserva do assento
                cursor = self.conn.cursor()
                cursor.execute(f'UPDATE Assentos SET disp = false WHERE num_voo = {num_voo}')
                if self.version == 'b':
                    self.conn.commit()  # Passo 3 em uma transação separada
                cursor.close()

                if self.version == 'a':
                    self.conn.commit()  # Passo 1 e 3 em uma única transação

                print(f'Thread {self.thread_id}: Cliente {cliente + 1} reservou assento {num_voo}')
                break

        print(f'Thread {self.thread_id} concluída')

def main():
    # Conecta ao banco de dados
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)

    # Cria a tabela Assentos se não existir
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS Assentos')
    cursor.execute('CREATE TABLE IF NOT EXISTS Assentos (num_voo INTEGER PRIMARY KEY, disp BOOLEAN)')
    cursor.execute('DELETE FROM Assentos')  # Limpa a tabela
    for num_voo in range(1, NUM_VOOS + 1):
        cursor.execute(f'INSERT INTO Assentos (num_voo, disp) VALUES ({num_voo}, true)')
    conn.commit()
    cursor.close()

    # Executa a simulação para diferentes versões e níveis de isolamento
    versions = ['a', 'b']
    isolation_levels = ['READ COMMITTED', 'SERIALIZABLE']
    k_values = [1, 2, 4, 6, 8, 10]

    for version in versions:
        for isolation_level in isolation_levels:
            print(f'Versão: {version}, Nível de Isolamento: {isolation_level}')
            arquivo.write(f'Versão: {version}, Nível de Isolamento: {isolation_level}\n')

            for k in k_values:
                print(f'-> Simulação com {k} threads (agentes de viagem)')
                arquivo.write(f' -> Simulação com {k} threads (agentes de viagem)\n')
                
                cursor = conn.cursor()
                cursor.execute('UPDATE Assentos SET disp = true')
                conn.commit()
                cursor.close()
                
                threads = []
                
                start_time = time.time()  # Registra o tempo inicial

                # Cria e inicia os agentes de viagens
                for thread_id in range(k):
                    thread = AgenteViagens(thread_id + 1, conn, version, isolation_level)
                    thread.start()
                    threads.append(thread)

                # Aguarda a conclusão de todas as threads
                for thread in threads:
                    thread.join()
                    
                end_time = time.time()  # Registra o tempo final
                total_time = end_time - start_time  # Calcula o tempo total da simulação
                
                print(f'Tempo necessário para fazer todas as reservas: {total_time} segundos')
                arquivo.write(f'    Tempo necessário para fazer todas as reservas: {total_time} segundos\n')
        
    # Fecha a conexão com o banco de dados
    conn.close()
    arquivo.close()

if __name__ == '__main__':
    main()