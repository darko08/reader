"""lexicon.py — part-of-speech tags used by the score (shared by reader.py and reader8.py).

Tags: P pronoun subject, N noun (can be a subject), V verb, X auxiliary (is was were will),
      M modifier that may sit between subject and verb (not never always still again then who),
      J adjective/adverb (may close a sentence), C connective (a function word that must not end a reading).
A word may carry several tags. 'quiet' carries none.
"""
def _t(tag, s):
    return {w: tag for w in s.split()}

TAGS = {}
def add(tag, s):
    for w in s.split():
        TAGS.setdefault(w, set()).add(tag)

# --- function words -------------------------------------------------------
add("C", "the a an of and to in not who from with no if but or as by what where when your my our his her their "
         "between under over through after before into toward past beyond behind above across inside so until "
         "while because till yet though since once whereas every all this that than nor upon onto")
add("X", "is was were will")
add("M", "not never always still again then who")
add("P", "i we you it they she he us me")

# --- adverbs / adjectives that can close a sentence ----------------------
add("J", "never always again here there below beneath away back down still now only once then home alone together "
         "cold deep dead heavy empty hollow asleep old new long slow dark static deeper last first half none many "
         "forever twice slowly silent awake late early whole lost found drowned starved open closed bare blind "
         "far near low soft wet dry deaf mute numb nothing everything ever too below quiet")

# --- verbs -----------------------------------------------------------------
add("V", "drift drown sink float swim sleep wake burn open close give take go come wait remember forget fall rise "
         "dig carry keep lose find hold hear see speak write break mend seal follow return leave stay hide watch "
         "dream knock listen bury drink answer call name lie cry fear mark sign flood rain kept lost found held sank "
         "drowned starved waiting whisper imprint echo promise starve "
         # past tense, used by reader8
         "woke slept fell rose dug carried broke mended sealed followed returned left stayed hid watched dreamed "
         "knocked listened buried drank opened closed gave took went came waited remembered forgot called named "
         "answered spoke wrote heard saw burned swam floated drifted sang prayed lied promised counted wept cried "
         "begged breathed choked froze shook bled turned carved whispered owed sank knelt climbed descended asked "
         "kept begged hungered dimmed rusted wore loved feared hoped lit lit sold stole sent "
         "tasted touched hummed sighed slipped tore bound nailed drew emptied filled marked signed swore")

# --- nouns (anything that can stand as a subject or an object) ------------
add("N", "salt tide sea wave current undertow brine flood well rain ice mist foam silt reef shore harbor anchor rope "
         "net keel hull pressure breath hand eye mouth hunger bone sleep blood heart skin tooth throat lung spine skull "
         "tongue ear finger child mother father hollow body face shoulder weight pulse lamp dark ember glass shadow "
         "fire smoke ash spark candle moon star dawn dusk night morning lantern mirror gold one two three nine ten "
         "answer call name key word silence promise lie song prayer secret letter story question echo voice cry oath "
         "debt law stone layer door wreck surface bottom wall gate room bridge tower stair cave mine shaft chamber vault "
         "grave garden dream maker reader diver probe tender vow mark sign chronicle static whisper imprint fear greed "
         "tenth drowned starved ghost year hour day winter home chain light iron mercy rust "
         # reader8 extras
         "stranger keeper sleeper miner sailor widow daughter son brother sister elder pilot warden bell water wind frost "
         "memory depth seabed trench pit cellar basin threshold well church field city road window floor house "
         "dust bread coin ring thread cloth nail wax oil ink map rope bed cradle coffin boat ship wheel hook knife "
         "feather shell pearl coral eel crab whale gull rib heel knee hair veil")
