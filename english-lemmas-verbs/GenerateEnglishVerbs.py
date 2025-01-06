
from pyrealb import *
from opts_feats import opts2feats, getTabCounters

# create a UD structures
#  present and past
def makeUDsent(sent_id, sent, infos, pron_form,pron_lemma,pron_feats,
                             verb_form,verb_lemma,verb_feats):
    verb_misc = "noun" if verb_form in lexicon and "N" in lexicon[verb_form] else "_"
    return f"""# text = {sent}
# sent_id = {sent_id}
# pyrealb-infos = {infos}
1	{pron_form}	{pron_lemma}	PRON	PRP	{pron_feats}	2	nsubj	_	_
2	{verb_form}	{verb_lemma}	VERB	VBP	{verb_feats}	0	root	_	{verb_misc}
3	.	.	PUNCT	.	_	2	punct	_	_
"""

# present participle
def makeUDsentPr(sent_id,sent, infos, pron_form,pron_lemma,pron_feats,
                               verb_form,verb_lemma,verb_feats,
                               pr_form,pr_lemma,pr_feats):
    pr_misc = "noun" if pr_form in lexicon and "N" in lexicon[pr_form] else "_"
    return f"""# text = {sent}
# sent_id = {sent_id}
# pyrealb-infos = {infos}
1	{pron_form}	{pron_lemma}	PRON	PRP	{pron_feats}	3	nsubj	_	_
2	{verb_form}	{verb_lemma}	AUX	VBP	{verb_feats}	3	aux	_	_
3	{pr_form}	{pr_lemma}	VERB	VBG	{pr_feats}	0	root	_	{pr_misc}
4	.	.	PUNCT	.	_	3	punct	_	_
"""

# conjugate verbs
def makeSentences(sent_id, infos, verb_lemma, tense):
    uds = []
    for (pe,n,g) in [(1,"s","-"),(2,"s","-"),(3,"s","m"),(3,"s","f"),(3,"s","n"),(1,"p","-"),(3,"p","-")]:
        pron = Pro("I").pe(pe).n(n)
        pron_opts = {"pe":pe,"n":n,"c":"nom"}
        if g != "-":
            pron.g(g)
            pron_opts["g"]=g
        if tense != "pr":
            verb = V(verb_lemma).t(tense).pe(pe).n(n)
            try:
                verb_form = verb.realize()
                verb_opts = {"t":tense, "pe":pe, "n":n}
                sent = S(pron,VP(verb)).realize()
                pron_form = sent.split(" ")[0]
                uds.append(makeUDsent(f"{sent_id}-{pe}{n}",sent,infos,
                                      pron_form,pron.realize(),opts2feats(pron_opts),
                                      verb_form,verb_lemma,opts2feats(verb_opts)))
            except Exception as error:
                pass
        else:
            verb = V("be").t("p").pe(pe).n(n)
            verb_form = verb.realize()
            verb_opts = {"t":"p","pe":pe,"n":n}
            pr = V(verb_lemma).t("pr")
            try:
                pr_form = pr.realize()
                pr_opts = {"t":"pr"}
                sent = S(pron,VP(verb,pr)).realize()
                pron_form = sent.split(" ")[0]
                uds.append(makeUDsentPr(f"{sent_id}-{pe}{n}",sent,infos,
                                        pron_form,pron.realize(),opts2feats(pron_opts),
                                        verb_form,"be",opts2feats(verb_opts),
                                        pr_form,verb_lemma,opts2feats(pr_opts)))
            except Exception as error:
                pass
    return uds

# generate for each "interesting" tenses
def makeVerb(verb_lemma):
    entry = lexicon[verb_lemma]
    tab = entry['V']['tab']
    verbFile.write(f"{verb_lemma}\t{tab}\t{counters_en[tab]}\n")
    infos = ", ".join(entry.keys())+f"\t{tab}\t{counters_en[tab]}"
    return [*makeSentences(f"{verb_lemma}-p", infos, verb_lemma, "p"),
            *makeSentences(f"{verb_lemma}-ps", infos, verb_lemma, "ps"),
            *makeSentences(f"{verb_lemma}-pr", infos, verb_lemma, "pr")]

####  verb selection
# conjugation table numbers used for more than 20 verbs in the English lexicon
# regular_verbs_tab = {"v1", "v3", "v2", "v4", "v9", "v12", "v14", "v7", "v11", "v5", "v13", "v10", "v6", "v16"}

def keep(entry):
    if "V" in entry:
        return entry["V"]["tab"] not in ["v1","v3"]
        # if entry["V"]["tab"] not in regular_verbs_tab:
        # return "ldv" in entry or "ldv" in entry["V"]
            # but is not either an adjective or a noun
            # return "A" not in entry and "N" not in entry
    else:
        return False

# get the list of lemma for "irregular" verbs
lexicon = getLexicon("en")
verbs = [lemma for lemma,entry in lexicon.items() if "-" not in lemma and keep(entry)]
counters_en = getTabCounters("en")

if __name__ == "__main__":
    load("en")
    Constituent.exceptionOnWarning = True
    fileName = "allverbs"
    verbFile = open(f"{fileName}.txt", "w", encoding="utf-8")
    verbUDs = open(f"{fileName}.conllu", "w", encoding="utf-8")
    for verb_lemma in verbs:
        verbUDs.write("\n".join(makeVerb(verb_lemma)) + "\n")
    print(f" {len(verbs)} verbs conjugated on {fileName}.conllu")
