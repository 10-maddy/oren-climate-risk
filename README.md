# Nimbus climate exposure (MVP 1 prototype)

A prototype built for Oren's PM assessment, *Climate risk: from idea to prototype*. It answers one question for a fictional customer, Meera Iyer, Head of Sustainability at Nimbus Cement Ltd:

> What is our business exposure to climate events today and by 2040?

The company and its nine plants are invented for the exercise. The hazard data is real and comes from public sources.

## What it shows

With the default assumptions, **70.2% of revenue (Rs 6,782 cr of Rs 9,658 cr)** comes from plants rated High for heat or water stress today. Counting the grinding units those plants feed with clinker, it is **91.0% (Rs 8,790 cr)**. At a heat cut-off of 60 hot days a year the figures fall to 57.0% and 65.8%.

"Exposure" here means the revenue sitting at High-rated plants. It is where revenue sits, not an estimate of losses.

## What's in the prototype

| Screen | What it does |
| :--- | :--- |
| Exposure | Headline sentence, split bar, summary tiles that filter the plant table, and a Today / About 2040 toggle with a heat cut-off slider |
| Plant drawer | Opens from any plant row. Shows why the plant is rated as it is, the heat history, the water-stress score, river data and clinker dependency |
| What if | Stops one plant for a chosen number of days and shows the revenue interrupted, including grinding units that run out of clinker |
| Next version | What was cut from v1 and why, with a link to the feedback form |
| Feedback | Google Form for MVP 1 users |
| Handover | One-page build spec for a developer. Can be printed to PDF or downloaded as Markdown |
| Sources | Where each figure comes from, the cautions, nine labelled assumptions and a plain-English glossary |

Every technical term is underlined and explains itself on hover, tap or keyboard focus.

## How exposure is rated

| Rule | Detail |
| :--- | :--- |
| Hot days | Days a year with a daily high of 40 °C or more. Today is the 2016 to 2025 average. About 2040 is today plus the median change across three climate models, never a model's own absolute value |
| Heat rating | High at 55 or more days (adjustable 40 to 70), Medium from 25, otherwise Low |
| Water rating | High if the state's Aqueduct score is 4.0 or more and the plant uses local fresh water. Medium from 3.0. Desalinated and municipal supply count as Low |
| Overall | The higher of heat and water |
| Fed by a High plant | A grinding unit whose kiln plant is rated High |
| Not rated | River flood is shown for today only. Cyclone is not scored and links out to ISRO Bhuvan |

## Data sources

| Source | Used for | Caution |
| :--- | :--- | :--- |
| [NASA POWER](https://power.larc.nasa.gov/) | Hot days, 2001 to 2025 | Grid of about 50 km. Smooths local extremes |
| [Open-Meteo Climate API](https://open-meteo.com/en/docs/climate-api) | Change in hot days to about 2040, three models | No emissions-scenario choice. Ends in 2050. Models disagree on direction at four plants |
| [Open-Meteo Flood API](https://open-meteo.com/en/docs/flood-api) | River flow, 1997 to 2025 | The 5 km cell often misses the river. Empty before 1997 |
| [WRI Aqueduct 4.0](https://www.wri.org/data/aqueduct-40-country-rankings) | Water stress by state | State average, not the plant's aquifer. WRI says the indicators are not validated |

All hazard figures are third-party model data, pulled on 22 Nov 2026, and can change when providers update their models. The prototype says so on every screen.

## Run it

The prototype is a single self-contained HTML file with the data embedded. It has no build step, no login and no runtime network calls apart from the page fonts, which fall back to system fonts if blocked.

1. Open `index.html` in a browser, or
2. Deploy the folder to Vercel (`vercel --prod`) or any static host.

To use your own feedback form, change the `FORM_URL` line near the top of the script.

## Project files

| File | Purpose |
| :--- | :--- |
| `index.html` | The prototype |
| `handover-doc.pdf` | The one-page developer ticket, printed from the Handover screen |
| `scripts/pull_projections.py` | Downloads the 2040 climate-model projections from Open-Meteo (standard library only) |

## Known limits

- The plant data is invented, and asset value is a rough gross block.
- Heat cut-offs and water-stress lines are assumptions, not Nimbus policy. At a cut-off of 60, Baloda Bazar drops out of High and takes two grinding units with it.
- River flood and cyclone are not projected to 2040.
- Grinding units are assumed fully dependent on their kiln for clinker.
- Revenue is not profit. A margin or EBITDA base may suit an auditor better.

## Built with

I worked with Claude in a single long chat. I made the scope calls (physical risk first, hazards weighted by what each plant does, exposure rather than loss) and the product direction. Claude pulled and checked the data, built the rating model and wrote the prototype. The headline numbers were recomputed in code and match the acceptance figures. How I used AI, including where it was wrong, is covered in the process note.

Tanmay, 22 Nov 2026
