# Reads in the training document for the Stanza French lemmatizer and
# looks for verbs which have expected lemmas in a list provided to us
# by Prof. Guy Lapalme, but were not in the training data.
#
# If this script is rerun after Stanza 1.10, be sure not to clobber
# the output file but rather append newly found missing lemmas

import stanza

# TODO: could make these arguments to an argparse
fr_words_file = "output_fr.txt"
conllu_file = "/home/john/stanza/data/lemma/fr_combined.train.in.conllu"
output_file = "fr_lemmas.conllu"

from stanza.utils.conll import CoNLL
doc = CoNLL.conll2doc(conllu_file)

known_verbs = {word.text: word.lemma for sentence in doc.sentences for word in sentence.words if word.upos == 'VERB'}
print(len(known_verbs))

with open(fr_words_file, encoding="utf-8") as fin:
    lines = fin.readlines()
for idx, line in enumerate(lines):
    if line.startswith("Règles et lexique"):
        break
else:
    raise ValueError("Unexpected file format")
lines = lines[idx:]
lines = [line.split(":", maxsplit=3) for line in lines]
lines = [line for line in lines if len(line) == 4]

new_training_lines = []
pipe = stanza.Pipeline("fr", processors="tokenize,pos,lemma")
for line in lines:
    input_text = line[0].strip()
    expected_lemma = line[2].strip()
    doc = pipe(input_text)
    if len(doc.sentences) > 1:
        raise ValueError("Error in number of sentences!  |%s|" % input_text)
    if len(doc.sentences[0].words) > 2:
        raise ValueError("Error in number of words!  |%s|" % input_text)

    verb = doc.sentences[0].words[1].text
    #if verb in known_verbs and expected_lemma != known_verbs[verb]:
    #    print("Unexpected labeling of %s: %s" % (verb, known_verbs[verb]))
    output_lemma = doc.sentences[0].words[1].lemma
    if output_lemma != expected_lemma:
        #print(input_text, verb, output_lemma, expected_lemma)
        if verb in known_verbs:
            print("Unexpected error for %s" % verb)
        else:
            new_training_lines.append((verb, expected_lemma))

with open(output_file, "w", encoding="utf-8") as fout:
    for sent_id, (verb, expected_lemma) in enumerate(new_training_lines):
        print(verb, expected_lemma)
        fout.write("# sent_id = missing_lemma_%4d\n" % sent_id)
        fout.write("# text = %s\n" % verb)
        fout.write("1\t%s\t%s\tVERB\t_\t_\t0\troot\t_\t_\n\n" % (verb, expected_lemma))

