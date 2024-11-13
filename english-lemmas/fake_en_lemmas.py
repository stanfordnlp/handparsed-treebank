with open("en_lemmas.txt") as fin:
    lines = fin.readlines()

lines = [x.strip() for x in lines]
lines = [x for x in lines if x and not x.startswith("#")]

lemmas = [x.split() for x in lines]

for idx, (word, lemma) in enumerate(lemmas):
    print("# sent_id = missing_lemma_%04d" % idx)
    print("# text = %s" % word)
    print("1\t%s\t%s\tVERB\t_\t_\t0\troot\t_\t_" % (word, lemma))
    print()
