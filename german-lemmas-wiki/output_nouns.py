from collections import defaultdict
from pprint import pprint

from german_nouns.lookup import Nouns

nouns = Nouns()

lemma_to_form = defaultdict(list)
form_to_lemma = defaultdict(list)

#{'flexion': {'akkusativ plural': '30er',
#             'dativ plural': '30ern',
#             'genitiv plural': '30er',
#             'nominativ plural': '30er'},
# 'lemma': '30er',
# 'pos': ['Substantiv']}


for noun in nouns:
    assert len(noun) == 1
    noun = noun[0]
    lemma = noun['lemma']
    if '-' in lemma or ' ' in lemma:
        continue
    if any(x in lemma for x in "0123456789"):
        continue

    inflections = set(noun['flexion'].values())
    for form in inflections:
        form_to_lemma[form].append(lemma)
        lemma_to_form[lemma].append(form)

        #print(form, lemma)

for form in form_to_lemma:
    if len(form_to_lemma[form]) != 1:
        #print("Conflict at %s" % form)
        for lemma in form_to_lemma[form]:
            if lemma in lemma_to_form:
                del lemma_to_form[lemma]

processed = []
for lemma in sorted(lemma_to_form):
    for form in sorted(set(lemma_to_form[lemma])):
        processed.append((lemma, form))

for idx, (lemma, form) in enumerate(processed):
    print("# sent_id = %d" % idx)
    print("# text = %s" % form)
    print("1\t%s\t%s\tNOUN\t_\t_\t0\troot\t_\t_" % (form, lemma))
    print()
