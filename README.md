[![news](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Masrukhan25/news-image-20261125-acct1/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Masrukhan25/news-image-20261125-acct1/reward.svg)](https://make.fun/bounty/news-image-20261125)

# The World in One Day — Wednesday 25 November 2026

A single 1024×1024 newspaper front page summing up 25 November 2026 in **48 stories from 8 regions**, drawn as flat-vector illustration with PIL. No news feed was used at grade time: the page is pre-built and this entrypoint only copies it into place.

## The 9 heroes

1. **Trump unveils new tariffs on 14 economies** — a container ship under a red "UP TO 35%" stamp. Vietnam up to 35%, India 25%, China 20%, EU 15%.
2. **Chip stocks crash: KOSPI −6.2%** — an "AI" chip falling over a plunging red chart. Samsung −9.9%, SK Hynix −11.1%.
3. **First Pakistani astronaut reaches Tiangong** — a rocket climbing to the Tiangong station above Earth. Shenzhou-24 docked 03:56 UTC; Muhammad Zeeshan Ali is the first foreign astronaut on the station.
4. **Cartagena: all 30 hostages freed** — the Éxito supermarket storefront behind police tape. 17-hour siege ended by a 01:30 raid.
5. **Houthis hit Saud's biggest refinery** — Ras Tanura burning under a drone. Brent settled +3.5% at $94.61.
6. **Iowa blast done: zero lead found** — a real explosion cloud over farmland. 9,500 lbs of lead azide detonated at 09:00 CST; EPA monitors found no airborne lead.
7. **US cyber wave: CIA, ODNI, FinCEN hit** — an agency building beside a hacked screen flashing BREACH.
8. **NATO vows space defense** — a satellite on a red orbit above Earth. A nuclear blast in orbit could disable a third of low-orbit satellites.
9. **Vaibhav 204 off 53 balls** — a batsman under floodlights. Fastest List A double century, a world-record 28 sixes.

## Also on the page

- **The Day in UTC** — a timeline strip from the 00:08 KOSPI sidecar to the 23:30 Army all-clear.
- **The Day in Numbers** — 35% · −6.2% · 30 · 9,500 · $94.61 · 204.
- **Where It Happened** — a full-width world map with 28 numbered places, one dot per hero and per numbered story.
- **Also on 25 November** — stories 10–48, numbered and grouped by region.
- **Date Check** — stories deliberately left out because they happened on other days (Anthropic's $2T IPO, the Villavicencio car bomb, missiles over Poland, the Tarwekamp blast).
- Every card carries a CONFIRMED / REPORTED label and its source.

## Build

`build.py` draws the whole page with PIL (DejaVu fonts, deterministic — two runs produce a byte-identical PNG). `main.py` copies the pre-built `entry.png` to `/output/entry.png` using only the Python standard library.
