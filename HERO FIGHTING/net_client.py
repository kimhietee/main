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
        self.p1_hero_ready = False
        self.p2_hero_ready = False
        self.both_ready = False
        self.opponent_ready = False
        self.ready_to_battle = False
        # ── Phase 2: cube sync ──
        self.cube_updates = []   # list of pending cube updates: {'index':i,'fall':f,'x':x}
        self._cube_lock = threading.Lock()
        self.opponent_left = False
        self.cube_seed = None   # shared seed for deterministic initial cube X positions
        self.declared_winner = None  # set by server in LAN mode

        self.my_rematch_sent = False
        self.opponent_rematch_sent = False
        self.rematch_confirmed = False

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

    def send_load_opponent_hero_ready(self, hero_name):
        send_msg(self.sock, {'type': 'load_opponent_hero', 'hero': hero_name})

    def send_cube_reset(self, index, fall, x, hero_hit=None, bonus_type=None, bonus_amount=None):
        if self.sock and self._running:
            try:
                send_msg(self.sock, {
                    'type': 'cube_reset', 'index': index, 'fall': fall, 'x': x,
                    'hero_hit': hero_hit, 'bonus_type': bonus_type, 'bonus_amount': bonus_amount
                })
            except:
                self._running = False
                self.phase = 'disconnected'

    def send_report_hp(self, p1_hp, p2_hp):
        send_msg(self.sock, {'type': 'report_hp', 'p1_hp': p1_hp, 'p2_hp': p2_hp})

    def send_rematch_request(self):
        self.my_rematch_sent = True
        send_msg(self.sock, {'type': 'rematch_request'})

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
            # print(message_type)

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
            elif message_type == 'hero_confirmed': # not used????
                if msg['player'] != self.my_player_type:
                    self.opponent_ready = True
                    print('opponent ready :)')

            elif message_type == 'both_ready':
                self.p1_hero = msg['p1_hero']
                self.p2_hero = msg['p2_hero']
                self.map_selected = msg['map']
                print('both ready :)')
                self.both_ready = True

            # elif message_type == 'not_ready':
            #     self.both_ready = False
            #     print('not ready :)')

            elif message_type == 'ready_to_battle':
                print('ready to battle!!!')
                self.cube_seed = msg.get('cube_seed')  # store shared seed for cube sync
                self.ready_to_battle = True

            elif message_type == 'cube_update':
                with self._cube_lock:
                    self.cube_updates.append({
                        'index': msg['index'],
                        'fall': msg['fall'],
                        'x': msg['x'],
                        'hero_hit': msg.get('hero_hit'),
                        'bonus_type': msg.get('bonus_type'),
                        'bonus_amount': msg.get('bonus_amount'),
                    })

            elif message_type == 'winner_declared':
                self.declared_winner = msg['winner']

            elif message_type == 'rematch_request_received':
                if msg['player'] != self.my_player_type:
                    self.opponent_rematch_sent = True

            elif message_type == 'rematch_confirmed':
                self.rematch_confirmed = True

    def send_disconnect(self, hero_name):
        send_msg(self.sock, {'type': 'disconnected'})

    def disconnect(self):
        self._running = False
        if self.sock:
            self.sock.close()
