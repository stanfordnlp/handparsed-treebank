from collections import Counter
from pyrealb import getLexicon

tense2feats = {
    "p": "Tense=Pres|Mood=Ind|VerbForm=Fin",
    "i": "Tense=Imp|Mood=Ind|VerbForm=Fin",
    "ps":"Tense=Past|Mood=Ind|VerbForm=Fin",
    "f": "Tense=Fut|Mood=Ind|VerbForm=Fin",
    "s": "Tense=Pres|Mood=Sub|VerbForm=Fin",
    "si":"Tense=Imp|Mood=Sub|VerbForm=Fin",
    "c": "Tense=Pres|Mood=Cnd|VerbForm=Fin",
    "ip":"Tense=Pres|Mood=Imp|VerbForm=Fin",

    "b": "Tense=Pres|VerbForm=Inf",

    "pr":"Tense=Pres|VerbForm=Part",
    "pp":"Tense=Past|VerbForm=Part",
}

case2feats = {
    "nom": "PronTyp=Prs|Case=Nom",
    "acc": "PronTyp=Prs|Case=Acc",
    "dat": "PronTyp=Prs|Case=Dat",
    "gen": "PronTyp=Prs|Case=Gen"
}

def opts2feats(opts):
    def error(k,v):
        print(f"** Strange {k}:{v} in {opts}")

    feats = []
    for key,val in opts.items():
        if key == "pe":
            if val in [1,2,3,"1","2","3"]: feats.append(f"Person={val}")
            else: error(key,val)
        elif key == "n":
            if val == "s":feats.append(f"Number=Sing")
            elif val == "p":feats.append(f"Number=Plur")
            else: error(key,val)
        elif key == "t":
            if val in tense2feats: feats.append(tense2feats[val])
            else: error(key,val)
        elif key == "g":
            if val == "m": feats.append("Gender=Masc")
            elif val == "f": feats.append("Gender=Fem")
        elif key == "c":
            if val in case2feats:feats.append(case2feats[val])
            else:error(key,val)
        else: error(key,val)
    return "|".join(feats)

# compute statistics about tab value occurrences
def getTabCounters(lang):
    counters = Counter()
    for (word,infos) in getLexicon(lang).items():
        for (pos,info) in infos.items():
            if isinstance(info,dict) and "tab" in info:
                    tabval = info["tab"]
                    if isinstance(tabval,str):
                        counters[tabval]+=1
    return counters
