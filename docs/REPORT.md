# Unsolved ADFGVX messages (Childs / Lasry list) — status report

Toolkit: `src/` (Python + C). Everything below was re-derived and
verified with my own decryptor (`core2.py`, `search2.c`, `search3.c`, `coldesc.c`,
`transclimb.c`), not just copied.

## 1. Research summary

* Source: Childs, *General Solution of the ADFGVX Cipher System* (Aegean Park Press 2000);
  the 14 daily keys were recovered by Lasry/Niebel/Kopal/Wacker (Cryptologia 2017).
  Keys are valid for 3-day periods; Nov 13-15 had two RICHI keys and the "CHI" traffic
  used yet another key.
* The Klausis-Krypto-Kolumne comment thread (Feb–May 2017: Armin Krauß, Norbert Biermann,
  Thomas Bosbach, Max Baertl, George Lasry) already cracked a large part of this list by
  hand/semi-automatically. I re-implemented their edit types and verified every claim.
* Typical mutilations found in the traffic: dropped/doubled Morse symbols, whole
  5-groups dropped or duplicated by the intercept operator, hyphens = unreadable symbols,
  a letter transcribed as U/B, encryption-stage slips (e.g. a plaintext letter encoded as
  three symbols instead of two, p.132), and messages logged under the wrong day.

## 2. Verified solutions (decrypted with my code)

| Page | Key | Fix applied to ciphertext | Plaintext (cleaned) |
|---|---|---|---|
| 100 | Nov 1-3 | insert `DG` before 3rd-last group (`FGDDF`→`DGFGDDF`) | KEINE STOERUNG DURCH FEIND X MITTAGS 2 FEINDL X DIV X IM MARSCH AUF BELGRAD X |
| 105 | Nov 1-3 | group 10: drop one X; group 20: drop `DG` | GERMANIA ETAPPE KONSTANTINOPEL XX FUER MITTELMEER DIVISION ZU X TEL X NR X 62 X DIV X TELEGR X NR X 58 X ERSTELLT X 32141 X Q4 X AN X 32141 X Q4 X A X VOM X 4 X NOVEMBER ERLEDIGT X ADMIRALSTAB X 32398 X B |
| 109 | Nov 1-3 | groups 16-19 (a duplicated pair) → `XXAVV XXDDG` | O X K X M X ABENDMELDUNG X S4V4 X UNTERBRINGUNG LETZTER TEILE BEENDET X 1 WEITERER DU X DIV 5 IM MARSCH AUF BELGRADER KAVV X 2 X SONST KEINE EREIGNISSE XX ASO X K511 |
| 132 | Nov 4-6 | encryption-stage error: one superfluous `V` in the interim (pre-transposition) text | FUER EILVESE X WIEDERHOLET TELEGR X VON VIERTER PERIODE IN FUENFTER X GEBETSORDER 5 MIN X VVV |
| 146 | Nov 4-6 | insert `FVXAA` before group 10; `XAAXV XAFDX` → `XAAXX` | FUNKSTELLE KERTSCH HAT BETRIEB X 1F X RUFNAMEN RICHARD EMIL KARL X FUNKSTELLEN DORTIGEN BEREICHS BENACHRICHTIGEN X NACHRICHTENCHEF 4B X 7834 X |
| 164 (F-G-X …) | Nov 7-9 | ~40 unknown symbols; partial | … X 9 X 11 X TEMESVAR X … DIE (DIV) VON X MIRCO NACH WESTEN UND SUEDEN WEG X LEIDER WEGE VOM GEGNER BESETZT X |
| 164 (VFGAG …) | Nov 7-9 | ~40 unknown symbols; partial | EL X DIE HOEHE X 828 X O X H X L X MIRCO X SONST KEINE EREIGNISSE VON BEDEUTUNG XX … |
| 171 | Nov 7-9 | 7 small edits (see `final_verify` in report) | IN UKRAINE UND POLEN RUBELKURSE STARK STEIGEND INFOLGE BRUCHES ZWISCHEN DEUTSCHLAND UND SOWJETREGIERUNG UND ERWARTUNG DER WIEDERHERSTELLUNG RUSSLANDS DURCH DEUTSCHLAND UND ENTENTE |
| 176 ("missing 10 letters") | Nov 10-12 | insert `FVFFF` after group 3; groups 25/26 → `AFFGA ADVAX DAVVV` | DURCHBRUCH VORBEREITET X DURCHBRUCHS RICHTUNG NACH NORDEN ODER NORDOSTEN ERFOLGEN WIRD X KANN JETZT NOCH NICHT BEURTEILT WERDEN X |
| ?? (= Childs p.215, VGADA …) | Nov 22-24 | insert one 5-group after group 6 and one after group 43 | ABS X MIDIV 5 X EILMELDG X 24N X 24N X ARMADA KERTSCH X BRINGT ENTENTE FLOTTE ZWO DIVISIONEN X NEUSEELAENDER X ENGL X U X FRANZO X MIT X NUR OHL X KORPS FRISCH X 3Y52 |
| 187 (FFVXV …, "1 TL") | **new CHI key** transp. `CMBLAKOHIDENFJGP` = 3,13,2,12,1,11,15,8,9,4,5,14,6,10,7,16 ; square rows `AROT+W / H++C++ / SVU+I+ / DXBP++ / +JXNZE / LFK+G+` | none needed | RUSSISCHEN UND POLN HEERESVERKEHR VOLL ERFASSEN X WICHTIGES BESONDERS AUS POLN VERKEHR UEBER OHL STATION VERZIFFERT FUNKEN |
| ??? (AFAFF …, "2 TL") | same CHI key | none needed | SOWEIT FERNSCHREIBERVERBDG NICHT ARBEITET X REST SCHRIFTLICH X NACH CHEF 0 X 01 |

(The p.187 pair is the one Lasry recovered after Norbert's guess that both parts share a key; I
rebuilt the Polybius square from the two ciphertexts and the known plaintext and confirmed it
decrypts both parts cleanly. p.132's fix reproduces exactly when deleting one V from the
*untransposed* text — proving the error was made by the German cipher clerk, not the intercept
operator.)

## 3. Still unsolved after this session (10 cryptograms)

p.73, p.152, p.153 (both), p.158, p.170, p.176 (GGDAA…), p.189, p.198, p.217.

What was tried on each, against all 14 daily keys + the CHI key:

1. **Exhaustive 1- and 2-edit search** (`search2`): insert/delete 1-6 symbols at any two
   positions (≈10⁶ variants per key/message), scored with a German quadgram model biased
   toward WWI military vocabulary. Validated: it re-finds p.100, p.146, p.176a, p.171 on its own.
2. **3-edit grid search** on 5-group boundaries (`search3`), and a **6-step beam search**
   (`beam.py`, width 60) chaining single edits.
3. **Column-offset simulated annealing** (`coldesc`): lets every ciphertext column start
   ±7 symbols from nominal (models arbitrary dropped/added symbols anywhere). Validated on
   p.146/p.176a.
4. **Key variants**: reversed transposition keys, one element dropped/inserted, any two
   columns swapped, and every (transposition, substitution) cross-pairing between days.
5. **Unknown-key attack** (`transclimb`): SA over the permutation maximising bigram IC of the
   interim text, K = 15…23. Works on the 212-letter p.187 (recovers K=16 partially) but the
   remaining cryptograms are 84–242 symbols with many hyphens — below the practical threshold
   for ciphertext-only key recovery on a single message.

Nothing scored better than ≈ −6.0 (genuine decrypts score −4.0 … −4.8); the few "readable-looking"
fragments came with wildly non-nominal offsets and are over-fitting artifacts. Conclusion for these ten:
they are most likely in the "14 cryptograms with correct length that decrypt with no key" class that
Lasry's paper attributes to **wrong encryption** (or a key not in the list, as with the CHI pair), or
they have too many missing groups (p.153b: 15 unknowns of 108; p.189: 6 of 90).

Most promising leads if someone wants to continue:
* p.153 (VFVAX…, AXVAA…) carry a **CHI** indicator like p.187 → probably yet another CHI key.
  A joint unknown-key attack over both parts (240 symbols) might work if a crib (e.g. "NACHRICHTENCHEF",
  "OHL", "STATION") is used.
* p.73's log date (Oct 26 vs Nov 8) is ambiguous; neither the Oct 28-31 nor Nov 7-9 key works even
  with 6 edits, so it may belong to an unrecovered late-October key.

## 4. Files

* `messages.py` – transcriptions; `core2.py` – decryptor with `?` support; `adfgvx.py` – key table.
* `search2.c / search3.c / coldesc.c / transclimb.c` – the search engines (compile with `gcc -O2`).
* `quad.bin` – German quadgram log-probabilities used for scoring.
