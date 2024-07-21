"""
Goal:

Add infinitives with pronouns on the end to the Spanish combined dataset

verlos
hacerlos
haberlos
etc etc

Starting from a list in this issue:

https://github.com/stanfordnlp/stanza/issues/1401
"""

from stanza.utils.conll import CoNLL

starter = CoNLL.conll2doc("handpicked.mwt")

VERBS = [
    "amar",
    "amoblar",
    "arreglar",
    "atar",
    "ayudar",
    "besar",
    "besar",
    "buscar",
    "cambiar",
    "compartir",
    "conquistar",
    "consumir",
    "decir",
    "distraer",
    "escuchar",
    "esquivar",
    "estudiar",
    "haber",
    "hacer",
    "incluir",
    "invadir",
    "llamar",
    "lograr",
    "matar",
    "nulificar",
    "ordenar",
    "oír",
    "romper",
    "saber",
    "sentir",
    "sublimar",
    "tener",
    "usar",
    "ver",
]

sent_id = int(starter.sentences[-1].sent_id)

new_sentences = []
for verb in VERBS:
    sent_id += 1
    mwt = ["1-2", "%slos" % verb, "_", "_", "_", "_", "_", "_", "_", "SpaceAfter=No"]
    inf = ["1", verb, verb, "VERB", "_", "VerbForm=Inf", "0", "root", "_", "_"]
    sentence = [
        "# sent_id = %d" % sent_id,
        "# text = %slos." % verb,
        "\t".join(mwt),
        "\t".join(inf),
        "2	los	él	PRON	_	_	1	obj	_	_",
        "3	.	.	PUNCT	_	PunctType=Peri	1	punct	_	_"
    ]
    new_sentences.append("\n".join(sentence))

    sent_id += 1
    Verb = verb[0].upper() + verb[1:]
    sentence[0] = "# sent_id = %d" % sent_id
    sentence[1] = "# text = %slos." % Verb
    mwt[1] = Verb + "los"
    sentence[2] = "\t".join(mwt)
    inf[1] = Verb
    sentence[3] = "\t".join(inf)
    new_sentences.append("\n".join(sentence))

print("{:C}".format(starter))
print()

for sentence in new_sentences:
    print(sentence)
    print()
