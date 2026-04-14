from importlib import import_module
from importlib.resources import files
import re

from ..colors import RESET

UPPER = '\u2580'
LOWER = '\u2584'
FULL = '\u2588'
ALPHA_THRESHOLD = 32
DEFAULT_IMAGE_WIDTH = 58
ANSI_RE = re.compile(r'\033\[[0-9;]*m')

_MODULES = {
    'azathoth': 'azathoth',
    'cthulhu': 'cthulhu',
    'dagon': 'dagon',
    'hastur': 'hastur',
    'nyarlathotep': 'nyarlathotep',
    'shub-niggurath': 'shub_niggurath',
    'yog-sothoth': 'yog_sothoth',
}


def _fg(n):
    return f'\033[38;5;{n}m'


def _bg(n):
    return f'\033[48;5;{n}m'


def _normalize(rows):
    width = max(len(row) for row in rows) if rows else 0
    return [row.ljust(width, '.') for row in rows]


def _visible_len(text):
    return len(ANSI_RE.sub('', text))


def _center_line(text, width):
    visible = _visible_len(text)
    if visible >= width:
        return text
    padding = (width - visible) // 2
    return (' ' * padding) + text


def _ansi_256_to_rgb(index):
    base = (
        (0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0),
        (0, 0, 128), (128, 0, 128), (0, 128, 128), (192, 192, 192),
        (128, 128, 128), (255, 0, 0), (0, 255, 0), (255, 255, 0),
        (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255),
    )
    if 0 <= index < 16:
        return base[index]
    if 16 <= index <= 231:
        value = index - 16
        r = value // 36
        g = (value % 36) // 6
        b = value % 6
        steps = (0, 95, 135, 175, 215, 255)
        return (steps[r], steps[g], steps[b])
    if 232 <= index <= 255:
        gray = 8 + (index - 232) * 10
        return (gray, gray, gray)
    return (255, 255, 255)


def render_pixels(rows, palette):
    rows = _normalize(rows)
    if len(rows) % 2:
        rows.append('.' * len(rows[0]))
    output = []
    for index in range(0, len(rows), 2):
        top_row = rows[index]
        bottom_row = rows[index + 1]
        line = []
        for column in range(len(top_row)):
            top_color = palette.get(top_row[column])
            bottom_color = palette.get(bottom_row[column])
            if top_color is None and bottom_color is None:
                line.append(' ')
            elif top_color is not None and bottom_color is None:
                line.append(f'{_fg(top_color)}{UPPER}{RESET}')
            elif top_color is None and bottom_color is not None:
                line.append(f'{_fg(bottom_color)}{LOWER}{RESET}')
            elif top_color == bottom_color:
                line.append(f'{_fg(top_color)}{FULL}{RESET}')
            else:
                line.append(f'{_fg(top_color)}{_bg(bottom_color)}{UPPER}{RESET}')
        output.append(''.join(line))
    return output


def _normalize_image_pixel(rgba, tint=None):
    if rgba is None:
        return None

    r, g, b, a = rgba
    if a < ALPHA_THRESHOLD:
        return None

    # Keep small eye details legible after downscaling by snapping strong reds
    # to a cleaner terminal red.
    if a > 160 and r > 200 and g < 80 and b < 80:
        return (255, 0, 0, a)

    if tint is not None:
        # Preserve black outlines and other very dark edge pixels so per-god
        # tinting shifts the body colors without washing out the silhouette.
        if max(r, g, b) <= 40:
            return (r, g, b, a)
        tr, tg, tb, strength = tint
        r = round(r + (tr - r) * strength)
        g = round(g + (tg - g) * strength)
        b = round(b + (tb - b) * strength)

    return (r, g, b, a)


def _render_truecolor_half_block(top_rgba, bottom_rgba, tint=None):
    top_rgba = _normalize_image_pixel(top_rgba, tint=tint)
    bottom_rgba = _normalize_image_pixel(bottom_rgba, tint=tint)
    top_alpha = top_rgba[3] if top_rgba else 0
    bottom_alpha = bottom_rgba[3] if bottom_rgba else 0

    if top_alpha == 0 and bottom_alpha == 0:
        return ' '

    if top_alpha and not bottom_alpha:
        r, g, b, _ = top_rgba
        return f'\033[38;2;{r};{g};{b}m{UPPER}{RESET}'

    if bottom_alpha and not top_alpha:
        r, g, b, _ = bottom_rgba
        return f'\033[38;2;{r};{g};{b}m{LOWER}{RESET}'

    top_rgb = top_rgba[:3]
    bottom_rgb = bottom_rgba[:3]
    if top_rgb == bottom_rgb:
        r, g, b = top_rgb
        return f'\033[38;2;{r};{g};{b}m{FULL}{RESET}'

    tr, tg, tb = top_rgb
    br, bg, bb = bottom_rgb
    return (
        f'\033[38;2;{tr};{tg};{tb}m'
        f'\033[48;2;{br};{bg};{bb}m'
        f'{UPPER}{RESET}'
    )


def render_image(asset_name, max_width=DEFAULT_IMAGE_WIDTH, tint=None):
    try:
        from PIL import Image
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            'Image-backed god rendering requires Pillow. '
            'Install project dependencies before running oldonesay.'
        ) from exc

    asset_path = files(__name__).joinpath(asset_name)
    with Image.open(asset_path) as image:
        image = image.convert('RGBA')
        alpha = image.getchannel('A')
        mask = alpha.point(lambda a: 255 if a >= ALPHA_THRESHOLD else 0)
        bbox = mask.getbbox()
        if bbox:
            image = image.crop(bbox)

        width, height = image.size
        if width == 0 or height == 0:
            return ''

        target_width = min(width, max_width)
        target_height = max(2, round(height * (target_width / width)))
        if target_height % 2:
            target_height += 1

        image = image.resize((target_width, target_height), Image.Resampling.NEAREST)

        output = []
        for y in range(0, target_height, 2):
            line = []
            for x in range(target_width):
                top_rgba = image.getpixel((x, y))
                bottom_rgba = image.getpixel((x, y + 1))
                line.append(_render_truecolor_half_block(top_rgba, bottom_rgba, tint=tint))
            output.append(''.join(line))
        return '\n'.join(output)


def _load_god(slug):
    module = import_module(f'.{_MODULES[slug]}', __name__)
    god = {
        'name': module.NAME,
        'color': module.COLOR,
        'epithet': module.EPITHET,
    }
    if hasattr(module, 'ASSET_FILE'):
        god['asset_file'] = module.ASSET_FILE
        if hasattr(module, 'IMAGE_TINT'):
            god['image_tint'] = module.IMAGE_TINT
        if hasattr(module, 'IMAGE_TINT_STRENGTH'):
            god['image_tint_strength'] = module.IMAGE_TINT_STRENGTH
    else:
        god['art'] = module.ART
        god['palette'] = module.PAL
    return god


GODS = {slug: _load_god(slug) for slug in sorted(_MODULES)}


def get_god(name):
    god = GODS[name].copy()
    if 'asset_file' in god:
        tint = None
        if 'image_tint' in god:
            tint = (*_ansi_256_to_rgb(god['image_tint']), god.get('image_tint_strength', 0.0))
        god['rendered'] = render_image(god['asset_file'], tint=tint)
    else:
        pixel_lines = render_pixels(god['art'], god['palette'])
        god['rendered'] = '\n'.join(pixel_lines)

    art_width = max(
        (_visible_len(line) for line in god['rendered'].splitlines()),
        default=0,
    )
    color = god['color']
    name_line = f"\033[1m\033[38;5;{color}m{god['name'].upper()}\033[0m"
    epithet_line = f"\033[2m\033[38;5;244m{god['epithet']}\033[0m"
    god['nameplate'] = '\n'.join([
        '',
        _center_line(name_line, art_width),
        _center_line(epithet_line, art_width),
    ])
    return god
