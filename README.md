![missing-migrants-preview](https://github.com/yotkadata/missing-migrants/assets/7913590/5381e452-acf6-4bc6-9541-9a83a52ccef8)

# Missing Migrants

### Visualizing IOM data on people who went missing or lost their lives during migration

Since 2014, the [**Missing Migrants Project**](https://missingmigrants.iom.int/) of the International Organization for Migration (IOM) has documented more than 65,000 people who died or went missing during migration (as of Jun 6 2024: 65,384). The actual number is likely much higher.

This repository contains the code for a visualization made with **Svelte** and **d3** of that horrendous number. Each circle in this graph represents one of more than 13,000 incidents from the IOM database where at least one migrant died or went missing. The circle's size indicates the number of people affected. Color and vertical position denote the region of occurrence.

The Mediterranean has by far been the region where most deaths and disappearances have been documented: More than 29,000.

### Data

The [Dataset](https://missingmigrants.iom.int/downloads) used for this project is the result of meticulous work by the Missing Migrants Project. It contains more than 13,000 incidents with information on where they happened, how many people died, which migration route was used, and where the information came from. Read more about the [methodology](https://missingmigrants.iom.int/methodology) here.

### Interactive version

Find an **interactive and automatically updated** version here: https://yotka.org/missing-migrants/
(Disclaimer: it probably takes some time to load.)

### Static version

![static version](https://github.com/yotkadata/missing-migrants/raw/main/svelte_app/public/static-graph-missing-migrants.png)
