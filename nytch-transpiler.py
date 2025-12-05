import json
import emoji
import re
from pathlib import Path

# --- Load NYCH glyph lexicon ---
GLYPH_PATH = Path('docs/nych_glyphs.json')
with GLYPH_PATH.open('r', encoding='utf-8') as f:
    NYCH_GLYPHS = json.load(f)

# --- Load Unicode standard emoji map (or build one as needed) ---
def build_standard_emoji_map():
    # Build a dict {word: emoji} using standard emoji library
    # This is a stub: you would use a robust emoji NLP library or database here
    # Use emoji.EMOJI_DATA for full mapping, or pull from your own curated file
    standard_map = {}
    for e, data in emoji.EMOJI_DATA.items():
        desc = data.get('en', '').lower()
        for word in desc.split():
            if word not in standard_map:
                standard_map[word] = e
    return standard_map

STANDARD_EMOJI_MAP = build_standard_emoji_map()

# --- Build NYCH mapping from your lexicon ---
NYCH_WORD_MAP = {}
for category, mapping in NYCH_GLYPHS.items():
    for k, v in mapping.items():
        if isinstance(v, list):
            for symbol in v:
                NYCH_WORD_MAP[k.lower()] = symbol
        else:
            NYCH_WORD_MAP[k.lower()] = v

# --- Main Transpiler ---
class NYCHTranspiler:
    def __init__(self, nych_map, std_emoji_map):
        self.nych_map = nych_map
        self.std_emoji_map = std_emoji_map

    def human_to_nych(self, sentence, container="ai_human_interface"):
        """Map human sentence to NYCH emoji string using your lexicon. Fall back to Unicode emoji if needed."""
        words = re.findall(r'\w+|\S', sentence.lower())
        output = []
        for word in words:
            if word in self.nych_map:
                output.append(self.nych_map[word])
            elif word in self.std_emoji_map:
                output.append(self.std_emoji_map[word])
            else:
                output.append(word)  # Keep as-is or log for review
        return ''.join(output)

    def is_lossless(self, sentence, container="ai_human_interface"):
        """Check if all words mapped 1-1 to NYCH assignments (no fallback to generic emoji or text)."""
        words = re.findall(r'\w+|\S', sentence.lower())
        for word in words:
            if word not in self.nych_map:
                return False
        return True

    def compress(self, sentence, container="ai_human_interface"):
        """Try NYCH-only. If not lossless, fall back to Unicode emoji and issue warning."""
        nych_seq = self.human_to_nych(sentence, container)
        if self.is_lossless(sentence, container):
            print("Compression: lossless for NYCH container.")
            return nych_seq
        else:
            print("Compression: fallback used, not all words matched NYCH lexicon.")
            return nych_seq

# --- Usage Example ---
if __name__ == "__main__":
    transpiler = NYCHTranspiler(NYCH_WORD_MAP, STANDARD_EMOJI_MAP)
    print("Type a human instruction to see its NYCH/emoji mapping:")
    while True:
        instr = input("> ")
        if instr.strip().lower() in {'quit', 'exit'}:
            break
        compressed = transpiler.compress(instr)
        print(compressed)
