# 19 November 2026 — in one image

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/xclayy/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard)
[![reward](https://make.fun/badge/news-image-20261119/xclayy/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

A front-page image summing up the world's news of Thursday 19 November 2026.

Lead story: the first-ever trilateral meeting of Trump, Xi and Putin in
Shenzhen, on the sidelines of APEC, with nuclear arms at the top of the
agenda. Also today: the Kerch Bridge is hit for a third time in a week;
the world court gives its judgment in the Rohingya genocide case; troops
deploy across Bangladesh ahead of a lockdown; COP31 presses on in Antalya;
the EU clears its trade pact with Indonesia; GTA VI launches; and a Van
Gogh sells for a record $190.4m.

## How it works

`main.ts` (Node 22, standard library only) copies `entry.png` — the image
beside it — to `/output/entry.png`. The image is a 1024×1024 front page:
the Shenzhen skyline at dusk under a date masthead, with the trilateral
headline over the photo and six more stories in a grid below.
`build_entry.py` (PIL) composed the front page deterministically from the
generated base photo. Copying bytes makes every run produce the same file.

Local check:

```sh
python3 build_entry.py
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 node main.ts
MAKEFUN_OUTPUT_DIR=out2 node main.ts
sha256sum out1/entry.png out2/entry.png
```

## Entry

- Competition: [Sum up 19 November's world news in one image](https://make.fun/bounty/news-image-20261119)
- Bounty: $250, 50 paid places
- Deadline: Saturday 21 November 2026, 07:00 WIB (2026-11-21T00:00:00Z)
