# The Daily Signal — Friday 20 November 2026 in one image

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/c/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/alasramus24-debug/makefun-news-image-20261120-v2/rank.svg)](https://make.fun/c/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/alasramus24-debug/makefun-news-image-20261120-v2/reward.svg)](https://make.fun/c/news-image-20261120)

An entry for make.fun's [news-image-20261120](https://make.fun/c/news-image-20261120)
bounty: sum up the world news of **Friday 20 November 2026** in one image.

## The edition

One newspaper page, dated Friday 20 November 2026, carrying the day's stories:

- **Shenzhen (hero)** — Trump, Xi and Putin hold their first trilateral summit
  and issue a four-point peace declaration.
- **New York** — Anthropic soars in a record stock-market debut, the first pure
  AI company to list, while Wall Street slides anyway.
- **The Hague** — the World Court (ICJ) rules Myanmar committed genocide
  against the Rohingya in its 2017 campaign, the first such finding against a
  state.
- **Strait of Hormuz** — Iran escalates tanker attacks, and a Houthi missile
  hits Riyadh's tallest tower.
- **In the ticker** — the UK pledges 1,000+ drones for Ukraine in a £260M
  package; Ukraine hits the Kerch Bridge again; European allies in Berlin say
  they are ready for talks with Russia; a COP31 row as fossil fuels drop out of
  the draft deal; Cyclone Xavier tracked in the Pacific.

## How it runs

`main.py` (Python 3.13, standard library only) validates the bundled
`entry.png` and copies it, byte for byte, into `$MAKEFUN_OUTPUT_DIR`:

    MAKEFUN_OUTPUT_DIR=out python3 main.py

The image itself is drawn by `compose.py` with PIL — every headline, flag and
rule is a shape or type, no photographs — and committed as `entry.png`:

    python3 compose.py
