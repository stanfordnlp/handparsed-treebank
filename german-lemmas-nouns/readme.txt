This directory contains files for recreating a list of lemmas from German Wiktionary:
extract_words.py

This uses the wiktionary_de_parser python library.  This version of
the library was compatible with python 3.9, whereas there is a newer
version compatible only with python >= 3.11.  The API may have changed
between versions... something to look out for

Included in the script is the expected format for the various words,
in case those change.

The script attempts to remove auxiliaries and some various comment
annotations on the words.



Also included is output_nouns.py
This *only* outputs a list of nouns, using a separate module german_nouns
Unfortunately, this seemed to confuse the lemmatizer into always
lemmatizing unknown words as if they were nouns.
Using extract_words.py is preferred
