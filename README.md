[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Wedspierre/news-image-20261124-entry/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Wedspierre/news-image-20261124-entry/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# Tuesday 24 November 2026: 36 stories, 8 regions — Ukraine sinks Russian warship off Libya, Huang back at Nvidia, FIFA names 2031 and 2035 hosts

A one-page newspaper front page summing up Tuesday 24 November 2026's world
news in a single 1024×1024 image: a masthead, a Monday-close market ticker,
one lead story, six story cards and 29 one-line briefs across 8 regions.
Every figure on the page is attributed to its reporting source.

The lead is Ukraine's sinking of the Russian corvette *Merkury* at Benghazi,
confirmed by President Zelenskyy on 23 November: seven sea drones, the cargo
ship MV Angara hit and a Ka-27 helicopter destroyed, 2,400 km from the front
line. The cards cover Nvidia reinstating Jensen Huang as CEO (+31.5% in a
day, +$952bn of value), FIFA naming the 2031 and 2035 Women's World Cup
hosts, the Cikande factory fire toll reaching 24 dead, Denmark's Supreme
Court backing "ghetto law" evictions, the Oxfam/CEOBS report finding
contamination indicators across over 99% of Gaza, and hoax bomb threats
sent to about 450 schools in Germany and Denmark.

## How it is built

`draw.py` (Python 3 + PIL, Liberation fonts, no network, no randomness)
renders `entry.png` deterministically — two runs produce byte-identical
output. `main.ts` (Node 22, standard library only) validates the image
(PNG magic, ≤ 1 MiB, ≤ 1024×1024) and copies it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), unlinking any existing
target first and verifying the copied bytes match.

## Verify locally

```sh
python3 draw.py
node --check main.ts
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 node main.ts
MAKEFUN_OUTPUT_DIR=out2 node main.ts
sha256sum entry.png out1/entry.png out2/entry.png   # all three must match
```

## Sources

Reuters, AP, CNN, AFP, FIFA, Oxfam, UKMTO, Addis Standard, PANA, Times of
India, CNET, Geopolitiki — reporting of 23–24 November 2026. See
`TRANSCRIPT.md` for the per-story source list and verification results.
