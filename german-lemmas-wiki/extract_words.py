from bz2 import BZ2File
from collections import defaultdict

from tqdm import tqdm
from wiktionary_de_parser import Parser

bzfile_path = 'dewiktionary-latest-pages-articles-multistream.xml.bz2'
bz_file = BZ2File(bzfile_path)

known_pos = set()

empty_pos = 0
multi_pos = 0


# ADJ: Adjektiv
# ADV: Adverb
# NOUN: Substantiv
# VERB: Verb

POS_MAP = {"Adjektiv":   "ADJ",
           "Adverb":     "ADV",
           "Substantiv": "NOUN",
           "Verb":       "VERB"}

form_to_lemma = defaultdict(set)
lemma_to_form = defaultdict(set)

# example verb:
# {'title': 'lieben', 'lemma': 'lieben', 'inflected': False,
#  'flexion': {'Präsens_ich': 'liebe', 'Präsens_du': 'liebst', 'Präsens_er, sie, es': 'liebt',
#              'Präteritum_ich': 'liebte', 'Partizip II': 'geliebt', 'Konjunktiv II_ich': 'liebte',
#              'Imperativ Singular': 'liebe', 'Imperativ Plural': 'liebt', 'Hilfsverb': 'haben'},
#  'ipa': ['ˈliːbn̩'], 'rhymes': ['iːbn̩'], 'lang': 'Deutsch', 'lang_code': 'de',
#  'pos': {'Verb': []}, 'syllables': ['lie', 'ben']}

# example noun:
# {'title': 'Hallo', 'lemma': 'Hallo', 'inflected': False,
#  'flexion': {'Genus': 'n', 'Nominativ Singular': 'Hallo', 'Nominativ Plural': 'Hallos',
#              'Genitiv Singular': 'Hallos', 'Genitiv Plural': 'Hallos', 'Dativ Singular': 'Hallo',
#              'Dativ Plural': 'Hallos', 'Akkusativ Singular': 'Hallo', 'Akkusativ Plural': 'Hallos'},
#  'ipa': ['haˈloː'], 'rhymes': ['oː'], 'lang': 'Deutsch', 'lang_code': 'de',
#  'pos': {'Substantiv': []}, 'syllables': ['Hal', 'lo']}

# example adverb:
# {'title': 'man', 'lemma': 'man', 'inflected': False,
#  'ipa': ['man'], 'rhymes': ['an'], 'lang': 'Deutsch', 'lang_code': 'de',
#  'pos': {'Adverb': []}, 'syllables': ['man']}

# example adj:
# {'title': 'pittoresk', 'lemma': 'pittoresk', 'inflected': False,
#  'flexion': {'Positiv': 'pittoresk', 'Komparativ': 'pittoresker', 'Superlativ': 'pittoreskesten'},
#  'ipa': ['ˌpɪtoˈʁɛsk'], 'rhymes': ['ɛsk'], 'lang': 'Deutsch', 'lang_code': 'de',
#  'pos': {'Adjektiv': []}, 'syllables': ['pit', 'to', 'resk']}

for record in tqdm(Parser(bz_file)):
    if 'lang_code' not in record or record['lang_code'] != 'de':
        continue
    if 'pos' not in record:
        continue
    if len(record['pos']) == 0:
        empty_pos += 1
        continue

    if len(record['pos']) > 1:
        multi_pos += 1
        continue

    lemma = record['lemma']
    if ' ' in lemma:
        continue

    if record['inflected']:
        continue

    for pos in record['pos']:
        # will be exactly one
        break
    known_pos.add(pos)
    if pos not in POS_MAP:
        continue
    pos = POS_MAP[pos]

    if 'flexion' not in record:
        flexion = [lemma]
    else:
        flexion = set(record['flexion'][x] for x in record['flexion']
                      if (not x.startswith('Hilfsverb') and not x.startswith('Genus') and
                          not x.startswith("Kein") and not x.startswith("kein") and not x in ("unpersönlich",)))

    if 'sein' in flexion:
        raise ValueError("Missing an auxiliary in this record:\n{}".format(record))

    if any(x in ('n', 'f', 'ja') for x in flexion):
        raise ValueError("Weird lemma in:\n{}".format(record))

    for form in flexion:
        if ' ' in form:
            continue
        form_to_lemma[(form, pos)].add(lemma)
        lemma_to_form[(lemma, pos)].add(form)

#print(empty_pos)
#print(multi_pos)
#print(sorted(known_pos))

print("Found %d lemma/pos combinations to consider" % len(lemma_to_form))

# If the same form and POS maps to two different lemmas, we eliminate
# all lemmas of those forms.
# This way, the lemmatizer will not be confused.
for key in tqdm(form_to_lemma):
    if len(form_to_lemma[key]) > 1:
        key = form, pos
        for lemma in form_to_lemma[key]:
            if (lemma, pos) in lemma_to_form:
                del lemma_to_form[(lemma, pos)]

print("Filtered to %d lemma/pos combinations to consider" % len(lemma_to_form))

processed = []
for key in sorted(lemma_to_form):
    for form in sorted(set(lemma_to_form[key])):
        lemma, pos = key
        processed.append((lemma, form, pos))

with open("de_wiki_lemmas.conllu", "w", encoding="utf-8") as fout:
    for idx, (lemma, form, pos) in tqdm(enumerate(processed)):
        fout.write("# sent_id = %d\n" % idx)
        fout.write("# text = %s\n" % form)
        fout.write("1\t%s\t%s\t%s\t_\t_\t0\troot\t_\t_\n" % (form, lemma, pos))
        fout.write("\n")
