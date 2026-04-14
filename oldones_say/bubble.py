import textwrap
from .colors import GOLD, GREY, LGREY, WHITE, BOLD, RESET, DGOLD

MAX_WIDTH = 60


def _visible_len(s):
    """Length of string ignoring ANSI escape codes."""
    import re
    return len(re.sub(r'\033\[[0-9;]*m', '', s))


def make_bubble(message: str, god_name: str, card_width: int = 51) -> str:
    """Render an eldritch speech bubble above the tarot card."""
    wrap_width = max(card_width - 4, 40)
    lines = []
    for paragraph in message.split('\n'):
        lines.extend(textwrap.wrap(paragraph, wrap_width) or [''])

    inner_width = max((_visible_len(l) for l in lines), default=1)
    inner_width = max(inner_width, card_width - 4)

    top    = f'{GOLD}{BOLD}╭{"─" * (inner_width + 2)}╮{RESET}'
    bottom = f'{GOLD}{BOLD}╰{"─" * (inner_width + 2)}╯{RESET}'

    rows = [top]
    for line in lines:
        pad = inner_width - _visible_len(line)
        rows.append(f'{GOLD}{BOLD}│{RESET} {LGREY}{line}{RESET}{" " * pad} {GOLD}{BOLD}│{RESET}')
    rows.append(bottom)

    # Connector pointing down-right toward the card's top-left
    offset = ' ' * 4
    rows.append(f'{DGOLD}{offset} ╲{RESET}')
    rows.append(f'{DGOLD}{offset}  ╲{RESET}')

    return '\n'.join(rows)
