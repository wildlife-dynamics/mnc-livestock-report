"""
Generate the MNC Livestock Report Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: mnc_livestock_report_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "mnc_livestock_report_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)

def c(text):
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"MNC Livestock Report — Technical Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

W = A4[0] - 4*cm   # usable width

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(60),
    p("MNC Livestock Report", TITLE),
    p("Technical Guide", SUBTITLE),
    sp(4),
    p("Mobile boma movements, cattle counts, livestock predation, and illegal grazing reporting", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>mnc_livestock_report</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>mnc_livestock_report</b> workflow fetches livestock-related events "
      "from EarthRanger for a specified time window — specifically "
      "<b>mobile_boma_rep</b>, <b>cattle_count</b>, <b>livestock_predation_rep</b>, "
      "and <b>illegal_grazing_rep</b> event types — and routes them into four "
      "independent reporting branches. In parallel, the workflow downloads MNC "
      "conservancy boundary and parcels geospatial files from Dropbox to use as "
      "base layers on all maps."),
    sp(4),
    p("The workflow delivers:"),
    bullet("<b>mobile_boma_movement_summary_table.csv</b> — daily count of mobile "
           "boma movement events with a grand total row"),
    bullet("<b>total_cattle_count_summary_table.csv</b> — cattle counts per grazing "
           "zone per date"),
    bullet("<b>livestock_predation_summary_table.csv</b> — predation incidents by "
           "species, suspected predator, and number of animals affected"),
    bullet("<b>boma_movement_map.html / .png</b> — point map of mobile boma "
           "locations on MNC grazing zones and parcels"),
    bullet("<b>livestock_predation_events.html / .png</b> — point map of predation "
           "incidents on conservancy boundaries and parcels"),
    bullet("<b>illegal_grazing_map.html / .png</b> — point map of illegal grazing "
           "incidents on MNC grazing zones"),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output", "Type", "Source event type", "Description"],
            ["mobile_boma_movement_summary_table.csv",
             "CSV", "mobile_boma_rep",
             "Daily boma event counts + Total row"],
            ["total_cattle_count_summary_table.csv",
             "CSV", "cattle_count",
             "Cattle per zone per date"],
            ["livestock_predation_summary_table.csv",
             "CSV", "livestock_predation_rep",
             "Predation records by species and predator"],
            ["boma_movement_map.html / .png",
             "Map", "mobile_boma_rep",
             "Boma locations on grazing zones and parcels"],
            ["livestock_predation_events.html / .png",
             "Map", "livestock_predation_rep",
             "Predation locations on conservancy boundaries"],
            ["illegal_grazing_map.html / .png",
             "Map", "illegal_grazing_rep",
             "Illegal grazing locations on grazing zones"],
        ],
        [5.5*cm, 1.5*cm, 3.5*cm, W - 10.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("2. Dependencies"),
    hr(),
    h2("2.1  Python packages"),
    make_table(
        [
            ["Package", "Version", "Channel"],
            ["ecoscope-workflows-core",        "0.22.18.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-ecoscope","0.22.18.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",  "0.0.43.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",     "0.0.18.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mnc",     "0.0.8.*",   "ecoscope-workflows-custom"],
        ],
        [6.5*cm, 3*cm, W - 9.5*cm],
    ),
    sp(6),
    h2("2.2  Connections and external assets"),
    make_table(
        [
            ["Asset", "Task / Source", "Purpose"],
            ["EarthRanger", "set_er_connection",
             "Fetch event records and resolve event detail display titles "
             "(used in all process_events_details calls)"],
            ["mnc_conservancy.gpkg", "fetch_and_persist_file (Dropbox)",
             "MNC community conservancy boundaries split by grazing zone. "
             "Used as polygon layers on the boma movement and illegal grazing maps."],
            ["mnc_across_the_river_parcels.gpkg", "fetch_and_persist_file (Dropbox)",
             "MNC across-the-river land parcels. Used as an additional polygon "
             "layer on the boma movement and livestock predation maps."],
        ],
        [3.5*cm, 4*cm, W - 7.5*cm],
    ),
    note("Both Dropbox files are downloaded with overwrite_existing: false and "
         "retries: 3. If the files already exist in ECOSCOPE_WORKFLOWS_RESULTS "
         "from a previous run, the download is skipped."),
    sp(6),
    h2("2.3  Grouper"),
    p("The workflow uses an <b>empty grouper list</b> (groupers: []). "
      "All event records are processed as a single undivided dataset — "
      "no fan-out or per-group branching is applied to the data. "
      "The grouper is passed through to the temporal index and the dashboard only."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. GEOSPATIAL ASSET PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("3. Geospatial Asset Pipeline"),
    hr(),
    p("Before any event data is fetched, the workflow downloads and prepares "
      "all geospatial base layers. These layers are shared across all three maps "
      "produced by the workflow."),
    sp(6),
    h2("3.1  Conservancy boundaries"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "fetch_and_persist_file",
             "Download <b>mnc_conservancy.gpkg</b> from Dropbox to "
             "ECOSCOPE_WORKFLOWS_RESULTS (overwrite_existing: false, retries: 3)."],
            ["2", "load_df",
             "Load the gpkg into a GeoDataFrame "
             "(layer: null, deserialize_json: false)."],
            ["3", "split_gdf_by_column",
             "Split the GeoDataFrame into a dict keyed by the <b>grazing_zone</b> "
             "column values (Conservancy, Conservancy Herd Zone, Grazing Zone 1–4)."],
            ["4", "annotate_gdf_dict_with_geom_type",
             "Add a geometry-type attribute to each GDF in the dict "
             "(required for layer rendering)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("3.2  Styled zone layers"),
    p("Two separate sets of DeckGL layers are created from the annotated dict:"),
    make_table(
        [
            ["Layer set", "Task", "Zones included", "Used on maps"],
            ["create_mnc_styled_layers",
             "create_deckgl_layers_from_gdf_dict",
             "Conservancy (grey outline), Conservancy Herd Zone (green), "
             "Grazing Zones 1–4 (dark olive, teal, dark green, sage)",
             "Boma movement map, Illegal grazing map"],
            ["create_conservancy_boundaries",
             "create_deckgl_layers_from_gdf_dict",
             "Conservancy boundary only (grey outline, no fill)",
             "Livestock predation map"],
        ],
        [3.5*cm, 3.5*cm, 4*cm, W - 11*cm],
    ),
    note("The full zone style set includes a map legend with colour swatches "
         "for all six zone types. The conservancy-only set uses a single "
         "'Boundaries' legend entry."),
    sp(6),
    h2("3.3  Conservancy and grazing zone GDFs"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "create_gdf_from_dict",
             "Extract the <b>Conservancy</b> key from the split dict "
             "to produce a single-zone GeoDataFrame (conservancy_gdf). "
             "Used to place conservancy name text labels on maps."],
            ["2", "filter_df",
             "Filter the full loaded GDF to rows where "
             "grazing_zone != 'Conservancy' (op: ne). "
             "Produces overall_grazing_zones, used to compute the global map "
             "zoom and view state."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("3.4  Conservancy text labels"),
    p("Task: <b>create_custom_text_layer</b>. Renders conservancy names on the map "
      "using the <b>name</b> field from conservancy_gdf. Key style parameters:"),
    make_table(
        [
            ["Parameter", "Value"],
            ["get_text",           "name"],
            ["get_color",          "[0, 0, 0, 255] (black)"],
            ["get_size",           "1500 m"],
            ["size_min_pixels",    "70"],
            ["size_max_pixels",    "100"],
            ["size_scale",         "2.25"],
            ["font_family",        "Calibri"],
            ["font_weight",        "700 (bold)"],
            ["billboard",          "true"],
            ["use_centroid",       "true (label placed at polygon centroid)"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("3.5  Parcels layer"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "fetch_and_persist_file",
             "Download <b>mnc_across_the_river_parcels.gpkg</b> from Dropbox "
             "(overwrite_existing: false, retries: 3)."],
            ["2", "load_df",
             "Load the parcels gpkg into a GeoDataFrame."],
            ["3", "get_gdf_geom_type",
             "Detect and attach the geometry type of the parcels GDF."],
            ["4", "create_deckgl_layer_from_gdf",
             "Render as a filled polygon layer: dark khaki fill (#bdb76b), "
             "opacity 0.15, stroked. Legend: 'Parcels'."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. EVENT INGESTION PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("4. Event Ingestion Pipeline"),
    hr(),
    p("All four reporting branches share a common event ingestion and "
      "normalisation pipeline."),
    sp(6),
    h2("4.1  Event retrieval"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Task",             "get_events"],
            ["event_types",      "mobile_boma_rep, cattle_count, "
                                 "livestock_predation_rep, illegal_grazing_rep"],
            ["Columns retained", "id, time, event_type, event_category, reported_by, "
                                 "serial_number, geometry, created_at, event_details, patrols"],
            ["include_details",  "true"],
            ["raise_on_empty",   "true"],
            ["include_null_geometry",   "false"],
            ["include_updates",         "false"],
            ["include_related_events",  "false"],
            ["include_display_values",  "false"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("4.2  Date extraction and temporal indexing"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "extract_column_as_type",
             "Extract the <b>time</b> column as <b>output_type: date</b> "
             "into a new column named <b>date</b>."],
            ["2", "add_temporal_index",
             "Add a temporal index using <b>time_col: date</b>, "
             "groupers: [], cast_to_datetime: true, format: mixed. "
             "Produces the shared <b>events_temporal</b> DataFrame."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("4.3  Common branch normalisation pattern"),
    p("Every branch applies the same four-step normalisation after filtering:"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "filter_df",
             "Filter events_temporal by event_type (op: equal, reset_index: true)."],
            ["2", "process_events_details",
             "Resolve event detail field IDs to display titles "
             "(map_to_titles: true, ordered: true). Requires the ER client."],
            ["3", "normalize_json_column",
             "Flatten the <b>event_details</b> JSON column "
             "(skip_if_not_exists: true, sort_columns: true)."],
            ["4", "drop_column_prefix",
             "Remove the <b>event_details__</b> prefix from all flattened columns "
             "(duplicate_strategy: keep_original)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    note("Because map_to_titles is true, the flattened column names are the "
         "human-readable field titles from EarthRanger (e.g. 'Mobile Boma Zone', "
         "'Livestock Species'). All downstream map_columns steps reference "
         "these titles directly."),
    sp(6),
    h2("4.4  Global map zoom value"),
    p("Task: <b>view_state_deck_gdf</b>. Computes the map centre and zoom from "
      "the <b>overall_grazing_zones</b> GeoDataFrame (pitch: 0, bearing: 0). "
      "This view state is shared by the boma movement map and the illegal grazing "
      "map. The livestock predation map uses a fixed view state instead "
      "(lon: 35.2093, lat: -1.2578, zoom: 9.75)."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. BRANCH 1 — MOBILE BOMA MOVEMENTS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("5. Branch 1 — Mobile Boma Movements"),
    hr(),
    p("Filters <b>mobile_boma_rep</b> events and produces a daily movement "
      "summary table and a point map of boma locations."),
    sp(6),
    h2("5.1  Normalisation"),
    p("Steps 1–4 follow the common normalisation pattern in Section 4.3."),
    sp(6),
    h2("5.2  Column selection"),
    p("Task: <b>map_columns</b> (raise_if_not_found: false, rename_columns: {}). "
      "The following columns are retained:"),
    make_table(
        [
            ["Column retained", "Notes"],
            ["id",                    "Used for counting events in the summary"],
            ["date",                  "Used for grouping in the summary table"],
            ["geometry",              "Used for the map"],
            ["Date of Relocation",    "Event detail field (title)"],
            ["Electric Boma Status",  "Event detail field (title)"],
            ["Mobile Boma Zone",      "Event detail field (title)"],
            ["Nature of the Site",    "Event detail field (title)"],
            ["Reason for relocation", "Event detail field (title)"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("5.3  Summary table"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "summarize_df",
             "Group by <b>date</b>; compute <b>sum(id)</b> displayed as "
             "<b>boma_events</b> (decimal_places: 0). reset_index: true."],
            ["2", "add_totals_row",
             "Append a grand <b>Total</b> row summing the boma_events column "
             "(label_col: date, label: 'Total')."],
            ["3", "persist_df",
             "Save as <b>mobile_boma_movement_summary_table.csv</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("5.4  Map"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "exclude_geom_outliers",
             "Remove spatial outliers using <b>z_threshold: 3</b> on the "
             "map_mobile_boma GDF."],
            ["2", "drop_null_geometry",
             "Drop any remaining rows with null geometry."],
            ["3", "apply_color_map",
             "Colour points by <b>event_type</b> using the <b>tab20</b> colormap "
             "→ output column <b>event_type_colors</b>."],
            ["4", "create_scatterplot_layer",
             "Render points: get_radius: 4, opacity: 0.75, stroked: true. "
             "Legend title: 'Boma Movements', label from event_type, "
             "colour from event_type_colors."],
            ["5", "combine_deckgl_map_layers",
             "Static layers: create_mnc_styled_layers, create_mnc_parcels_layers, "
             "conservancy_text_layer. Grouped: mobile boma point layer."],
            ["6", "draw_map",
             "Render map (max_zoom: 10, legend placement: bottom-right, "
             "view_state from global_zoom_value)."],
            ["7", "persist_text",
             "Save HTML to <b>boma_movement_map.html</b>."],
            ["8", "html_to_png",
             "Convert to PNG (device_scale_factor: 2.0, wait: 40 s)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. BRANCH 2 — CATTLE COUNTS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("6. Branch 2 — Cattle Counts"),
    hr(),
    p("Filters <b>cattle_count</b> events and produces a table of cattle counts "
      "broken down by grazing zone per date. This branch produces no map."),
    sp(6),
    h2("6.1  Normalisation"),
    p("Steps 1–4 follow the common normalisation pattern in Section 4.3."),
    sp(6),
    h2("6.2  Column selection and renaming"),
    p("Task: <b>map_columns</b> (raise_if_not_found: false). "
      "The following columns are retained and renamed:"),
    make_table(
        [
            ["Source column (title after prefix drop)", "Renamed to"],
            ["date",                                    "date (retained, not renamed)"],
            ["# cattle in Zone 1 mobile boma",          "zone_1"],
            ["# cattle in Zone 2/3 mobile boma",        "zone_2_3"],
            ["# cattle in Zone 4",                      "zone_4"],
            ["total_cattle_counted_from_all_zones",     "total_count"],
        ],
        [7*cm, W - 7*cm],
    ),
    sp(6),
    h2("6.3  Persistence"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "persist_df",
             "Save as <b>total_cattle_count_summary_table.csv</b> (filetype: csv)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. BRANCH 3 — LIVESTOCK PREDATION
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Branch 3 — Livestock Predation"),
    hr(),
    p("Filters <b>livestock_predation_rep</b> events and produces both a point "
      "map and a cleaned summary table."),
    sp(6),
    h2("7.1  Normalisation"),
    p("Steps 1–4 follow the common normalisation pattern in Section 4.3."),
    sp(6),
    h2("7.2  Column selection for mapping"),
    p("Task: <b>map_columns</b> (raise_if_not_found: false, rename_columns: {}). "
      "The following columns are retained for both the map and the summary table:"),
    make_table(
        [
            ["Column retained", "Notes"],
            ["id",                       "Row identifier"],
            ["date",                     "Event date"],
            ["geometry",                 "Used for the map"],
            ["Livestock Species",        "Event detail field (title)"],
            ["Suspected Predator",       "Event detail field (title)"],
            ["Total livestock affected", "Event detail field (title)"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("7.3  Map"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "exclude_geom_outliers",
             "Remove spatial outliers (z_threshold: 3)."],
            ["2", "drop_null_geometry",
             "Drop rows with null geometry."],
            ["3", "apply_color_map",
             "Colour points by <b>Livestock Species</b> using the <b>tab20</b> "
             "colormap → output column <b>colors</b>."],
            ["4", "create_scatterplot_layer",
             "Render points: get_radius: 4, opacity: 0.75, stroked: true. "
             "Legend title: 'Livestock Species', label from Livestock Species, "
             "colour from colors."],
            ["5", "combine_deckgl_map_layers",
             "Static layers: create_conservancy_boundaries, "
             "create_mnc_parcels_layers, conservancy_text_layer. "
             "Grouped: predation point layer."],
            ["6", "draw_map",
             "Render map using fixed view state "
             "(lon: 35.2093, lat: -1.2578, zoom: 9.75, "
             "max_zoom: 10, legend: bottom-right)."],
            ["7", "persist_text",
             "Save HTML to <b>livestock_predation_events.html</b>."],
            ["8", "html_to_png",
             "Convert to PNG (device_scale_factor: 2.0, wait: 40 s)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    note("The livestock predation map uses a fixed view state rather than the "
         "computed global_zoom_value, centred on the MNC area at zoom 9.75. "
         "It also uses the conservancy-boundaries-only layer set (no coloured "
         "grazing zones) to keep the focus on predation incident locations."),
    sp(6),
    h2("7.4  Summary tables"),
    p("The livestock predation branch produces two independent CSVs from the "
      "same normalised DataFrame."),
    h3("7.4a  total_livestock_predation_summary_table.csv"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "summarize_df",
             "Group by <b>date</b>; compute <b>nunique(id)</b> displayed as "
             "<b>livestock_predation_events</b> (decimal_places: 0). "
             "reset_index: true."],
            ["2", "add_totals_row",
             "Append a grand <b>Total</b> row summing the "
             "livestock_predation_events column "
             "(label_col: date, label: 'Total')."],
            ["3", "persist_df",
             "Save as <b>total_livestock_predation_summary_table.csv</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h3("7.4b  livestock_predation_summary_table.csv"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "map_columns",
             "Retain date, Livestock Species, Suspected Predator, "
             "Total livestock affected. Rename: "
             "Livestock Species → livestock_species, "
             "Suspected Predator → suspected_predator, "
             "Total livestock affected → total_livestock_affected. "
             "(raise_if_not_found: false)"],
            ["2", "replace_missing_with_label",
             "Replace nulls in <b>suspected_predator</b> and "
             "<b>livestock_species</b> with the label <b>'Unknown'</b>."],
            ["3", "map_column_values",
             "Map <b>'Other (specify in comments)'</b> → <b>'Unknown'</b> "
             "in the <b>suspected_predator</b> column (inplace: true)."],
            ["4", "convert_to_int",
             "Cast <b>total_livestock_affected</b> to integer "
             "(errors: coerce, fill_value: 0, inplace: false)."],
            ["5", "persist_df",
             "Save as <b>livestock_predation_summary_table.csv</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. BRANCH 4 — ILLEGAL GRAZING
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Branch 4 — Illegal Grazing"),
    hr(),
    p("Filters <b>illegal_grazing_rep</b> events and produces a point map of "
      "illegal grazing incidents on the MNC grazing zones. This branch produces "
      "no CSV summary table."),
    sp(6),
    h2("8.1  Normalisation"),
    p("Steps 1–4 follow the common normalisation pattern in Section 4.3."),
    sp(6),
    h2("8.2  Column selection"),
    p("Task: <b>map_columns</b> (raise_if_not_found: false, rename_columns: {}). "
      "The following columns are retained:"),
    make_table(
        [
            ["Column retained", "Notes"],
            ["date",          "Event date"],
            ["event_type",    "Event type identifier; used for colouring map points"],
            ["geometry",      "Used for the map"],
            ["Herd Zone",     "Event detail field (title)"],
            ["Landowner name","Event detail field (title)"],
            ["action taken",  "Event detail field (title)"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("8.3  Map"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "exclude_geom_outliers",
             "Remove spatial outliers (z_threshold: 3)."],
            ["2", "drop_null_geometry",
             "Drop rows with null geometry."],
            ["3", "apply_color_map",
             "Colour points by <b>event_type</b> using the <b>tab20</b> "
             "colormap → output column <b>event_type_colors</b>."],
            ["4", "create_scatterplot_layer",
             "Render points: get_radius: 4, opacity: 0.75, stroked: true. "
             "Legend title: 'Illegal grazing', label from event_type."],
            ["5", "combine_deckgl_map_layers",
             "Static layers: create_mnc_styled_layers, conservancy_text_layer. "
             "Grouped: illegal grazing point layer. "
             "(Note: parcels layer is not included on this map.)"],
            ["6", "draw_map",
             "Render map (max_zoom: 10, legend: bottom-right, "
             "view_state from global_zoom_value)."],
            ["7", "persist_text",
             "Save HTML to <b>illegal_grazing_map.html</b>."],
            ["8", "html_to_png",
             "Convert to PNG (device_scale_factor: 2.0, wait: 40 s)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("9. Output Files"),
    hr(),
    p("All outputs are written to <b>ECOSCOPE_WORKFLOWS_RESULTS</b>."),
    h2("9.1  CSV tables"),
    make_table(
        [
            ["File", "Branch", "Columns", "Description"],
            ["mobile_boma_movement_summary_table.csv",
             "Mobile Boma",
             "date, boma_events",
             "Daily boma event counts with a grand Total row"],
            ["total_cattle_count_summary_table.csv",
             "Cattle Count",
             "date, zone_1, zone_2_3, zone_4, total_count",
             "Cattle counts per zone per date"],
            ["total_livestock_predation_summary_table.csv",
             "Livestock Predation",
             "date, livestock_predation_events",
             "Daily unique predation event count with a grand Total row"],
            ["livestock_predation_summary_table.csv",
             "Livestock Predation",
             "date, livestock_species, suspected_predator, total_livestock_affected",
             "Predation records by species and predator"],
        ],
        [5*cm, 3*cm, 4*cm, W - 12*cm],
    ),
    sp(6),
    h2("9.2  Maps"),
    make_table(
        [
            ["File", "Branch", "Coloured by", "Base layers"],
            ["boma_movement_map.html / .png",
             "Mobile Boma",
             "event_type",
             "MNC grazing zones, parcels, conservancy labels"],
            ["livestock_predation_events.html / .png",
             "Livestock Predation",
             "Livestock Species",
             "Conservancy boundaries, parcels, conservancy labels"],
            ["illegal_grazing_map.html / .png",
             "Illegal Grazing",
             "event_type",
             "MNC grazing zones, conservancy labels (no parcels)"],
        ],
        [5*cm, 3*cm, 3.5*cm, W - 11.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 10. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("10. Workflow Execution Logic"),
    hr(),
    h2("10.1  Per-task skip conditions"),
    p("This workflow does <b>not</b> use a global <b>task-instance-defaults</b> "
      "block. Every task from event retrieval onwards carries its own explicit "
      "skipif block:"),
    make_table(
        [
            ["Condition", "Behaviour"],
            ["any_is_empty_df",        "Skip this task if any input DataFrame is empty"],
            ["any_dependency_skipped", "Skip this task if any upstream dependency was skipped"],
        ],
        [5*cm, W - 5*cm],
    ),
    note("Because skip conditions are per-task rather than global, each of the "
         "four branches propagates skips independently. For example, if no "
         "cattle_count events are returned, only the cattle count branch is "
         "skipped; the other three branches continue normally."),
    sp(6),
    h2("10.2  Four independent branches"),
    p("After the shared ingestion pipeline produces <b>events_temporal</b>, "
      "the workflow splits into four fully independent branches. Each branch "
      "reads directly from events_temporal with no cross-branch dependencies:"),
    make_table(
        [
            ["Branch", "Filter value", "CSV output", "Map output"],
            ["Mobile Boma",    "mobile_boma_rep",
             "mobile_boma_movement_summary_table.csv", "boma_movement_map"],
            ["Cattle Count",   "cattle_count",
             "total_cattle_count_summary_table.csv", "—"],
            ["Livestock Predation", "livestock_predation_rep",
             "livestock_predation_summary_table.csv", "livestock_predation_events"],
            ["Illegal Grazing", "illegal_grazing_rep",
             "—", "illegal_grazing_map"],
        ],
        [3.5*cm, 3.5*cm, 4.5*cm, W - 11.5*cm],
    ),
    sp(6),
    h2("10.3  No mapvalues or fan-out"),
    p("This workflow processes all records as a single batch. There is no "
      "<b>mapvalues</b>, <b>split_groups</b>, or <b>zip_groupbykey</b> — "
      "every task runs exactly once."),
    sp(6),
    h2("10.4  HTML to PNG conversion"),
    p("Three maps are rendered as HTML and then converted to PNG using "
      "<b>html_to_png</b>. All three use the same conversion settings: "
      "device_scale_factor: 2.0, wait_for_timeout: 40 000 ms, "
      "max_concurrent_pages: 1, full_page: false."),
    sp(6),
    h2("10.5  Dashboard"),
    p("The workflow concludes with <b>gather_dashboard</b> which packages "
      "workflow details, time range, and groupers. The <b>widgets</b> list "
      "is empty — no single-value or map widgets are configured."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 11. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("11. Software Versions"),
    hr(),
    make_table(
        [
            ["Package", "Version pinned in spec.yaml"],
            ["ecoscope-workflows-core",        "0.22.18.*"],
            ["ecoscope-workflows-ext-ecoscope","0.22.18.*"],
            ["ecoscope-workflows-ext-custom",  "0.0.43.*"],
            ["ecoscope-workflows-ext-ste",     "0.0.18.*"],
            ["ecoscope-workflows-ext-mnc",     "0.0.8.*"],
        ],
        [7*cm, W - 7*cm],
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF written → {OUTPUT_FILE}")
