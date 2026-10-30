This directory contains a list of lemmas from German Wiktionary,
de_wiki_lemmas.conllu.gz, used as the dictionary of the de_combined
lemmatizer.  It is gzipped to stay under the GitHub file size limit.

To recreate it, use the converter in Stanza:

  pip install wiktionary-de-parser==0.16.0
  python3 -m stanza.utils.datasets.lemma.convert_de_wiktionary dewiktionary-latest-pages-articles-multistream.xml.bz2 de_wiki_lemmas.conllu.gz

https://github.com/stanfordnlp/stanza/blob/dev/stanza/utils/datasets/lemma/convert_de_wiktionary.py

The converter is written for that exact version of wiktionary-de-parser,
which requires Python 3.13 or later, and checks for it.  The parser's
output format changes between versions, so a different version needs
the converter updated to match.

The dump is available from

  https://dumps.wikimedia.org/dewiktionary/latest/

German Wiktionary is licensed under CC BY-SA 4.0.


extract_words.py is the original script, which was written for an
older version of wiktionary_de_parser compatible with Python 3.9.  It
does not run with current versions of the library, but is kept for
reference.


Also included is output_nouns.py
This *only* outputs a list of nouns, using a separate module german_nouns
Unfortunately, this seemed to confuse the lemmatizer into always
lemmatizing unknown words as if they were nouns.
Using the Stanza converter is preferred
