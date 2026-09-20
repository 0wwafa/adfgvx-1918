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

## Decoded messages

All twelve verified decrypts (regenerate with `src/verify.py`; exact ciphertext fixes in
[`docs/SOLUTIONS.md`](docs/SOLUTIONS.md)). `X` is the German telegraphic full stop / word separator.

| Childs p. | Key | German plaintext | English |
|---|---|---|---|
| 100 | Nov 1–3 | KEINE STOERUNG DURCH FEIND X MITTAGS 2 FEINDL X DIV X IM MARSCH AUF BELGRAD X | No interference by the enemy. At noon two enemy divisions on the march towards Belgrade. |
| 105 | Nov 1–3 | GERMANIA ETAPPE KONSTANTINOPEL XX FUER MITTELMEER DIVISION ZU X TEL X NR X 62 X DIV X TELEGR X NR X 58 X ERSTELLT X 32141 X Q4 X AN X 32141 X Q4 X A X VOM X 4 X NOVEMBER ERLEDIGT X ADMIRALSTAB X 32398 X B | Germania [ship/station], Constantinople rear-area command. For the Mediterranean Division. Re telegram no. 62, division telegram no. 58: settled. 32141 Q4 to 32141 Q4 A of 4 November — dealt with. Admiralty Staff 32398 B. |
| 109 | Nov 1–3 | O X K X M X ABENDMELDUNG X S4V4 X UNTERBRINGUNG LETZTER TEILE BEENDET X 1 WEITERER DU X DIV 5 IM MARSCH AUF BELGRADER KAVV X 2 X SONST KEINE EREIGNISSE XX ASO X K511 | O.K.M. [Oberkommando Mackensen] evening report S4V4. Quartering of the last elements completed. 1. One further [unit]; 5th Division on the march to the Belgrade cav. [area]. 2. Otherwise no events. ASO [Sevastopol] K511. |
| 132 | Nov 4–6 | FUER EILVESE X WIEDERHOLET TELEGR X VON VIERTER PERIODE IN FUENFTER X GEBETSORDER 5 MIN X VVV | For Eilvese [radio station]: repeat the telegram of the fourth period in the fifth. Prayer order [pause] 5 min. VVV. |
| 146 | Nov 4–6 | FUNKSTELLE KERTSCH HAT BETRIEB X 1F X RUFNAMEN RICHARD EMIL KARL X FUNKSTELLEN DORTIGEN BEREICHS BENACHRICHTIGEN X NACHRICHTENCHEF 4B X 7834 X | Radio station Kertch is operational. 1F. Call sign R-E-K. Notify the radio stations of that area. Chief Signals Officer 4B. 7834. |
| 164 (F-G-X…) *partial* | Nov 7–9 | … X 9 X 11 X TEMESVAR X … DIV VON X MIRCO NACH WESTEN UND SUEDEN WEG X LEIDER WEGE VOM GEGNER BESETZT X | … 9 [Nov] 11 [h] Temesvár … division from [Prince] Mirko's [area] away to the west and south. Unfortunately the roads are occupied by the enemy. |
| 164 (VFGAG…) *partial* | Nov 7–9 | EL X DIE HOEHE X 828 X O X H X L X MIRCO X SONST KEINE EREIGNISSE VON BEDEUTUNG XX … | … hill 828. O.H.L. [Supreme Command]. Mirko. Otherwise no events of importance. |
| 171 | Nov 7–9 | IN UKRAINE UND POLEN RUBELKURSE STARK STEIGEND INFOLGE BRUCHES ZWISCHEN DEUTSCHLAND UND SOWJETREGIERUNG UND ERWARTUNG DER WIEDERHERSTELLUNG RUSSLANDS DURCH DEUTSCHLAND UND ENTENTE | In Ukraine and Poland rouble exchange rates rising sharply as a result of the break between Germany and the Soviet government and the expectation that Russia will be restored by Germany and the Entente. |
| 176 (VVAVD…) | Nov 10–12 | DURCHBRUCH VORBEREITET X DURCHBRUCHSRICHTUNG NACH NORDEN ODER NORDOSTEN ERFOLGEN WIRD X KANN JETZT NOCH NICHT BEURTEILT WERDEN X | Break-out prepared. Whether the break-out will go north or north-east cannot yet be judged. |
| 215 ("page ??") | Nov 22–24 | ABS X MIDIV 5 X EILMELDG X 24N X 24N X ARMADA KERTSCH X BRINGT ENTENTE FLOTTE ZWO DIVISIONEN X NEUSEELAENDER X ENGL X U X FRANZO X MIT X NUR OHL X KORPS FRISCH X 3Y52 | Sender: Military Division 5. Urgent report, 24 Nov. Fleet at Kertch: the Entente fleet is bringing two divisions — New Zealanders, English and French. For OHL only. Corps [is] fresh. 3Y52. |
| 187 (part 1) | CHI key, 13 Nov | RUSSISCHEN UND POLN HEERESVERKEHR VOLL ERFASSEN X WICHTIGES BESONDERS AUS POLN VERKEHR UEBER OHL STATION VERZIFFERT FUNKEN | Intercept Russian and Polish army traffic in full. Send important items, especially from Polish traffic, enciphered by radio via the OHL station |
| "page ???" (part 2) | CHI key, 13 Nov | SOWEIT FERNSCHREIBERVERBDG NICHT ARBEITET X REST SCHRIFTLICH X NACH CHEF 0 X 01 | as long as the teleprinter link is not working. The rest in writing. Chief Signals Officer 0.01. |
| 217 | TRUPPENVERSCHIEBUNG | EIN ENGLISCHER KREUZER EINLIEG X SEWASTOPOL X S4STEN [=24STEN] X EIN GESCHWADER DER X ALLIIERTEN FOLGT 26STEN X | An English cruiser put in at Sevastopol on the 24th. A squadron of the Allies follows on the 26th. |

The p.217 dates match the arrival of HMS *Canterbury* at Sevastopol on 24 November 1918 and of the
Allied squadron on the 26th.

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
