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
next_slot = [1]

# ── Phase 2: lobby state ──
lobby = {
    'map': None,          # chosen by host (player 1)
    'p1_hero': None,      # hero name confirmed by p1
    'p2_hero': None,      # hero name confirmed by p2
    'p1_ready': False,
    'p2_ready': False,
    'p1_load_ready': False, # check if p1 loads the p2 successfully
    'p2_load_ready': False
}

# ── Phase 2: cube position authority ──
cube_states = [
    {'fall': -500, 'x': 640},   # health cube
    {'fall': -300, 'x': 640},   # mana cube
    {'fall': -700, 'x': 640},   # special cube
]

def broadcast(msg):
    # print(f"[SERVER] Broadcasting: {msg['type']} to {list(clients.keys())} players")
    for sock in list(clients.values()):
        try: send_msg(sock, msg)
        except: pass

def handle_client(conn, player_type):
    print(f"[SERVER] Player {player_type} connected.")
    print(f"[SERVER] clients now: {list(clients.keys())}")
    try:
        while True:
            msg = recv_msg(conn)
            if msg is None:
                break


            message_type = msg.get('type')
            # print(f"[SERVER] Received '{message_type}' from Player {player_type}")
            if message_type == 'input':
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


            # ── Phase 2: lobby messages ──
            elif message_type == 'set_map':
                lobby['map'] = msg['map']
                broadcast({'type': 'map_set', 'map': msg['map']})
            elif message_type == 'hero_ready':
                lobby[f'p{player_type}_hero'] = msg['hero']
                lobby[f'p{player_type}_ready'] = True
                broadcast({'type': 'hero_confirmed', 'player': player_type, 'hero': msg['hero']})                
                if lobby['p1_ready'] and lobby['p2_ready']:
                    broadcast({'type': 'both_ready',
                               'p1_hero': lobby['p1_hero'],
                               'p2_hero': lobby['p2_hero'],
                               'map': lobby['map']})
                    lobby['p1_ready'] = False
                    lobby['p2_ready'] = False

            elif message_type == 'load_opponent_hero':
                lobby[f'p{player_type}_load_ready'] = True
                if lobby['p1_load_ready'] and lobby['p2_load_ready']:
                    broadcast({'type': 'ready_to_battle'})
                    lobby['p1_load_ready'] = False
                    lobby['p2_load_ready'] = False
                
            elif message_type == 'cube_reset':
                idx = msg['index']
                cube_states[idx]['fall'] = msg['fall']
                cube_states[idx]['x'] = msg['x']
                broadcast({'type': 'cube_update', 'index': idx, 'fall': msg['fall'], 'x': msg['x']})
    except (ConnectionResetError, ConnectionAbortedError):
        print('[SERVER] Connection error!')
    finally:
        with lock:
            clients.pop(player_type, None)
            print(f"[SERVER] Player {player_type} disconnected.")
            print(f"[SERVER] clients now: {list(clients.keys())}")
            # Reset slot counter if both disconnected
            if len(clients) == 0:
                next_slot[0] = 1
                print(f"[SERVER] All disconnected. Resetting slots.")
        conn.close()
        for pt, sock in clients.items():
            try:
                send_msg(sock, {'type': 'opponent_left'})
            except:
                pass

def accept_loop():
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
        thread = threading.Thread(target=handle_client, args=(conn, pt), daemon=True)
        thread.start()
        if len(clients) == 2:
            broadcast({'type': 'start'})
            print("[SERVER] Both players connected. Game starting.")
            # Don't reset next_slot here — wait for disconnects

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
