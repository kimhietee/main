import socket
import threading
import time
from network import send_msg, recv_msg

HOST = '0.0.0.0'
PORT = 5555

# Shared input state — server stores latest inputs from each player
player_inputs = {
    1: {'left': False, 'right': False, 'up': False,
        'skill1': False, 'skill2': False, 'skill3': False,
        'skill4': False, 'basic': False, 'special': False},
    2: {'left': False, 'right': False, 'up': False,
        'skill1': False, 'skill2': False, 'skill3': False,
        'skill4': False, 'basic': False, 'special': False},
}
clients = {}   # player_type (1 or 2) -> socket
lock = threading.Lock()

def broadcast(msg):
    for sock in list(clients.values()):
        try: send_msg(sock, msg)
        except: pass

def handle_client(conn, player_type):
    print(f"[SERVER] Player {player_type} connected.")
    try:
        while True:
            msg = recv_msg(conn)
            if msg is None:
                break
            if msg.get('type') == 'input':
                with lock:
                    player_inputs[player_type] = msg['keys']
                # Broadcast both players' latest inputs to everyone
                with lock:
                    state = {
                        'type': 'inputs',
                        'p1': dict(player_inputs[1]),
                        'p2': dict(player_inputs[2]),
                    }
                broadcast(state)
    except (ConnectionResetError, ConnectionAbortedError):
        pass
    finally:
        print(f"[SERVER] Player {player_type} disconnected.")
        with lock:
            clients.pop(player_type, None)
        conn.close()
        broadcast({'type': 'opponent_left'})

def accept_loop():
    next_slot = [1]
    while True:
        conn, addr = server.accept()
        pt = next_slot[0]
        if pt > 2:
            conn.close()
            continue
        next_slot[0] += 1
        with lock:
            clients[pt] = conn
        send_msg(conn, {'type': 'welcome', 'your_player_type': pt})
        t = threading.Thread(target=handle_client, args=(conn, pt), daemon=True)
        t.start()
        if len(clients) == 2:
            broadcast({'type': 'start'})
            print("[SERVER] Both players connected. Game starting.")
            next_slot[0] = 1   # reset for reconnects

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print(f"[SERVER] Listening on port {PORT}...")

try:
    accept_loop()
except KeyboardInterrupt:
    print("[SERVER] Shutting down.")
    server.close()
