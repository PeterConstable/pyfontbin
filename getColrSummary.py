# script that gets a font file name from the command line and prints some basic info about the COLR table
from fontTools.ttLib import TTFont
import sys

f=TTFont(sys.argv[1])

if 'COLR' not in f:
    print("COLR table not found")
    sys.exit()

print ("Reading COLR table...")
colr=f['COLR']
print("COLR table version:", colr.version)

# fontTools decompiles COLR version 0 differently than COLR version 1:
#  - COLR version 0: the ColorLayers attribute returns a list 
#    (if COLR.numBaseGlyphRecords > 0)
#  - COLR version 1: the ColorLayers attribute is not defined; instead, 
#    the table attribute returns an otTables.COLR object, which has
#    several attributes reflecting the COLR table structure

if colr.version == 0:
    if not hasattr(colr, 'ColorLayers'):
        print("Number of version 0 base glyphs: 0")
    else:
        print("Number of version 0 base glyphs:", len(colr.ColorLayers))
else: # colr.version > 0:
    print("Number of version 0 base glyphs:", colr.table.BaseGlyphRecordCount)
    print("Number of version 0 layer records:", colr.table.LayerRecordCount)
    print("Number of version 1 base glyphs:", colr.table.BaseGlyphList.BaseGlyphCount)
    print("Number of version 1 layers:", colr.table.LayerList.LayerCount)
    if hasattr(colr.table, 'ClipList'):
        print("Has ClipList: True")
        print("Number of Clip records:", len(colr.table.ClipList.clips))
    else:
        print("Has ClipList: False")
    print("Has ItemVariationStore: ", colr.table.VarStore is not None)

