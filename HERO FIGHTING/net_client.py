import socket
import threading
from network import send_msg, recv_msg

class NetClient:
    """
    Manages the socket connection for one player.
    The game loop calls send_input() every frame.
    The latest inputs for both players are always available
    in self.p1_keys and self.p2_keys.
    """
    def __init__(self, host, port=5555):
        self.host = host
        self.port = port
        self.sock = None
        self.my_player_type = None
        self.phase = 'connecting'   # connecting -> lobby -> playing -> disconnected
        self.p1_keys = {}
        self.p2_keys = {}
        self._lock = threading.Lock()
        self._running = False
        # ── Phase 2: lobby state ──
        self.map_selected = None
        self.p1_hero = None
        self.p2_hero = None
        self.both_ready = False
        self.opponent_ready = False
        # ── Phase 2: cube sync ──
        self.cube_updates = []   # list of pending cube updates: {'index':i,'fall':f,'x':x}
        self._cube_lock = threading.Lock()
        self.opponent_left = False

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        welcome = recv_msg(self.sock)
        if welcome is None:
            raise ConnectionError("No welcome message from server.")
        self.my_player_type = welcome['your_player_type']
        self._running = True
        thread = threading.Thread(target=self._recv_loop, daemon=True)
        thread.start()
        print(f"[CLIENT] Connected as Player {self.my_player_type}")

    def send_input(self, keys: dict):
        """Call every frame with a dict of booleans for this player's keys."""
        if self.sock and self._running:
            try:
                send_msg(self.sock, {'type': 'input', 'keys': keys})
            except:
                self._running = False
                self.phase = 'disconnected'

    def get_inputs(self):
        """Returns (p1_keys, p2_keys) -- latest known inputs for both players."""
        with self._lock:
            return dict(self.p1_keys), dict(self.p2_keys)

    # ── Phase 2: lobby send methods ──
    def send_map(self, map_name):
        send_msg(self.sock, {'type': 'set_map', 'map': map_name})

    def send_hero_ready(self, hero_name):
        send_msg(self.sock, {'type': 'hero_ready', 'hero': hero_name})

    def send_cube_reset(self, index, fall, x):
        send_msg(self.sock, {'type': 'cube_reset', 'index': index, 'fall': fall, 'x': x})

    def pop_cube_updates(self):
        """Returns and clears pending cube updates."""
        with self._cube_lock:
            updates = list(self.cube_updates)
            self.cube_updates.clear()
            return updates

    def _recv_loop(self):
        while self._running:
            msg = recv_msg(self.sock)
            if msg is None:
                self.phase = 'disconnected'
                self._running = False
                break
            message_type = msg.get('type')
            if message_type == 'start':
                self.phase = 'lobby'
            elif message_type == 'inputs':
                with self._lock:
                    self.p1_keys = msg.get('p1', {})
                    self.p2_keys = msg.get('p2', {})
            elif message_type == 'opponent_left':
                if self._running:
                    self.phase = 'lobby'
                    self.opponent_left = True
            # ── Phase 2: lobby messages ──
            elif message_type == 'map_set':
                self.map_selected = msg['map']
            elif message_type == 'hero_confirmed':
                if msg['player'] != self.my_player_type:
                    self.opponent_ready = True
            elif message_type == 'both_ready':
                self.p1_hero = msg['p1_hero']
                self.p2_hero = msg['p2_hero']
                self.map_selected = msg['map']
                self.both_ready = True
            elif message_type == 'cube_update':
                with self._cube_lock:
                    self.cube_updates.append({
                        'index': msg['index'],
                        'fall': msg['fall'],
                        'x': msg['x']
                    })

    def send_disconnect(self, hero_name):
        send_msg(self.sock, {'type': 'disconnected'})

    def disconnect(self):
        self._running = False
        if self.sock:
            self.sock.close()
