import socket
import threading


clients = set()
lock = threading.Lock()

def handle_client(client_socket):
    """Обработка сообщений от конкретного клиента."""
    global clients
    with lock:
        clients.add(client_socket)
    try:
        while True:
            message = client_socket.recv(2048).decode()  # Получение сообщения от клиента
            NUser = client_socket
            if not message:
                break
            broadcast_message(NUser,message)  # Рассылаем сообщение всем клиентам
    except Exception as e:
        pass
    finally:
        with lock:
            clients.remove(client_socket)
        client_socket.close()

def broadcast_message(NUser,message):
    """Рассылка сообщения всем подключенным клиентам."""
    for client in clients:
        try:
            if NUser == client:
                continue
            else:
                client.sendall((f"{message}\n").encode())  # Добавление новой строки для удобства отображения
        except BrokenPipeError:
            continue  # Игнорируем ошибки, если клиент отключился

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('0.0.0.0', 10000)
    server_socket.bind(server_address)
    server_socket.listen()

    print("Сервер запущен и ожидает подключения...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Принято новое подключение от: {client_address}")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    main()
    
