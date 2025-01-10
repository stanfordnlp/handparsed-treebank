# Converts a file of English adjectives and their lemmas
# Lemma information sent from Prof. Lapalme in Montreal

with open("english-Adj-comp.txt") as fin:
    text = fin.readlines()

words = []
for line in text:
    line = line.strip()
    if not line:
        continue
    pieces = line.split()
    for word in pieces:
        # lemma, word
        words.append((pieces[0], word))

pos = "ADJ"
with open("en_adj.conllu", "w") as fout:
    for idx, (lemma, form) in enumerate(words):
        fout.write("# sent_id = %d\n" % idx)
        fout.write("# text = %s\n" % form)
        fout.write("1\t%s\t%s\t%s\t_\t_\t0\troot\t_\t_\n" % (form, lemma, pos))
        fout.write("\n")
