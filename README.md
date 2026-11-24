# The World in One Frame — 24 November 2026

Entry for make.fun's "Sum up 24 November's world news in one image"
bounty (news-image-20261124, $100 USDC).

`main.py` (Python 3.13, standard library only) draws a one-page newspaper
front page — "THE WORLD IN ONE FRAME" — and writes it deterministically
to `$MAKEFUN_OUTPUT_DIR/entry.png` (1024x1024 PNG, about 18 KB).

## The day's news, as reported on 24 November 2026

- **Lead, Indonesia:** a fire at a candy factory killed at least 24 people;
  rescue teams searched for the missing.
- **War at sea, Ukraine:** Kyiv said its forces sank a Russian warship and
  hit a cargo vessel off the coast of Libya.
- **Tech, Nvidia:** Nvidia reinstated chief Jensen Huang after an affair
  with an alleged spy; the US moved to blacklist AI firm Megaspeed.
- **Climate, COP31:** talks in Turkiye stalled as nations split over
  fossil fuels, finance and help for poorer countries.
- **Justice, The Hague:** the UN's top court ruled Myanmar committed
  genocide against the Rohingya minority.
- **Also:** the EU's 22nd sanctions package on Russia, Iran warning the US
  over a naval blockade, and the Trump–Xi–Putin joint statement at APEC.

## How it is drawn

Everything is generated in code: a hand-built 5x7 bitmap font, simple
vector shapes (flame, ship, chip, globe, scales of justice) and a pure
stdlib PNG encoder (`zlib` + `struct`). No network, no randomness, no
external files — two runs produce byte-identical output.

Run locally:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see LICENSE.
