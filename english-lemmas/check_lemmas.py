import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--lemmas', default="en_lemmas.txt", type=str, help='Where to find the lemmas to look for')
parser.add_argument('--conllu', default="/home/john/stanza/data/lemma/en_combined.train.in.conllu", type=str, help='Where to find the training data to check')
args = parser.parse_args()

lemma_file = args.lemmas
conllu_file = args.conllu

with open(lemma_file) as fin:
    lines = fin.readlines()

lemmas = [x.strip().split() for x in lines]

with open(conllu_file) as fin:
    lines = fin.readlines()
    lines = [x.strip() for x in lines]

for lemma in lemmas:
    text = "\t%s\t" % lemma[0]
    print("Looking for %s" % text)
    for line in lines:
        if text in line and "VERB" in line:
            print(line)

print("===================")

for lemma in lemmas:
    text = "\t%s\t" % lemma[0]
    print("Looking for %s" % text)
    for line in lines:
        if text in line and "VERB" not in line:
            print(line)
