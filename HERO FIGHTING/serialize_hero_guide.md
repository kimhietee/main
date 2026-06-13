# serialize_hero — Complete Player State Scan & Network Sync Guide
457109
> [!NOTE]
> Based on a thorough scan of `player.py` (base `Player` class) and all 9 hero subclasses:
> Fire_Wizard, Wanderer_Magician, Fire_Knight, Wind_Hashashin, Water_Princess, Forest_Ranger, Yurei, Chthulu, Phantom_Assassin

---

## 1. What You're Currently Serializing (commit `a3d8f53`)

```python
# Current serialize_hero()
'health', 'mana', 'special', 'temp_hp',
'x', 'y', 'yv', 'jump', 'facing_right',
'frozen', 'rooted', 'slowed', 'silenced', 'stunned',
'hasted', 'flying', 'invisible',
'attacking1', 'attacking2', 'attacking3', 'attacking4', 'basic_attacking',
'enemy', 'immortality_activated', 'immortality_duration',
'skills_cd', 'special_skills_cd'
```

---

## 2. Every Player Variable — Full Breakdown

### 🔴 CRITICAL — Must Sync (causes desync if missing)

These change every frame or affect gameplay logic directly.

| Variable | Type | Info | Currently Synced? |
|---|---|---|---|
| `health` | float | Current HP, changes every frame from damage/regen | ✅ |
| `mana` | float | Current mana, changes from regen and skill usage | ✅ |
| `special` | float | Special meter (0 to MAX_SPECIAL) | ✅ |
| `temp_hp` | float | Temporary HP shield, absorbs damage first | ✅ |
| `x_pos` | float | Horizontal position — **changes every frame** | ✅ |
| `y_pos` | float | Vertical position — **changes every frame** (jumping/gravity) | ✅ |
| `y_velocity` | float | Vertical speed, changes with gravity/jumps | ✅ |
| `facing_right` | bool | Direction the hero faces — affects skill spawn direction | ✅ |
| `jumping` | bool | Whether hero is in the air | ✅ |
| `attacking1` | bool | Casting skill 1 | ✅ |
| `attacking2` | bool | Casting skill 2 | ✅ |
| `attacking3` | bool | Casting skill 3 | ✅ |
| `sp_attacking` | bool | Casting skill 4 (ult) | ✅ |
| `basic_attacking` | bool | Doing basic attack | ✅ |
| `special_active` | bool | Whether special mode is ON (changes skills, buffs) | ❌ **MISSING** |
| `running` | bool | Whether hero is running (movement animation) | ❌ **MISSING** |
| `speed` | float | Current move speed (can be buffed/debuffed) | ❌ **MISSING** |

### 🟡 IMPORTANT — Status Effects

| Variable | Type | Info | Currently Synced? |
|---|---|---|---|
| `frozen` | bool | Can't move or attack | ✅ |
| `freeze_source` | obj | Who froze them (for removal) | ❌ (complex, skip for now) |
| `rooted` | bool | Can't move but can attack | ✅ |
| `root_source` | obj | Who rooted them | ❌ (complex, skip for now) |
| `slowed` | bool | Move speed reduced | ✅ |
| `slow_source` | obj | Who slowed them | ❌ (complex, skip for now) |
| `slow_speed` | float | How much they're slowed (0–1) | ❌ **MISSING** |
| `speed_multiplier` | float | Movement speed multiplier from effects | ❌ **MISSING** |
| `silenced` | bool | Can't cast skills, only basic attack | ✅ |
| `stunned` | bool | Can't do anything | ✅ |
| `hasted` | bool/None | Move speed boosted (hero-specific) | ✅ (via getattr) |
| `flying` | bool/None | Airborne state (hero-specific) | ✅ (via getattr) |
| `invisible` | bool/None | Stealth state (hero-specific) | ✅ (via getattr) |
| `immortality_activated` | bool | Immortality item active | ✅ |
| `immortality_duration` | float | Time left on immortality | ✅ |

### 🟢 MODERATE — Skill Cooldowns

| Variable | Type | Info | Currently Synced? |
|---|---|---|---|
| `attacks[i].get_skill_cooldown()` | float | Remaining CD for each basic skill | ✅ |
| `attacks_special[i].get_skill_cooldown()` | float | Remaining CD for each special skill | ✅ |

> [!TIP]
> You're currently serializing cooldowns as dicts with index keys — this works. But `remaining_ms` on the P2 side is only cosmetic (for display). P2 doesn't need to track internal `_last_used_time` because the host runs all skill logic.

### 🔵 NICE TO HAVE — Display & Combat Modifiers

These don't cause hard desyncs but improve visual fidelity on P2's side.

| Variable | Type | Info | Currently Synced? |
|---|---|---|---|
| `max_health` | float | Max HP (for bar display) | ❌ |
| `max_mana` | float | Max mana (for bar display) | ❌ |
| `max_special` | float | Max special (usually constant) | ❌ |
| `max_temp_hp` | float | Max temp HP | ❌ |
| `basic_attack_damage` | float | Current basic atk damage (with items) | ❌ |
| `damage_reduce` | float | % damage reduction from items | ❌ |
| `damage_increase` | float | % extra damage taken | ❌ |
| `lifesteal` | float | Lifesteal % | ❌ |
| `crit_chance` | float | Crit chance % | ❌ |
| `crit_damage` | float | Crit damage multiplier | ❌ |
| `damage_return` | float | Damage reflected back | ❌ |
| `health_regen` | float | HP/frame regen rate | ❌ |
| `mana_regen` | float | Mana/frame regen rate | ❌ |

### ⚪ NO NEED — Static/Config (don't change during game)

These are set once at hero creation and never change during a match.

| Variable | Info |
|---|---|
| `player_type` | 1 or 2, fixed |
| `name` | Hero name, fixed |
| `strength`, `intelligence`, `agility` | Set at creation + items (doesn't change mid-fight) |
| `str_mult`, `int_mult`, `agi_mult` | Constants |
| `hitbox_rect` | Size is static per hero |
| `attacks[]` (the Attacks objects) | Structure is identical on both clients |
| `items[]` | Both clients select items during hero select |
| `skill_iframes_config` | Static config per hero |
| `limit_movement_left/right` | Constants |
| `jump_force` | Static per hero |
| All animation frames/sprites | Loaded locally |
| All sound effects | Loaded locally |

### ⚫ DO NOT SERIALIZE — Internal/Rendering Only

| Variable | Info |
|---|---|
| `player_*_index` | Animation frame indices — let P2 compute locally |
| `image`, `rect` | Pygame rendering objects — not serializable |
| `damage_numbers` | Floating text display — local only |
| `white_health_p1/p2`, `white_mana_p1/p2` | White bar chase — cosmetic, computed locally |
| `last_health`, `last_mana` | For damage detection display |
| `_net_keys` | Network input, separate system |
| Dash state (`dashing`, `dash_distance_covered`, etc.) | Computed from position changes |

---

## 3. ❌ What You're Missing (Priority Order)

### Must-fix (will cause visible desyncs):

1. **`special_active`** — P2 won't know when the hero enters special mode. Skills, damage, and animations will be completely wrong.
2. **`running`** — P2 hero might show idle animation while running.
3. **`speed`** — If speed is modified (by items, slow, special mode), P2 won't reflect it.
4. **`slow_speed`** — If a hero is slowed, P2 won't know the rate.

### Should-fix (for correct display):

5. **`max_health`** / **`max_mana`** — P2's health/mana bars won't scale correctly if items modify max values.

---

## 4. Recommended Updated `serialize_hero`

```python
def serialize_hero(h):
    """Snapshot the crucial, host-authoritative state of one hero."""
    return {
        # ── Core Resources ──
        'health': h.health,
        'mana': h.mana,
        'special': h.special,
        'temp_hp': h.temp_hp,
        'max_health': h.max_health,     # NEW: for bar display
        'max_mana': h.max_mana,         # NEW: for bar display

        # ── Position & Movement ──
        'x': h.x_pos,
        'y': h.y_pos,
        'yv': h.y_velocity,
        'jump': h.jumping,
        'facing_right': h.facing_right,
        'running': h.running,           # NEW: movement animation
        'speed': h.speed,               # NEW: current speed (with buffs/debuffs)

        # ── Status Effects ──
        'frozen': h.frozen,
        'rooted': h.rooted,
        'slowed': h.slowed,
        'slow_speed': h.slow_speed,     # NEW: slow rate
        'silenced': h.silenced,
        'stunned': h.stunned,
        'hasted': getattr(h, 'hasted', None),
        'flying': getattr(h, 'flying', None),
        'invisible': getattr(h, 'invisible', None),

        # ── Attacking States ──
        'attacking1': h.attacking1,
        'attacking2': h.attacking2,
        'attacking3': h.attacking3,
        'attacking4': h.sp_attacking,
        'basic_attacking': h.basic_attacking,
        'special_active': h.special_active,  # NEW: special mode toggle

        # ── Items/Abilities ──
        'immortality_activated': h.immortality_activated,
        'immortality_duration': h.immortality_duration,

        # ── Cooldowns ──
        'skills_cd': {i: skill.get_skill_cooldown() for i, skill in enumerate(h.attacks)},
        'special_skills_cd': {i: skill.get_skill_cooldown() for i, skill in enumerate(h.attacks_special)},
    }
```

> [!WARNING]
> **Remove `'enemy': h.enemy`** from serialize — `h.enemy` is a list of Player objects. Serializing pygame objects over the network will either crash or send garbage. The enemy reference is already set up on both clients during hero selection.

---

## 5. Recommended Updated `apply_hero_state`

```python
def apply_hero_state(h, s, x=None, y=None):
    if h is None or s is None:
        return

    # ── Core Resources ──
    h.health = s['health']
    h.mana = s['mana']
    h.special = s['special']
    h.temp_hp = s['temp_hp']
    h.max_health = s['max_health']
    h.max_mana = s['max_mana']

    # ── Position & Movement ──
    h.x_pos = s['x'] if x is None else x
    h.y_pos = s['y'] if y is None else y
    h.y_velocity = s['yv']
    h.jumping = s['jump']
    h.facing_right = s['facing_right']
    h.running = s['running']
    h.speed = s['speed']

    # ── Status Effects ──
    h.frozen = s['frozen']
    h.rooted = s['rooted']
    h.slowed = s['slowed']
    h.slow_speed = s['slow_speed']
    h.silenced = s['silenced']
    h.stunned = s['stunned']
    if hasattr(h, 'hasted'): h.hasted = s['hasted']
    if hasattr(h, 'flying'): h.flying = s['flying']
    if hasattr(h, 'invisible'): h.invisible = s['invisible']

    # ── Attacking States ──
    h.attacking1 = s['attacking1']
    h.attacking2 = s['attacking2']
    h.attacking3 = s['attacking3']
    h.sp_attacking = s['attacking4']
    h.basic_attacking = s['basic_attacking']
    h.special_active = s['special_active']

    # ── Items/Abilities ──
    h.immortality_activated = s['immortality_activated']
    h.immortality_duration = s['immortality_duration']

    # ── Cooldowns (display only on P2) ──
    for skill_idx, cd_time in s['skills_cd'].items():
        h.attacks[int(skill_idx)].remaining_ms = cd_time
    for skill_idx, cd_time in s['special_skills_cd'].items():
        h.attacks_special[int(skill_idx)].remaining_ms = cd_time
```

---

## 6. Step-by-Step Guide to Apply

### Step 1: Update `serialize_hero` in `gameloop.py` (~line 813)
Replace the current `serialize_hero` function with the one from Section 4 above.

**Key changes:**
- Add `special_active`, `running`, `speed`, `slow_speed`, `max_health`, `max_mana`
- **Remove** `'enemy': h.enemy` (can't serialize pygame objects)

### Step 2: Update `apply_hero_state` in `gameloop.py` (~line 833)
Replace the current `apply_hero_state` function with the one from Section 5 above.

**Key changes:**
- Add lines for `special_active`, `running`, `speed`, `slow_speed`, `max_health`, `max_mana`
- **Remove** the `h.enemy = s['enemy']` line

### Step 3: Verify `remaining_ms` is used in display
In `heroes.py`, make sure `draw_skill_icon` uses `self.remaining_ms` for P2's cooldown display (this is already done in your latest commit).

### Step 4: Test
1. Run a LAN game
2. On P2's screen, verify:
   - Hero switches to special mode visually when P1 activates it
   - Running animation plays when moving
   - Health/mana bars show correct max values
   - Slow effect visually slows the hero on P2's screen

> [!CAUTION]
> **Do NOT serialize**: `h.enemy`, `h.image`, `h.rect`, any `pygame.Surface`, any `pygame.Sound`, or animation frame lists. These are not JSON-serializable and will crash the network code.
