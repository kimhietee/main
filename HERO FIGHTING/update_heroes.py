import os
import glob
import re

hero_codes_path = r'f:\NEW PYTHON KIMHIETEE\Game\my-game-kimhietee\Game\HERO FIGHTING\hero_codes'
files = glob.glob(os.path.join(hero_codes_path, '*.py'))

import_stmt = 'from path_helper import resource_path\n'

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if needs modification
    if 'pygame.mixer.Sound' in content and 'resource_path(' not in content:
        # Add import after import pygame
        if 'import pygame' in content and import_stmt not in content:
            content = content.replace('import pygame', f'import pygame\n{import_stmt}', 1)

        def repl(match):
            path_str = match.group(1)
            clean_path = path_str.replace('\\\\', '/').replace('\\', '/')
            return f'pygame.mixer.Sound(resource_path(\'{clean_path}\'))'

        new_content = re.sub(r'pygame\.mixer\.Sound\(\s*r?[\'\"]([^\'\"]+)[\'\"]\s*\)', repl, content)

        if content != new_content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated {os.path.basename(fpath)}')
