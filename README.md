# Path Relinking za problem trgovackog putnika (TSP)

Projekat iz predmeta Racunarska inteligencija na Matematickom fakultetu
Univerziteta u Beogradu.

## Problem

Problem trgovackog putnika (TSP) trazi najkracu zatvorenu rutu koja prolazi kroz
svaki grad tacno jednom i vraca se na pocetni. Posmatra se simetricni Euklidski
TSP (gradovi su tacke u ravni). TSP je NP-tezak, pa se za vece instance koriste
metaheuristike koje nalaze resenja bliska optimalnom.

## Resenje

Implementiran je GRASP (Greedy Randomized Adaptive Search Procedure) u kombinaciji
sa Path Relinking-om kao strategijom intenzifikacije. GRASP gradi i popravlja
resenja, Path Relinking povezuje dva dobra resenja trazeci jos bolje "izmedju"
njih, a elite skup cuva najbolja resenja. Sve glavne komponente implementirane su
od nule u Pythonu; matplotlib se koristi samo za vizualizaciju.

## Detalji implementacije

- Kodiranje resenja: ruta je permutacija indeksa gradova, sa implicitnim povratkom
  sa poslednjeg na prvi grad.
- Funkcija cilja: ukupna duzina rute (suma Euklidskih rastojanja susednih gradova).
- GRASP konstrukcija: u svakom koraku se formira lista kandidata (RCL) od gradova
  cije je rastojanje ispod praga `cmin + alpha * (cmax - cmin)`, pa se bira nasumicno
  iz nje. Parametar `alpha` kontrolise odnos pohlepnosti i nasumicnosti.
- Lokalna pretraga: 2-opt, koji obrce segment rute kada se time skracuje ukupna duzina.
- Path Relinking: atribut resenja je grana (neuredjeni par gradova). U svakom koraku
  bira se 2-opt potez koji uvodi granu vodeceg resenja, cime se broj zajednickih grana
  monotono povecava i postupak je zagarantovano zavrsen.
- Elite skup: fiksne velicine; novo resenje ulazi ako je dovoljno razlicito (po broju
  razlicitih grana) i bolje od najgoreg u skupu.

Glavna funkcija `grasp_pr` (u `src/grasp.py`) prima parametre `iterations`, `alpha`,
`elite_size`, `min_diff`, `use_pr`, `variant` i `seed`.

## Struktura projekta

```
src/
  tsp.py             ucitavanje instance, matrica rastojanja, duzina rute
  baselines.py       nearest-neighbor heuristika
  local_search.py    2-opt lokalna pretraga
  construction.py    GRASP pohlepno-nasumicna konstrukcija
  path_relinking.py  Path Relinking (forward, backward, back-and-forward, mixed)
  elite.py           elite skup (najbolja i raznovrsna resenja)
  grasp.py           glavna petlja: konstrukcija -> 2-opt -> PR -> elite
  experiments.py     poredjenje metoda preko vise instanci i seed-ova
  visualize.py       crtanje rute i krive konvergencije
data/                TSPLIB instance (berlin52, eil51, st70, kroA100)
results/             sacuvane tabele i grafici
```

## Pokretanje

Potreban je Python 3 i matplotlib.

```
pip install matplotlib
```

Eksperimenti (tabela poredjenja metoda):

```
python src/experiments.py
```

Vizualizacija (ruta i konvergencija za berlin52):

```
python src/visualize.py
```

## Path Relinking varijante

- forward: ide od pocetnog ka vodecem resenju
- backward: ide u suprotnom smeru
- back-and-forward: radi oba smera i uzima bolji
- mixed: krece iz oba kraja istovremeno i spaja ih u sredini

## Rezultati

Poredjenje je radjeno preko vise seed-ova na cetiri TSPLIB instance. Prosecni
gap do poznatog optimuma (manje je bolje):

| instanca | GRASP bez PR | najbolja PR varijanta |
|----------|--------------|-----------------------|
| eil51    | 2.70%        | 1.45% (mixed)         |
| berlin52 | 3.92%        | 0.03% (back-and-forward) |
| st70     | 2.05%        | 1.10% (forward)       |
| kroA100  | 3.72%        | 0.33% (back-and-forward) |

Path Relinking poboljsava rezultat na svakoj testiranoj instanci u odnosu na
cist GRASP, uz vece vreme izvrsavanja. Varijanta back-and-forward je u proseku
najkvalitetnija, ali i najsporija jer radi oba smera.

## Skup podataka

Koriscene su standardne TSPLIB instance sa poznatim optimalnim resenjima.

## Autor

Uros Kovacevic 76/2021
