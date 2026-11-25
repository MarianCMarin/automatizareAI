# Memoria firmei: kitul de foldere

Agenții AI nu țin minte nimic de la o conversație la alta. Firma ține minte pentru ei, în fișiere simple, pe care le citește și un om. Kitul are 3 niveluri: o hartă, câte o fișă pe domeniu și un jurnal.

## Structura

```
firma/
├── CLAUDE.md                  ← harta: ce există, unde stă, ce nu se amestecă (o pagină)
├── regulament.md              ← regulamentul agentului (ton, prețuri, „întreabă-mă întâi”)
├── vanzari/
│   ├── context.md             ← fișa domeniului: ce știm, ce s-a decis, ce e interzis
│   ├── oferta.md              ← serviciile și lista de prețuri valabilă
│   └── sabloane/              ← răspuns la cerere, ofertă, follow-up
├── marketing/
│   ├── context.md
│   ├── ton.md                 ← cum sună firma, cu 3 exemple bune și 3 de evitat
│   └── cuvinte_interzise.md
├── clienti/
│   └── <nume-client>/
│       └── fisa.md            ← câte o fișă pe fiecare client mare
├── administrativ/
│   └── context.md             ← facturare, contabil, termene (fără parole!)
└── istoric/
    └── 2026-11-25_sesiune.md  ← un fișier după fiecare sesiune de lucru
```

## Ce scrii în fiecare

### `CLAUDE.md` (harta, maximum o pagină)

```markdown
# Harta firmei [Nume]

Citește întâi acest fișier, apoi `regulament.md`, apoi fișa domeniului, apoi ultimul fișier din `istoric/`.

| Domeniu | Folder | Ce e acolo |
|---|---|---|
| Vânzări | vanzari/ | oferta, prețurile, șabloanele |
| Marketing | marketing/ | tonul, cuvintele interzise |
| Clienți | clienti/ | câte o fișă pe client mare |
| Administrativ | administrativ/ | facturare, termene |

Nu amesteca: [ex. „prețurile pentru firme cu cele pentru persoane fizice”].
Ce nu există încă: [ex. „nu avem magazin online”] - nu-l presupune.
```

### `<domeniu>/context.md` (fișa domeniului)

```markdown
# Vânzări - fișa domeniului

## Ce știm (fapte, cu data)
- [25.11.2026] Cele mai multe cereri vin din formularul site-ului.

## Ce s-a decis (cu data și cine)
- [20.11.2026, patronul] Ofertele peste 2.000 lei le aprob eu.

## Ce e interzis
- Reduceri fără acord.

## Întrebări deschise
- Trecem la un CRM sau rămânem pe tabel?
```

### `clienti/<nume>/fisa.md`

```markdown
# [Nume client]
- Cine e, ce cumpără, de când.
- Persoana de contact și cum preferă să fie contactată (fără parole, fără date de card).
- Ce s-a promis și până când.
- Ce nu-i place (ex. „nu vrea apeluri după 17:00”).
- Ultima discuție: [data], [ce s-a stabilit].
```

### `istoric/AAAA-LL-ZZ_sesiune.md`

```markdown
# Sesiunea din [data]
## Ce s-a făcut
## Unde stă fiecare lucru (căi de fișiere)
## Ce rămâne de decis de patron
```

## Trei reguli care țin kitul viu

1. **Harta trimite explicit la fișe.** Agentul citește automat doar fișierul de la rădăcină; restul îl găsește pentru că harta îi spune unde.
2. **Jurnalul se scrie la final, de fiecare dată.** Fără el, a doua zi o iei de la zero.
3. **Parolele și datele de card nu intră niciodată în aceste fișiere.** Ele stau într-un manager de parole sau într-un fișier separat, pe care agentul nu-l citește.

## Cât durează

Prima variantă: o oră, cu harta, regulamentul și o singură fișă (domeniul care te costă cele mai multe ore; testul gratuit „Unde pierde firma ta ore” îți spune care e). Restul se adaugă pe măsură ce agentul primește sarcini noi.

Marian Cristian Marin · automatizare cu AI pentru firme
