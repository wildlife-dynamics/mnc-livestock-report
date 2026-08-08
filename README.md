# MNC Livestock Report — User Guide

This guide walks you through configuring and running the MNC Livestock Report workflow, which processes mobile boma movement, cattle count, livestock predation, and illegal grazing events from EarthRanger to produce tabular CSV reports, interactive maps, and a dashboard.

---

## Overview

The workflow delivers, for each run:

**CSV tables**
- **mobile_boma_movement_summary_table.csv** — daily count of unique mobile boma movement events
- **total_cattle_count_summary_table.csv** — cattle counts per grazing zone per date, with a total column computed by the workflow
- **total_livestock_predation_summary_table.csv** — daily count of unique livestock predation events
- **livestock_predation_summary_table.csv** — detailed predation records by species, suspected predator, and total animals affected

**Maps (HTML + PNG)**
- **boma_movement_map** — point map of mobile boma locations over the grazing zones, parcels, and conservancy boundary
- **livestock_predation_events** — point map of predation incidents over the same base layers, coloured by livestock species
- **illegal_grazing_map** — point map of illegal grazing incidents over the same base layers

**Dashboard**

A dashboard combining the three maps above and the two count-summary tables (cattle count, livestock predation) as interactive widgets.

---

## Prerequisites

Before running the workflow, ensure you have:

- Access to an **EarthRanger** instance with `mobile_boma_rep`, `cattle_count`, `livestock_predation_rep`, and `illegal_grazing_rep` events recorded for the analysis period
- Network access to **Dropbox** so the workflow can download the MNC conservancy boundary and parcels files at runtime

---

## Step-by-Step Configuration

### Step 1 — Add the Workflow Template

In the Ecoscope app, navigate to the **Workflow Templates** tab and click **Add Workflow Template** (top-right). In the **Github Link** field that appears, paste the repository URL:

```
https://github.com/wildlife-dynamics/mnc-livestock-report.git
```

Then click **Add Template** to register the template.

---

### Step 2 — Configure the EarthRanger Connection

Navigate to **Data Sources** and click **Connect**. The **Connect Ecoscope to EarthRanger** dialog will open. Fill in the form:

| Field | Description |
|-------|-------------|
| Data Source Name | A label to identify this connection (e.g. `Mara North Conservancy`) |
| EarthRanger URL | Your instance URL (e.g. `your-site.pamdas.org`) |
| EarthRanger Username | Your EarthRanger username |
| EarthRanger Password | Your EarthRanger password |

> **Important:** Credentials entered here are **not** validated during setup. Any authentication errors will only appear when the workflow runs.

Click **Connect** to save the data source.

---

### Step 3 — Select the Workflow

Go back to **Workflow Templates**. The newly added template appears as the **livestock_monitoring** card (showing the source repository URL). Click the card to open the workflow configuration form.

---

### Step 4 — Configure Workflow Details, Time Range, and EarthRanger Connection

The configuration form is divided into three sections, each highlighted in the left-hand navigation panel.

**Set Workflow Details**

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run (required) |
| Workflow Description | Optional notes to differentiate this run from others (e.g. reporting month or site) |

**Time Range**

| Field | Description |
|-------|-------------|
| Timezone | Select the local timezone (e.g. `Africa/Nairobi (UTC+03:00)`) |
| Since | Start date and time — all livestock events from this point are fetched |
| Until | End date and time of the analysis window |

**Connect to EarthRanger**

Select the EarthRanger data source configured in Step 2 from the **Data Source** dropdown (e.g. `Mara North Conservancy`).

Once all three sections are filled, click **Submit** to start the workflow.

---

## Running the Workflow

Once submitted, the runner will:

1. Download the MNC community conservancy boundary and parcels files from Dropbox; fix any invalid geometries in the boundary file; build the shared map base layers — a conservancy boundary outline, colour-coded grazing zones (colours and legend generated automatically from the zone names), and a parcels layer.
2. Fetch `mobile_boma_rep`, `cattle_count`, `livestock_predation_rep`, and `illegal_grazing_rep` events for the analysis period from EarthRanger as point geometries; extract the date from each event's timestamp; add a temporal index.
3. **Mobile Boma branch** — filter `mobile_boma_rep` events; process and flatten event details; retain key fields (date, event type, location, boma zone, boma status, relocation date and reason); count unique boma events per day; save as `mobile_boma_movement_summary_table.csv`; draw a point map over the shared base layers, save as `boma_movement_map.html`/`.png`, and add it to the dashboard.
4. **Cattle Count branch** — filter `cattle_count` events; process and flatten event details; retain cattle counts per zone (Zone 1, Zone 2/3, Zone 4); convert the counts to numeric and compute the total itself by summing the three zones; rename columns to display-friendly headers; save as `total_cattle_count_summary_table.csv`; add it to the dashboard as an interactive table widget.
5. **Livestock Predation branch** — filter `livestock_predation_rep` events; process and flatten event details; capitalise the livestock species field for consistent grouping; draw a point map coloured by livestock species over the shared base layers, save as `livestock_predation_events.html`/`.png`, and add it to the dashboard. Separately, count unique predation events per day, rename to display headers, and save as `total_livestock_predation_summary_table.csv`, also added to the dashboard as a table widget. Separately again, produce a detailed record-level table (species, suspected predator — nulls and "Other" values replaced with Unknown — and animals affected), saved as `livestock_predation_summary_table.csv` (CSV only, no dashboard widget).
6. **Illegal Grazing branch** — filter `illegal_grazing_rep` events; process and flatten event details; retain herd zone, landowner, and action taken; draw a point map over the shared base layers (now including the parcels layer), save as `illegal_grazing_map.html`/`.png`, and add it to the dashboard.
7. Assemble the dashboard, combining workflow details, time range, groupers, and the five widgets above (three maps, two summary tables).
8. Save all outputs to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`.

> All three maps now frame themselves to the extent of the Mara North Conservancy boundary, so they share a consistent view — previously the livestock predation map used a fixed, hand-picked coordinate and zoom level.

> Steps are automatically skipped if their input data is empty or an upstream step was skipped, so a run with no events of a given type will simply omit that branch's output rather than failing.

---

## Output Files

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS/`.

### CSV Tables

| File | Description |
|------|-------------|
| `mobile_boma_movement_summary_table.csv` | Daily unique boma event count (`date`, `boma_events`) |
| `total_cattle_count_summary_table.csv` | Cattle counts per date by zone (`Date`, `Zone 1`, `Zone 2/3`, `Zone 4`, `Total`) |
| `total_livestock_predation_summary_table.csv` | Daily unique predation event count (`Date`, `Livestock Predation Events`) |
| `livestock_predation_summary_table.csv` | Detailed predation records: `date`, `livestock_species`, `suspected_predator`, `total_livestock_affected` |

### Maps

| File | Description |
|------|-------------|
| `boma_movement_map.html` / `.png` | Mobile boma locations over grazing zones, parcels, and the conservancy boundary |
| `livestock_predation_events.html` / `.png` | Predation incident locations over the same base layers, coloured by livestock species |
| `illegal_grazing_map.html` / `.png` | Illegal grazing locations over the same base layers |

### Dashboard

The workflow run also produces a dashboard, viewable in the workflow runner, with one interactive widget per map and per count-summary table:

| Widget | Type | Source |
|--------|------|--------|
| Mobile Boma Movement Map | Map | `boma_movement_map.html` |
| Livestock Predation Events Map | Map | `livestock_predation_events.html` |
| Illegal Grazing Events Map | Map | `illegal_grazing_map.html` |
| Total Cattle Count Summary | Table | `total_cattle_count_summary_table.csv` |
| Livestock Predation Summary | Table | `total_livestock_predation_summary_table.csv` (the daily event **count**, not the detailed `livestock_predation_summary_table.csv`, which has no dashboard widget) |
