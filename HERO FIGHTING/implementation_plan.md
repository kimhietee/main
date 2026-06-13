# Implementation Plan — YOMIH Style LAN Multiplayer Lobby & Server Browser

The objective is to fix network teardown/disconnect bugs, prevent "host can join host" conflicts, and overhaul the multiplayer landing page into a sleek "Your Only Move Is Hustle" style lobby browser with local network discovery.

---

## Proposed Changes

### 1. Networking Teardown & Discovery

#### [MODIFY] [net_server.py](file:///d:/Game/HERO%20FIGHTING/net_server.py)
- Implement `stop_server()` to cleanly close the main server listener socket and all active client sockets, resetting `_server_thread` and `clients`.
- Implement background UDP broadcasting. When the server is active, it broadcasts its presence (`HERO_FIGHTING_LOBBY:<ip>:5555`) to the subnet on UDP port 5556 every 1.5 seconds.
- Update `start_background_server()` and `stop_server()` to start and stop this UDP broadcaster thread.

#### [MODIFY] [net_client.py](file:///d:/Game/HERO%20FIGHTING/net_client.py)
- Implement UDP scanning/discovery functions:
  - `start_lan_scanning()`: Spawns a background UDP listener on port 5556 to record incoming broadcasts.
  - `stop_lan_scanning()`: Cleanly shuts down the listener thread.
  - `get_active_servers()`: Returns a dictionary of active LAN lobbies `{ip: name}` and automatically purges any lobby not heard from in 5 seconds.

---

### 2. UI Overhaul (YOMIH Style Lobby Menu)

#### [MODIFY] [heroes.py](file:///d:/Game/HERO%20FIGHTING/heroes.py)
- Replace the legacy text-based `multiplayer_menu()` with a modern, image-button-driven **Multiplayer Lobby screen**:
  - Left panel: Displays a list of active LAN lobbies discovered via UDP scanning. Lobbies are shown as buttons that players can click to join. If none are found, shows "Scanning for LAN lobbies...".
  - Right panel:
    - **Host Game** (Image Button + Label): Launches a local server and puts the host in a dedicated wait screen.
    - **Direct Connect** (Image Button + Label): Opens a text-input box to type a custom IP.
    - **Local PvP** (Image Button + Label): Launches the local offline 2-player mode.
    - **Back** (Image Button + Label): Closes scanning and returns to the Main Menu.
- Implement a modern **Lobby Host Screen**:
  - Displayed to the host while waiting for Player 2.
  - Shows "Hosting Game", "Your LAN IP: <IP>", "Waiting for opponent to join..." with a spinning loading indicator or bouncing dots.
  - A big, clearly labeled "Cancel Hosting" Image Button that shuts down the server.
- Implement a helper `cleanup_networking()` function that disconnects `active_net_client` and stops the local server, calling it before hosting, joining, or when exiting back to the main menu.

#### [MODIFY] [gameloop.py](file:///d:/Game/HERO%20FIGHTING/gameloop.py)
- Route the main menu's `multiplayer_button` click handler to call `main.multiplayer_menu()` (Network Lobby) instead of starting offline PvP directly.
- Ensure that whenever a player returns to the main menu or disconnects, `cleanup_networking()` is called.

---

## Verification Plan

### Automated Tests
We will execute python syntax checks on the modified files to ensure there are no compilation errors:
```powershell
python -m py_compile "d:\Game\HERO FIGHTING\net_server.py"
python -m py_compile "d:\Game\HERO FIGHTING\net_client.py"
python -m py_compile "d:\Game\HERO FIGHTING\heroes.py"
python -m py_compile "d:\Game\HERO FIGHTING\gameloop.py"
```

### Manual Verification
1. **Lobby Scanning**: Open two instances. Click "Multiplayer" -> "Host Game" on one. On the other, click "Multiplayer" and verify that the first instance's lobby appears in the server browser list.
2. **Teardown**: Cancel hosting and check that port 5555 is freed and the other client is notified/handles disconnection gracefully.
3. **No Dual Hosting**: Verify that clicking Host Game while already connected/hosting performs a clean shutdown first.
