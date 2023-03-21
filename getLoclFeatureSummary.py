# script that gets a font file name from the command line and reports the language system tags that use the 'locl' feature
from fontTools.ttLib import TTFont
import sys

def getLangSysSummary(tag, font):
    if tag not in font:
        print("\n'%s' table not found" % tag)
    else:
        print("\n'%s' table found\n" % tag)
        otTable = font[tag]

        # get list of script / language system tags
        langsys = [(script.ScriptTag, langsys.LangSysTag, langsys) 
                for script in otTable.table.ScriptList.ScriptRecord 
                for langsys in script.Script.LangSysRecord
                    ]
        if len(langsys) == 0:
            print("'%s' does not use any language system tags\n" % tag)
        else:
            print("'%s' uses the following non-default language systems (script, language system):" % tag)
            for l in langsys:
                print(l[0], l[1])

        # filter that list to include only those that use the 'locl' feature

        # get list of 'locl' feature indices
        locl = [i for i, f in enumerate(otTable.table.FeatureList.FeatureRecord) if f.FeatureTag == 'locl']
        # print("\n'locl' feature indices:", locl)

        # get list of script / language system tags that use the 'locl' feature
        langsysWithLocl = [l for l in langsys for f in l[2].LangSys.FeatureIndex if f in locl]

        if len(langsysWithLocl) == 0:
            print("\n'%s' does not use the 'locl' feature in any language system\n" % tag)
        else:
            print("\n'%s' uses the 'locl' feature in the following language systems:" % tag)
            for l in langsysWithLocl:
                print(l[0], l[1])
    return

f=TTFont(sys.argv[1])
print("\n=========================================")
getLangSysSummary('GPOS', f)
print("-----------------------------------------")
getLangSysSummary('GSUB', f)
print("\n=========================================\n")

