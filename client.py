import socket
import threading

# Configurações do cliente
HOST = '127.0.0.1'  # Endereço do servidor
PORT = 55555

nickname = input("Escolha um apelido: ")

# Conecta ao servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Função para receber mensagens do servidor
def receive():
    while True:
        try:
            message = client.recv(1024).decode('UTF-8')
            if message == 'NICK':
                client.send(nickname.encode('UTF-8'))
            else: 
                print(message)
        except:
            print("Erro ao receber mensagem.")
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('UTF-8'))

# Thread para receber mensagens
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()