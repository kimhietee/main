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

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        welcome = recv_msg(self.sock)
        if welcome is None:
            raise ConnectionError("No welcome message from server.")
        self.my_player_type = welcome['your_player_type']
        self._running = True
        t = threading.Thread(target=self._recv_loop, daemon=True)
        t.start()
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

    def _recv_loop(self):
        while self._running:
            msg = recv_msg(self.sock)
            if msg is None:
                self.phase = 'disconnected'
                self._running = False
                break
            t = msg.get('type')
            if t == 'start':
                self.phase = 'playing'
            elif t == 'inputs':
                with self._lock:
                    self.p1_keys = msg.get('p1', {})
                    self.p2_keys = msg.get('p2', {})
            elif t == 'opponent_left':
                self.phase = 'lobby'

    def disconnect(self):
        self._running = False
        if self.sock:
            self.sock.close()
