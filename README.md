# Himari

**Himari** contains some GitHub Actions for processing various NationStates things for Hare and other card things. The project consists of multiple components:

1. **Dump Parser:** Parses NationStates regional and nation dumps, extracting the necessary data for use in Hare and cte statuses.
2. **Ledger:** Tracks the cte status of nations, legendary cards, and top 100 card players.
3. **Daily STats:** Updates a CSV containing trade stats and generates graphs to visualize the data.

New data is generated daily at **11 PM UTC-7**.

### What is the sorting order for the Ledger?

The sorting order defaults to showing CTE (ceased-to-exist) nations first, followed by non-CTE nations. When sorting by season, it will show:

1. CTE nations for the selected season.
2. Non-CTE nations for the selected season.
3. Non-CTE nations without the selected season.
4. CTE nations without the selected season.

### Why is data generated at 11 PM PST?

The CTE checker relies on NationStates nation dumps, which are typically available around 10:30 PM PST. The script runs at 11 PM PST to ensure the dumps exist before processing.

![himari-eimi](public/himari-eimi.jpg)
