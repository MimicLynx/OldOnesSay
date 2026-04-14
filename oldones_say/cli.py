#!/usr/bin/env python3
"""
oldonesay — The Old Ones have something to say.

Usage:
  oldonesay                         # random god, canonical quote
  oldonesay "your message"          # random god speaks your words
  oldonesay -g cthulhu              # specific god, canonical quote
  oldonesay -g hastur "He stirs."   # specific god speaks your words
  oldonesay -l                      # list all entities
  echo "text" | oldonesay           # pipe input
"""
import argparse
import random
import sys

from .bubble import make_bubble
from .gods import GODS, get_god
from .quotes import get_quote


def main():
    parser = argparse.ArgumentParser(
        prog='oldonesay',
        description='The Old Ones have something to say.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        'message',
        nargs='*',
        help='Words for the entity to speak (defaults to a canonical quote)',
    )
    parser.add_argument(
        '-g', '--god',
        choices=sorted(GODS.keys()) + ['random'],
        default='random',
        metavar='GOD',
        help=(
            'Which entity speaks. Choices: '
            + ', '.join(sorted(GODS.keys()))
            + ', random (default)'
        ),
    )
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List all available entities and exit',
    )
    parser.add_argument(
        '-q', '--quote',
        action='store_true',
        help='Force a canonical quote even if a message is supplied',
    )

    args = parser.parse_args()

    if args.list:
        print()
        print('  The Old Ones who may speak:')
        print()
        for key, data in sorted(GODS.items()):
            print(f'    {key:<20}  {data["epithet"]}')
        print()
        return

    god_name = (
        args.god if args.god != 'random'
        else random.choice(list(GODS.keys()))
    )
    god = get_god(god_name)

    # Determine message
    if args.quote or not args.message and sys.stdin.isatty():
        message = get_quote(god_name)
    elif args.message:
        message = ' '.join(args.message)
    else:
        # Piped input
        message = sys.stdin.read().strip() or get_quote(god_name)

    bubble = make_bubble(message, god_name)

    print()
    print(bubble)
    print(god['rendered'])
    print(god['nameplate'])
    print()


if __name__ == '__main__':
    main()
