# PolyBot - Polymarket alpha scanner

A Python bot that scans active Polymarket prediction markets, scores each one
for a possible edge, sends the best candidates to Perplexity for a short
research pass, and writes a JSON report that a static three-tab dashboard
reads.

## How it works

1. `PolymarketScanner` pulls active markets from the public Gamma API.
2. `AlphaDetector` scores each market from liquidity, 24h volume, spread and
   price, and drops anything under the thresholds at the top of
   `polymarket_alpha_bot.py` (`MIN_LIQUIDITY`, `MIN_VOLUME_24H`, `MAX_SPREAD`,
   `MIN_ALPHA_SCORE`).
3. `PerplexityResearcher` asks the `sonar-pro` model for a short research
   note on the top markets and parses a position, a confidence level and the
   reasoning out of the reply. A rule-based fallback runs if the API is not
   available.
4. `AlphaBot` combines score and confidence into a verdict
   (`STRONG_BUY` / `BUY` / `NEUTRAL` / `REJECT`), suggests a position size,
   and writes `reports/latest_report.json` plus a text summary.
5. `dashboard_triple.html` reads the report and shows it in three tabs
   (all markets, serious, meme).

## Run

```bash
pip install -r requirements.txt
export PERPLEXITY_API_KEY=...   # never commit this; the bot reads it from the environment
python polymarket_alpha_bot.py
./view.sh                       # serve the dashboard on http://localhost:8000
```

`run.sh` / `view.sh` are the Linux launchers; `LAUNCH_SINGLE.bat` and
`setup_nightly_single.bat` do the same on Windows, including a nightly
Task Scheduler run. See `SETUP_GUIDE.md`, `NIGHTLY_AUTOMATION_GUIDE.md` and
`COST_OPTIMIZATION.md` for details.

## Notes

This is a research tool, not trading advice. The reports in `reports/` and
`public/` are sample output from past runs.
