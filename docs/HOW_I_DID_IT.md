# How I did it

A chronological account. The paper (`PAPER.md`) is the tidy version; this is the messy one.

## 1. Research first

Before touching code I read everything around the challenge:

* Lasry, Niebel, Kopal & Wacker's *Cryptologia* article — the 14 daily keys, the description of the
  intercept logs, and crucially section 5.3 "Handling errors", which lists the mutilation types they
  met and states that ~14 correct-length cryptograms decrypted with no key at all.
* The full 56-comment thread under Schmeh's blog post. This turned out to be the richest source:
  between Feb and May 2017 Armin Krauß, Norbert Biermann, Thomas Bosbach, Max Baertl and Lasry had
  already read about half the list by hand-editing ciphertexts. Their comments also corrected the
  key table (WordPress had swallowed the "+" placeholders in three substitution squares, making
  them 33–34 characters long) and gave the station callsigns and historical context.
* The Sept 2026 reports that Childs p.217 had been solved with the keyword TRUPPENVERSCHIEBUNG.

Two decisions came out of this: (a) don't trust any claim, re-derive it; (b) the problem is not
"find the key" but "find the damage".

## 2. Tooling

* `adfgvx.py` — key table, encrypt/decrypt, first scoring function.
* `core2.py` — decryptor that carries `?` for unknown symbols through transposition and
  substitution, plus `expand_dashes()` which normalises the web transcription (en/em dashes
  standing for 1–3 unreadable symbols) so each group has exactly 5 slots.
* German quadgram model from Gutenberg prose plus a 15× up-weighted file of the already-solved
  1918 plaintexts and military vocabulary → `quad.bin`.
* First sanity check: Armin's fix for p.100 decrypts with my code. Good.

## 3. The first bug that mattered

My first scorer *skipped* quadgrams containing digits or `?`. The very first exhaustive search
produced "top" results like `9kj60djr30j35jw?ande3ofd54?5014t89…` at a score better than a real
decrypt. The optimiser had simply learned to produce digits. Fix: penalise every non-letter
quadgram at −7.0. After that, true decrypts sit at −4.0…−4.8 and the noise floor of a wrong key is
−6.4…−6.7 — a clean gap, and the basis for every negative result later.

## 4. Search engines, in the order I wrote them

1. **`search2.c`** — for a key, try every single and every pair of insert/delete edits (±1…6
   symbols) anywhere. ~10⁶ candidates, 0.7 s. Validated by re-finding p.100 (insert 2 at 113),
   p.146, p.176a from raw text.
2. **`search3.c`** — three edits restricted to 5-group boundaries (operators lose whole groups).
3. **`beam.py`** — six chained single-edit rounds, width 60. This recovers Biermann's
   seven-edit p.171 solution without help, which convinced me the approach was sound.
4. **`colclimb.c` → `coldesc.c`** — the general model: every column start free within ±7,
   total length free within ±6, simulated annealing with staircase moves, then coordinate descent.
   Needed 30 000 iterations and 20 restarts to reliably re-find p.146's +5/−5 pattern.
5. **Interim-text search** for p.132. The ciphertext is 155 symbols — odd, impossible. No
   single ciphertext deletion helps (−7.0), but deleting one symbol from the *untransposed*
   stream gives −4.9 and Biermann's plaintext. The clerk wrote VVV for VV. I liked this one:
   which search succeeds tells you *who* made the error.
6. **`keyvar.py` / `mixkeys.py`** — reversed keys, one rank dropped/inserted, two columns swapped,
   and all cross-pairings of transposition and substitution between periods.
7. **`transclimb.c`** — unknown-key attack by bigram-IC annealing over the permutation. It
   partially recovers K=16 on the 212-symbol p.187 and nothing stable on anything shorter.
8. **Square reconstruction** (inline scripts) — given a transposition key and a candidate
   plaintext, fit the Polybius square as a constraint problem and count conflicts.

Most runs are in `results/`. One operational lesson: `pkill -f focus.py` also kills the shell
that issued it. Twice.

## 5. What each message got

* **p.100, 105, 109, 146, 171, 176a, 215** — reproduced the 2017 solutions; the two-edit or beam
  search finds them unaided.
* **p.132** — see §4.5.
* **p.187 + "???"** — Biermann guessed both parts share a CHI key; Lasry recovered the
  transposition (CMBLAKOHIDENFJGP). I rebuilt the square from the two ciphertexts and the
  plaintext: zero conflicts, 23 cells determined, both parts decrypt with no edit at all.
* **p.217** — applied the TRUPPENVERSCHIEBUNG rank key, untransposed, fitted the square against
  the reported plaintext: zero conflicts, a keyword-mixed square that looks right
  (`TRUPE4/N·SC2H/·I···G/6A·D·F/···KL·/O·WX·Z`), score −5.0 vs −7.3 for a random 19-key.
  Confirmed. The "S4STEN" is one garbled symbol for "24STEN" — HMS Canterbury, 24 Nov 1918.
* **p.73, 152, 153×2, 158, 170, 176b, 189, 198** — every engine, every key, every key variant.
  Nothing above −5.5; the best-looking fragments needed a dozen columns at extreme offsets, which
  is what over-fitting looks like. Diagnoses: p.153 pair is CHI traffic → probably another
  unrecovered CHI key; p.73 is filed on an ambiguous date and may need a late-October key not in the
  list; p.152/170/189 are too short to distinguish multi-fault fixes from noise; p.176b/198 have
  the profile of messages mis-enciphered at source.

## 6. What I'd do next

* Crib-driven joint attack on the two p.153 parts (NACHRICHTENCHEF / OHL / STATION).
* Try *every* key attested anywhere in Childs's book on the residue regardless of its date —
  p.217 shows the key calendar is not reliable.
* Get the scans: the transcriptions on the blog have at least one known copy error (p.171) and
  the p.164 messages have a missing line of unknowns.
