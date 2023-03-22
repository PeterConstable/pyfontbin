# script that takes in a filename pattern or list of filenames for fonts and returns the font versions
from fontTools.ttLib import TTFont, TTCollection
import sys
from pathlib import Path

def getFontVersion(font):
    version = font['name'].getDebugName(5)
    if version == None:
        version = font['head'].fontRevision
    return version

def getFontsFromPath(fontPath):
    # returns list of tuples (fontPath, font)
    if fontPath.is_dir():
        return []
    elif fontPath.suffix in (".ttc", ".otc"):
        return [(fontPath.name +":" + str(i), font) for i, font in enumerate(TTCollection(fontPath).fonts)]
    elif fontPath.suffix in (".ttf", ".otf"):
        return [(fontPath.name, TTFont(fontPath))]
    else:
        return []

if __name__ == "__main__":
    from argparse import ArgumentParser
    import glob

    parser = ArgumentParser(description="Get font versions from font files")
    parser.add_argument("filePaths", nargs="+", help="Files or patterns to search")
    args = parser.parse_args()

    # Deglob filePaths for Windows
    files = []
    for path in args.filePaths:
        files.extend([Path(f) for f in glob.glob(path, recursive=True)])

    for fontPath in files:
        for item in getFontsFromPath(fontPath):
            print(item[0], getFontVersion(item[1]))
