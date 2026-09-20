# adfgvx-1918 — Re-attacking the "unsolved" ADFGVX cryptograms of 1918

Tools, data, logs and a short paper on the 22 World-War-I ADFGVX radiograms from
J. Rives Childs's collection that George Lasry and Klaus Schmeh published as an open challenge
(scienceblogs.de, Feb 2017). Twelve of them are now read and verified; nine remain open.

| | |
|---|---|
| **Paper** | [`docs/PAPER.md`](docs/PAPER.md) — methods, results, negative results |
| **How I did it** | [`docs/HOW_I_DID_IT.md`](docs/HOW_I_DID_IT.md) — the chronological, first-person account |
| **Run log / status table** | [`docs/REPORT.md`](docs/REPORT.md) |
| **Solutions** | [`docs/SOLUTIONS.md`](docs/SOLUTIONS.md) — every decrypt with its exact ciphertext fix |
| **Code** | [`src/`](src/) — Python drivers + C search engines |
| **Raw search output** | [`results/`](results/) |

## Quick start

```bash
cd src
make                 # builds search2 search3 coldesc colclimb transclimb (needs gcc)
python3 verify.py    # regenerates all 12 verified decrypts from the raw transcriptions
```

Attack a message with every known key (two-edit exhaustive search):

```bash
python3 runall.py p152            # or any id from messages.py
python3 beam.py p158 Nov7-9       # 6-step beam search with one key
./coldesc "<CIPHERTEXT>" "6,12,7,15,1,11,16,5,8,14,3,18,9,13,2,17,20,10,19,4" \
          "PRMYUW3LZGES8C71QOV29ITB405KXH6AJNDF" 236 248 12 1 7   # column-offset annealing
```

`data/quad.bin` is the German quadgram model used by the C engines; rebuild it with
`python3 build_model.py` (downloads a few Gutenberg texts).

## Layout

```
docs/      PAPER.md  HOW_I_DID_IT.md  SOLUTIONS.md  REPORT.md
src/       adfgvx.py core2.py messages.py      library: keys, decryptor, transcriptions
           search2.c search3.c coldesc.c colclimb.c transclimb.c   C engines
           runall.py run3.py beam.py iter.py focus.py keyvar.py mixkeys.py final_cd.py  drivers
           verify.py build_model.py Makefile
data/      quad.bin  military_vocab.txt
results/   raw logs of the big searches
```

## Credits

Keys: Lasry, Niebel, Kopal & Wacker, *Cryptologia* 41(2), 2017. First manual solutions (2017):
Armin Krauß, Norbert Biermann, Thomas Bosbach, Max Baertl, George Lasry. p.217 keyword
(TRUPPENVERSCHIEBUNG): "prinz" with GPT-6 Astra, Sept 2026. This repository independently
re-derives and verifies all of these and adds the systematic error-model search and the
negative results. Licence: MIT.
