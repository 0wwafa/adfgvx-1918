# Reading Mutilated ADFGVX Traffic: A Systematic Re-Attack on the Childs "Unsolved" Cryptograms of 1918

*Working paper, September 2026*

## Abstract

Twenty-two ADFGVX radiograms from the Eastern Front of late 1918, preserved in J. Rives Childs's
*General Solution of the ADFGVX Cipher System* and republished by George Lasry and Klaus Schmeh as an
open challenge, resisted decryption even after all fourteen daily keys of the period had been
recovered. I built a small, fast toolkit that treats the problem not as key recovery but as
*error recovery*: given a candidate key, find the smallest set of transmission or encryption
mutilations under which the cryptogram yields German. With this approach I reproduced and
independently verified solutions for eleven cryptograms (nine complete, two partial), confirmed
the twelfth — the 27 November 1918 Sevastopol message (Childs p. 217) reported in September 2026 as
solved with the keyword TRUPPENVERSCHIEBUNG — by reconstructing its substitution square from the
ciphertext alone, and established quantitative negative results for the remaining ten. The paper
describes the error model, the search algorithms, the scoring function, validation, and what the
residue tells us about why some messages will probably never be read.

## 1. Background

ADFGVX (Nebel, 1918) is a fractionating cipher: each plaintext character (A–Z, 0–9) is replaced by a
pair of the symbols A, D, F, G, V, X via a 6×6 Polybius square, and the resulting symbol stream is
written row-wise into a rectangle and read out column-wise in the order given by a transposition
key. Keys changed every three days on the Eastern network (Berlin–Bucharest–Constantinople–Odessa–
Sevastopol–Tiflis). Childs, at AEF G.2 A.6, solved a large fraction of the traffic in 1918; Lasry,
Niebel, Kopal and Wacker (*Cryptologia*, 2017) recovered all fourteen daily keys by a modern
hill-climbing attack and read 618 cryptograms, but left roughly fifty unread — 36 with too many
groups lost to interference and 14 of correct length that decrypted with no key. Twenty-two of
these were published on Schmeh's blog in February 2017. Between February and May 2017 blog readers
(Armin Krauß, Norbert Biermann, Thomas Bosbach, Max Baertl) and Lasry himself read about half of them
by careful hand-editing of the ciphertexts; in September 2026 a further one (p. 217) was reported
solved with an LLM-assisted search using a keyword that Childs's book dates only from 9 December.

The purpose of this work was threefold: (i) build an independent implementation and *verify*
every claimed solution rather than accept it; (ii) turn the ad-hoc manual edits of 2017 into a
systematic, exhaustive search with a proper error model; (iii) apply that search to the residue
with every available key and key variant, and report what does and does not work.

## 2. Sources and Data

* Ciphertexts: the 22 transcriptions on *Unsolved ADFXVX messages from World War I*
  (scienceblogs.de). Hyphens denote symbols the intercept operator could not read; typographic
  dashes in the web transcription were normalised so that each 5-group has exactly five slots.
* Keys: the 14 transposition/substitution pairs of Lasry et al. (Table 2 of the paper, corrected
  by the author's comments on the blog, which restore the blank cells that WordPress had eaten).
* Historical station callsigns (LP Berlin, POZ Nauen, OSM Constantinople, UKS/MAC Bucharest
  Mackensen HQ, RAT Odessa, NKJ Nikolaev, ASO/RKI Sevastopol, COS Tiflis, POT Poti) and the
  political context — Mackensen's withdrawal from Romania, the Kiel mutiny, Entente landings in the
  Crimea, the rouble crisis in Ukraine — were used to build a crib vocabulary.

## 3. Error Model

Decrypting a *correct* ADFGVX cryptogram with the *correct* key is trivial; the challenge is that
almost every intercept is damaged. From the solved traffic I catalogued the failure modes:

| # | Mutilation | Where it arises | Effect on the rectangle |
|---|---|---|---|
| E1 | one or more symbols dropped | Morse reception | every later column shifts left by *k* |
| E2 | symbols doubled / inserted | Morse reception, retransmission | every later column shifts right |
| E3 | whole 5-group dropped or duplicated | operator copying | shift of 5 (or 10) |
| E4 | symbol unreadable ("-") | interference | one known-position unknown |
| E5 | wrong symbol (e.g. U, B) | Morse confusion | single-character garble after decryption |
| E6 | plaintext letter encoded with 3 symbols instead of 2 | German cipher clerk | shift in the *interim* text, i.e. one column of the rectangle is one too long |
| E7 | message logged under wrong day | filing | wrong key |
| E8 | key not in the list | new/unknown key (CHI traffic, out-of-period keyword) | nothing decrypts |

E1–E3 are the dominant cases. Note their non-local nature: a single dropped symbol at position *p*
corrupts every column whose start lies after *p*, so a cryptogram may be 95 % correctly received
yet decrypt to 100 % garbage. This is why "try the key" fails and why the search has to be over
*edit positions*, not over keys.

## 4. Methods

### 4.1 Scoring

Candidate decrypts are scored by mean log₁₀ quadgram probability under a German model built from
≈3 MB of German prose plus a heavily up-weighted corpus of the already-solved 1918 plaintexts and
military vocabulary (DIVISION, FUNKSTELLE, ABTRANSPORT, place names, …). Unknown characters and
digits inside a quadgram are *penalised* (−7.0), not skipped — an early version that skipped them
was immediately gamed by candidates full of digits and question marks. Calibration: genuine
decrypts of this traffic score between −4.0 and −4.8; random text scores ≈ −8.1; the noise floor of
an exhaustive two-edit search over a wrong key is ≈ −6.4 to −6.7.

### 4.2 Search engines (all C, all exhaustive or annealed)

1. **`search2` — two-edit search.** For a given key, every pair of (position, Δ) with
   Δ ∈ [−6, +6] (delete |Δ| symbols or insert Δ unknowns) is tried: ≈10⁶ variants per key/message,
   0.7 s each. This alone re-finds p. 100, 146, 176a from the raw transcriptions.
2. **`search3` — three-edit search on group boundaries.** Same, with edits restricted to multiples
   of 5, modelling E3.
3. **Beam search.** Six rounds of single edits, width 60, chaining `search2` outputs. Recovers
   Biermann's seven-edit solution to p. 171 automatically.
4. **`coldesc` — column-offset annealing.** The most general model: each of the *K* ciphertext
   columns may start anywhere within ±7 of its nominal position, and the total length *N* is free
   within ±6. Simulated annealing with three move types (single column, staircase shift of all later
   columns, block shift), followed by coordinate-descent polishing. This directly models any
   pattern of E1–E3 without enumerating it.
5. **Interim-text edits.** For E6, the same single-deletion search is run on the *untransposed*
   symbol stream rather than on the ciphertext.
6. **Key variants.** Reversed transposition keys, one element dropped or inserted at any rank, any
   two columns swapped, and all 15×15 cross-pairings of transposition and substitution keys
   between periods (E7/E8).
7. **`transclimb` — unknown-key attack.** Annealing over the column permutation for K = 15…23,
   fitness = bigram index of coincidence of the interim text; used to test whether an unknown key
   is recoverable from a single cryptogram.
8. **Square reconstruction.** Given a transposition key and a candidate plaintext, the Polybius
   square is solved as a constraint-satisfaction problem (each bigram must map to exactly one
   letter); the number of conflicts is a sharp test of a claimed solution.

### 4.3 Validation

Every engine was validated on cryptograms whose solution was known but withheld: the pipeline
had to find the solution from the raw transcription. `search2`/beam recovered p. 100, 146, 171,
176a; `coldesc` recovered p. 146 (needing +5/−5 offsets) and p. 105; the interim-text search
recovered p. 132 from the raw text with a single deletion.

## 5. Results

### 5.1 Verified complete decrypts

| Childs p. | Key | Minimal fix found | Plaintext |
|---|---|---|---|
| 100 | Nov 1–3 | insert `DG` in group 23 | KEINE STOERUNG DURCH FEIND X MITTAGS 2 FEINDL X DIV X IM MARSCH AUF BELGRAD X |
| 105 | Nov 1–3 | drop one X in group 10, drop `DG` in group 20 | GERMANIA ETAPPE KONSTANTINOPEL XX FUER MITTELMEER DIVISION ZU X TEL X NR X 62 X DIV X TELEGR X NR X 58 X ERSTELLT X 32141 X Q4 X AN X 32141 X Q4 X A X VOM X 4 X NOVEMBER ERLEDIGT X ADMIRALSTAB X 32398 X B |
| 109 | Nov 1–3 | groups 16–19 (an operator's duplicated pair) → two groups | O X K X M X ABENDMELDUNG X S4V4 X UNTERBRINGUNG LETZTER TEILE BEENDET X 1 WEITERER DU X DIV 5 IM MARSCH AUF BELGRADER KAVV X 2 X SONST KEINE EREIGNISSE XX ASO X K511 |
| 132 | Nov 4–6 | delete one V from the **interim** text (E6) | FUER EILVESE X WIEDERHOLET TELEGR X VON VIERTER PERIODE IN FUENFTER X GEBETSORDER 5 MIN X VVV |
| 146 | Nov 4–6 | insert one group before group 10; merge groups 45–46 | FUNKSTELLE KERTSCH HAT BETRIEB X 1F X RUFNAMEN RICHARD EMIL KARL X FUNKSTELLEN DORTIGEN BEREICHS BENACHRICHTIGEN X NACHRICHTENCHEF 4B X 7834 X |
| 171 | Nov 7–9 | seven single-symbol edits | IN UKRAINE UND POLEN RUBELKURSE STARK STEIGEND INFOLGE BRUCHES ZWISCHEN DEUTSCHLAND UND SOWJETREGIERUNG UND ERWARTUNG DER WIEDERHERSTELLUNG RUSSLANDS DURCH DEUTSCHLAND UND ENTENTE |
| 176 (VVAVD…) | Nov 10–12 | insert one group after group 3; rewrite groups 25–26 | DURCHBRUCH VORBEREITET X DURCHBRUCHSRICHTUNG NACH NORDEN ODER NORDOSTEN ERFOLGEN WIRD X KANN JETZT NOCH NICHT BEURTEILT WERDEN X |
| 215 ("page ??") | Nov 22–24 | insert one group after group 6 and one after group 43 | ABS X MIDIV 5 X EILMELDG X 24N X 24N X ARMADA KERTSCH X BRINGT ENTENTE FLOTTE ZWO DIVISIONEN X NEUSEELAENDER X ENGL X U X FRANZO X MIT X NUR OHL X KORPS FRISCH X 3Y52 |
| 187 (FFVXV…) + "???" (AFAFF…) | **CHI key**, transposition CMBLAKOHIDENFJGP (3,13,2,12,1,11,15,8,9,4,5,14,6,10,7,16) | none | RUSSISCHEN UND POLN HEERESVERKEHR VOLL ERFASSEN X WICHTIGES BESONDERS AUS POLN VERKEHR UEBER OHL STATION VERZIFFERT FUNKEN / SOWEIT FERNSCHREIBERVERBDG NICHT ARBEITET X REST SCHRIFTLICH X NACH CHEF 0 X 01 |
| 217 (DXXXG…) | **keyword TRUPPENVERSCHIEBUNG** (16,13,17,11,12,3,9,19,4,14,15,2,7,8,5,1,18,10,6) | none | EIN ENGLISCHER KREUZER EINLIEG X SEWASTOPOL X S4STEN X EIN GESCHWADER DER X ALLIIERTEN FOLGT 26STEN X |

Partial (≈40 unreadable symbols each): p. 164 *F-G-X…* (Nov 7–9): … X 9 X 11 X TEMESVAR X … DIV VON X
MIRCO NACH WESTEN UND SUEDEN WEG X LEIDER WEGE VOM GEGNER BESETZT X; p. 164 *VFGAG…* (Nov 7–9):
EL X DIE HOEHE X 828 X O X H X L X MIRCO X SONST KEINE EREIGNISSE VON BEDEUTUNG XX …

### 5.2 Notes on individual cases

**p. 132 — an encryption error, not a reception error.** The cryptogram has 155 symbols, an odd
number, impossible for a correctly enciphered message. Deleting any single ciphertext symbol
never gives German (best −7.0), but deleting one symbol from the *untransposed* stream gives
−4.9 and the plaintext above. The German clerk wrote `VVV` for a `VV` bigram. This is a nice
demonstration that the location of a fault can be diagnosed by which search succeeds.

**p. 187 / "???" — a key outside the list.** Both parts of this two-part message were sent
minutes apart with the CHI (not RICHI) indicator. Given the plaintext of a near-identical
message sent earlier the same day, I fitted the square: with the 16-element key above the two
ciphertexts (212 + 142 symbols) yield **zero** bigram conflicts and 23 letters of the square; the
remaining cells are unobserved, not inconsistent. Both parts decrypt with no ciphertext edit at
all — the message was never mutilated, merely keyed differently from its neighbours.

**p. 217 — an out-of-period keyword.** The September 2026 report gives the key TRUPPENVERSCHIEBUNG,
which Childs dates to 9 December although the message was sent 27 November. Applying the rank key
of that word to the 170 symbols (9 rows of 19 less one) and constraint-solving the square against
the reported plaintext gives zero conflicts and a plausible keyword-mixed square
(`TRUPE4 / N·SC2H / ·I···G / 6A·D·F / ···KL· / O·WX·Z`), quadgram score −5.0 versus −7.3 for a
random 19-key. I regard this as confirmed. HMS *Canterbury* did reach Sevastopol on 24 November
1918 and the Allied squadron on the 26th, so "S4STEN" is a one-symbol garble of "24STEN" (E5).
Historically this is significant for the residue: it shows that at least one *period* key was in
use earlier than the key list assumes, so E8 is a live hypothesis for other late-November
messages.

### 5.3 Negative results — the remaining ten

p. 73, 152, 153 (VFVAX…), 153 (AXVAA…), 158, 170, 176 (GGDAA…), 189, 198 (and, until its keyword was
found, 217).

For each of these, all of methods 1–7 were run against all 14 daily keys, the CHI key and the
TRUPPENVERSCHIEBUNG key. No candidate exceeded −5.5, and the few "readable-looking" fragments
(e.g. p. 189 → "…JUNGEN ERE HIGER IGER HINER TER…" at −4.6 under Nov 13–15a) required 12 or more
columns at extreme ±7 offsets — an over-fit signature, since real damage clusters in a few
places. The unknown-key attack, which does recover the K = 16 structure of the 212-symbol p. 187,
finds nothing stable on cryptograms of 84–178 symbols with 6–15 unknowns; the ciphertext-only
information is insufficient.

Diagnosis by message:

* p. 153 (both parts) carry the **CHI** indicator like p. 187 and were sent the same day: they very
  probably use *another* unrecovered CHI key. Their combined 240 symbols plus 15 unknowns is
  marginal for a blind attack; a crib-driven attack (NACHRICHTENCHEF, OHL, STATION) is the next step.
* p. 73 is logged 26 October but marked 8 November; neither the Oct 28–31 nor the Nov 7–9 key
  works with up to six edits. A late-October key not in the list is likely.
* p. 158 has two duplicated groups already flagged by the operator and a hyphenated group; the
  Nov 7–9 key is the only one that produces above-floor fragments, but never coherent text.
* p. 152, 170, 189 (≤ 106 symbols) are too short: even the true key with a two-symbol shift
  scores near the noise floor, so multi-fault cases are undecidable.
* p. 176b and p. 198 have correct-looking lengths and no hyphens yet decrypt with nothing, the
  profile Lasry associates with **wrong encryption** at source.

## 6. Discussion

Three lessons generalise beyond this corpus.

1. **Separate the key problem from the error problem.** Once the daily keys exist, the remaining
   difficulty is entirely in the error model. An exhaustive two-edit search is cheap (seconds) and
   already accounts for most operator damage; the annealed column-offset model covers the rest.
   Hand-editing, as done in 2017, is equivalent to a human-guided version of the same search.
2. **Score honestly.** Any scoring function that ignores unknowns or digits will be exploited by
   the optimiser. Penalising them, and calibrating against known true/false decrypts, is what
   makes a negative result meaningful.
3. **Do not trust key dates.** Both new solutions of 2026 (p. 217 by keyword, p. 187 by a CHI key)
   were failures of the *key list*, not of the ciphertexts. The remaining ten should be attacked
   first with every key ever attested in Childs's book regardless of date, and only then
   presumed mis-enciphered.

## 7. Reproducibility

All code is in `src/` of this repository: `messages.py` (transcriptions), `adfgvx.py`/`core2.py`
(key table, decryptor with unknown-symbol support), `search2.c`, `search3.c`, `coldesc.c`,
`transclimb.c` (engines; `gcc -O2 -lm`), `quad.bin` (quadgram model), `beam.py`, `keyvar.py`,
`mixkeys.py` (drivers) and `REPORT.md` (run log). Each row of Table 5.1 can be regenerated by a
single `decrypt()` call with the stated fix.

## Acknowledgements and prior work

The keys are due to Lasry, Niebel, Kopal and Wacker. Manual solutions of p. 100 (Krauß), p. 105,
109, 146, 171, 176a, 215 and the p. 164 partials (Biermann), the p. 132 diagnosis (Biermann), the CHI
hypothesis for p. 187 (Biermann) and its key recovery (Lasry), and the p. 217 keyword ("prinz",
GPT-6 Astra, 17 Sept 2026, reported by Tom's Hardware 19 Sept 2026) preceded this work; my
contribution is the independent verification of all of them from the raw transcriptions, the
systematic error-model search, the square reconstructions for p. 187 and p. 217, and the
quantified negative results for the residue.
