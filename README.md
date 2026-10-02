# Little-Miss-Cookbook
## Expanded reference collections (1 October 2026)

The painted hero has keyboard-accessible hotspots over the pot, vegetables, jars,
glass and notebook. The "Show me where" button reveals their labels. On narrow
screens the whole original painting remains visible, with larger controls below.

The Food & recipe archive contains **54,843 historical recipe records** from
[Open Recipe Archive](https://github.com/AdamBouhmad/open-recipe-archive), plus
**7,793 USDA SR Legacy food records** from the April 2018 release. Counts are
source records, not distinct ingredient species, kitchen-tested recipes or modern
lessons. The modern practice collection now has 52 recipes (including 14 drinks) and 14 lessons;
**the requested 6,000+ in each area is not yet fulfilled**.

Historical text and provenance are preserved. These records may contain obsolete
or unsafe methods, transcription errors and missing measurements; they are a
reference archive, not modern cooking guidance. Source URLs and licence metadata
appear beside every record. An optional keyword filter hides mentions of nuts,
banana and plantain by default, but cannot establish allergy suitability.

USDA nutrition values are per 100 g of the described food, including its stated
raw/cooked form; missing values are not zero. The imported six nutrient fields
are identified in `scripts/import-reference-data.py`. SR Legacy is historical
composition data, not a live branded-food catalogue.

`data/manifest.json` stores exact counts by collection/group and the pinned
archive source commit. `data/ARCHIVE-LICENSE.md` preserves the upstream licence.
USDA FoodData Central data are public domain. Rebuild with local source downloads:

```
python scripts/import-reference-data.py /path/to/open-recipe-archive /path/to/USDA-CSV-directory
```

Data are gzip-compressed static JSON. The browser loads indexes on demand,
displays 18 results per page, and fetches recipe bodies in 500-record chunks.
A modern browser with `DecompressionStream` is required for the reference section.
Loading failures show a retry action. Search, food groups/collections, exclusions,
pagination, source dialogs and historical bookmarks work locally; bookmarks are
separate from modern recipe favourites.

## Interactive expansion, 2 October 2026

Added 24 distinct authored recipes: 12 drinks and 12 food recipes, all with quantities, equipment, visual cues, estimated timings, science and troubleshooting. These are authored practice recipes, not claims of kitchen testing. Existing guided cooking, timers, serving controls, checklists and favourites apply to every modern recipe.

Historical records now have a step-through source reader with ingredient checklists, reading progress and adaptation notes saved per record on this browser. It parses only numbered directions from the source. Unparseable records retain full source text. It does not invent times or certify historical instructions for current cooking.
