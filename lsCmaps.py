# write a scripts that gets a font file name from the command line and prints the cmap encoding records
from fontTools.ttLib import TTFont
from fontTools.ttLib import TTCollection
import sys

f=TTFont(sys.argv[1])

cmaps = [(table.platformID, table.platEncID, table.format) for table in f['cmap'].tables]

platforms = ("Unicode", "Macintosh", "ISO", "Windows", "Custom")
encodings = (
                # Unicode encodings:
                (   "1.0 semantics", 
                    "1.1 semantics", 
                    "ISO/IEC 10646 semantics",
                    "2.0 BMP semantics",
                    "2.0 full repertoire semantics", 
                    "Variation Sequences",
                    "Full Unicode coverage semantics"
                ),

                # Macintosh encodings:
                (   "Roman", "Japanese", "Chinese (Traditional)", "Korean",
                    "Arabic", "Hebrew", "Greek", "Russian", "RSymbol", "Devanagari",
                    "Gurmukhi", "Gujarati", "Oryia", "Bengali", "Tamil", "Telugu",
                    "Kannada", "Malayalam", "Sinhalese", "Burmese", "Khmer",
                    "Thai", "Laotian", "Georgian", "Armenian", "Simplified Chinese",
                    "Tibetan", "Mongolian", "Geez", "Slavic", "Vietnamese", "Sindhi",
                    "Uninterpreted"
                ),

                # ISO encodings:
                (   "7-bit ASCII", "10646", "8859-1" ),

                # Windows encodings:
                (   "Symbol", "Unicode BMP (UCS-2)", "ShiftJIS", "PRC", "Big 5",
                    "Wansung", "Johab", "Reserved", "Reserved", "Unicode UCS-4"
                )
            )
             
print("\ncmap subtables:\n")

for cmap in cmaps:
    if cmap[0] < 4:
        p = platforms[cmap[0]]
        if cmap[1] < len(encodings[cmap[0]]):
            e = encodings[cmap[0]][cmap[1]]
        else:
            e = "unknown encoding"
        print(f"{cmap[0]}/{cmap[1]}/{cmap[2]} ({p}, {e}, format {cmap[2]})")
    else:
        print(cmap)
        