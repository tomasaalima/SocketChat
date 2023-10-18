import socket
import threading

# Configurações do servidor
HOST = '127.0.0.1'  # Ouvir em todas as interfaces
PORT = 55555

# Inicializa o servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Lista para armazenar clientes
clients = []
nicknames = []

# Função para transmitir mensagens para todos os clientes
def broadcast(message):
    for client in clients:
            client.send(message)

# Thread para lidar com cada cliente
def handle(client):
    while True:
        try:
            while True:
                message = client.recv(1024)
                broadcast(message)
        except:
            index =  clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} deixou a sala!'.encode('UTF-8'))
            nicknames.remove(nickname)
            break
    

# Aceita conexões de clientes
def receive():
    while True:
        client, address = server.accept()
        print(f"Conexão estabelecida com {str(address)}")

        client.send('NICK'.encode('UTF-8'))
        nickname = client.recv(1024).decode('UTF-8')
        nicknames.append(nickname)
        clients.append(client)
        
        print(f'O apelido desse usuário é {nickname}!')
        broadcast(f'{nickname} entrou na sala'.encode('UTF-8'))
        client.send('Conectado ao servidor!'.encode('UTF-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Servidor ouvindo...")
receive()