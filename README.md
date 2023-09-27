# Missing Migrants

### Visualizing IOM data on people who went missing or lost their lives during migration

Since 2014, the [**Missing Migrants Project**](https://missingmigrants.iom.int/) of the International Organization for Migration (IOM) has documented more than 58,000 people who died or went missing during migration (as of Sep 17th 2023: 58,811). The actual number is likely much higher.

This repository contains the code for a visualization made with **Svelte** and **d3** of that horrendous number. Each circle in this graph represents one of more than 13,000 incidents from the IOM database where at least one migrant died or went missing. The circle's size indicates the number of people affected. Color and vertical position denote the region of occurrence.

The Mediterranean has by far been the region where most deaths and disappearances have been documented: More than 28,000.

Find an **interactive version** here: https://yotka.org/missing-migrants/
(Disclaimer: it probably takes some time to load.)

The [Dataset](https://missingmigrants.iom.int/downloads) used for this project is the result of meticulous work by the Missing Migrants Project. It contains more than 13,000 incidents with information on where they happened, how many people died, which migration route was used, and where the information came from. Read more about the [methodology](https://missingmigrants.iom.int/methodology) here.
