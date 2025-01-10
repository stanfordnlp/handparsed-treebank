This directory contains files for recreating a list of lemmas from German Wiktionary.

This uses the wiktionary_de_parser python library.  This version of
the library was compatible with python 3.9, whereas there is a newer
version compatible only with python >= 3.11.  The API may have changed
between versions... something to look out for

Included in the script is the expected format for the various words,
in case those change.

The script attempts to remove auxiliaries and some various comment
annotations on the words.

