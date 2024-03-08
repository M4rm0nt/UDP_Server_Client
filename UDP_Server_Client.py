import socket
import threading
import time


def run_server(host='127.0.0.1', port=9997):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        print(f"Echo-Server läuft auf {host}:{port}")

        while True:
            data, addr = server_socket.recvfrom(1024)
            print(f"Nachricht von {addr}: {data.decode()}")
            server_socket.sendto(data, addr)


def run_client(target_host='127.0.0.1', target_port=9997):
    time.sleep(1)  # Gib dem Server Zeit, sich zu initialisieren
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
            client.settimeout(5)  # Timeout nach 5 Sekunden

            message = b"AAABBBCCC"
            client.sendto(message, (target_host, target_port))

            try:
                data, addr = client.recvfrom(4096)
                print(f"Client empfängt: {data.decode()}")
            except socket.timeout:
                print("Zeitüberschreitung beim Warten auf eine Antwort vom Server.")

    except socket.error as e:
        print(f"Socket-Fehler: {e}")
    except Exception as e:
        print(f"Allgemeiner Fehler: {e}")


if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    client_thread = threading.Thread(target=run_client)
    client_thread.start()

    server_thread.join()
    client_thread.join()
