import random

QUOTES = {
    "cthulhu": [
        "In his house at R'lyeh, dead Cthulhu waits dreaming.",
        "That is not dead which can eternal lie, and with strange aeons even death may die.",
        "Ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn.",
        "The most merciful thing in the world is the inability of the human mind to correlate all its contents.",
        "We live on a placid island of ignorance in the midst of black seas of infinity.",
    ],
    "nyarlathotep": [
        "I am the Crawling Chaos. I am the last. I will tell the audient void.",
        "Nyarlathotep... the crawling chaos... I am the last... I will tell the audient void.",
        "The dreams and fancies of fallen houses, and of strange, sinister forms that lurk in high, distant places.",
        "Wildly dressed, squint-eyed half-castes and unstable creatures who drift and dream.",
        "He was of no particular race, and yet he was of all races.",
        "I remember the night I saw Nyarlathotep... the tall, swarthy man who spoke of such terrifying things.",
    ],
    "azathoth": [
        "Outside the ordered universe is that amorphous blight of nethermost confusion which blasphemes and bubbles at the center of all infinity.",
        "The blind idiot god Azathoth, Lord of All Things, encircled by his flopping horde of mindless and amorphous dancers.",
        "Azathoth, that last amorphous blight of nethermost confusion where bubbles and blasphemes at infinity's center the mindless daemon sultan.",
        "All matter and energy vibrated to the mad piping of that hideous flute.",
        "At the center of ultimate chaos, the daemon sultan Azathoth gnaws hungrily in inconceivable, unlighted chambers beyond time.",
    ],
    "yog-sothoth": [
        "Yog-Sothoth knows the gate. Yog-Sothoth is the gate. Yog-Sothoth is the key and guardian of the gate.",
        "Past, present, future — all are one in Yog-Sothoth.",
        "He knows where the Old Ones broke through of old, and where They shall break through again.",
        "The Old Ones were, the Old Ones are, and the Old Ones shall be. Not in the spaces we know, but between them.",
        "Yog-Sothoth knows the sign by which the spheres are counted and the vault opened.",
    ],
    "hastur": [
        "The King in Yellow shall rule where He will and no law shall bind him.",
        "You have looked upon Hastur. None who look upon the King may live.",
        "Strange is the night where black stars rise, and strange moons circle through the skies.",
        "Along the shore the cloud waves break, the twin suns sink behind the lake.",
        "It is a fearful thing to fall into the hands of the living god.",
        "Camilla: You, sir, should unmask. Stranger: Indeed? Cassilda: Indeed it's time. We all have laid aside disguise but you.",
    ],
    "shub-niggurath": [
        "Iä! Shub-Niggurath! The Black Goat of the Woods with a Thousand Young!",
        "The thousand young of Shub-Niggurath swarm across the angles of impossible space.",
        "She who dwells in the outer hells shall send her thousand young to devour the world.",
        "Iä! Iä! The Black Goat of the Woods! The dark mother feeds on the screaming stars!",
        "In the dark woods they gather, the Dark Young, the children of the Black Goat.",
        "She rules the outer chaos, the mother of abominations, the goat of a thousand young.",
    ],
    "dagon": [
        "I think their predominant colour was a greyish-green, though they had white bellies.",
        "The Deep Ones shall inherit the earth. In time even death shall die.",
        "Ph'nglui mglw'nafh Dagon deep below wgah'nagl fhtagn.",
        "They were not altogether crows, nor moles, nor buzzards, nor ants, nor vampire bats, nor decomposed human beings; but something I cannot and must not recall.",
        "In my dreams I saw great Dagon rise from the black sea, arms outstretched, calling to his kind.",
        "Iä! Iä! Dagon! Father of the deep! Rise from the abyss and reclaim the world!",
    ],
}


def get_quote(god_name: str) -> str:
    quotes = QUOTES.get(god_name, ["The void stares back."])
    return random.choice(quotes)
