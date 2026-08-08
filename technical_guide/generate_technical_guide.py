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
    p("Workflow id: <b>livestock_monitoring</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>livestock_monitoring</b> workflow (repository: mnc_livestock_report) "
      "fetches livestock-related events from EarthRanger for a specified time "
      "window — specifically <b>mobile_boma_rep</b>, <b>cattle_count</b>, "
      "<b>livestock_predation_rep</b>, and <b>illegal_grazing_rep</b> event types "
      "— and routes them into four independent reporting branches. In parallel, "
      "the workflow downloads MNC conservancy boundary and parcels geospatial "
      "files from Dropbox and builds a shared set of map base layers (conservancy "
      "boundary, colour-coded grazing zones, parcels) used by all three maps. "
      "Three of the four branches, plus all three maps, are additionally wrapped "
      "as widgets on the workflow's dashboard."),
    sp(4),
    p("The workflow delivers:"),
    bullet("<b>mobile_boma_movement_summary_table.csv</b> — daily count of mobile "
           "boma movement events"),
    bullet("<b>total_cattle_count_summary_table.csv</b> — cattle counts per grazing "
           "zone per date, with a workflow-computed total column"),
    bullet("<b>total_livestock_predation_summary_table.csv</b> — daily count of "
           "livestock predation events"),
    bullet("<b>livestock_predation_summary_table.csv</b> — predation incidents by "
           "species, suspected predator, and number of animals affected"),
    bullet("<b>boma_movement_map.html / .png</b> — point map of mobile boma "
           "locations over the shared base layers"),
    bullet("<b>livestock_predation_events.html / .png</b> — point map of predation "
           "incidents over the shared base layers, coloured by species"),
    bullet("<b>illegal_grazing_map.html / .png</b> — point map of illegal grazing "
           "incidents over the shared base layers"),
    bullet("<b>A dashboard</b> — five widgets: the three maps above, plus the "
           "cattle count and livestock predation count-summary tables"),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output", "Type", "Source event type", "Dashboard widget?"],
            ["mobile_boma_movement_summary_table.csv",
             "CSV", "mobile_boma_rep", "No"],
            ["total_cattle_count_summary_table.csv",
             "CSV", "cattle_count", "Yes (table)"],
            ["total_livestock_predation_summary_table.csv",
             "CSV", "livestock_predation_rep", "Yes (table)"],
            ["livestock_predation_summary_table.csv",
             "CSV", "livestock_predation_rep", "No"],
            ["boma_movement_map.html / .png",
             "Map", "mobile_boma_rep", "Yes (map)"],
            ["livestock_predation_events.html / .png",
             "Map", "livestock_predation_rep", "Yes (map)"],
            ["illegal_grazing_map.html / .png",
             "Map", "illegal_grazing_rep", "Yes (map)"],
        ],
        [6*cm, 1.5*cm, 3.5*cm, W - 11*cm],
    ),
    note("total_livestock_predation_summary_table.csv (daily counts) and "
         "livestock_predation_summary_table.csv (detailed per-event records) are "
         "two distinct outputs from the same branch — only the former has a "
         "dashboard widget, titled “Livestock Predation Summary”."),
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
            ["ecoscope-platform",              ">=2.15.0, <2.16.0", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",  "0.1.0rc14.*", "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",     "0.0.0rc1.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mnc",     "1.0.0.*",     "ecoscope-workflows-custom"],
            ["pydeck",                         "0.9.2",       "conda-forge"],
            ["opentelemetry-sdk",              ">=1.20.0, <2.0.0", "conda-forge"],
        ],
        [6.5*cm, 3.5*cm, W - 10*cm],
    ),
    note("<b>ecoscope-platform</b> replaces the previously separate "
         "<b>ecoscope-workflows-core</b> and <b>ecoscope-workflows-ext-ecoscope</b> "
         "packages. The <b>ecoscope-workflows-ext-mep</b> and "
         "<b>ecoscope-workflows-ext-big-life</b> packages, previously listed, are "
         "no longer required. Several tasks that used to resolve from the default "
         "task namespace are now referenced by their fully qualified module path "
         "(e.g. ecoscope_workflows_ext_ste.tasks.io.fetch_and_persist_file, "
         "ecoscope_workflows_ext_custom.tasks.results.draw_map) — this is a "
         "housekeeping change with no behavioural effect."),
    sp(6),
    h2("2.2  Connections and external assets"),
    make_table(
        [
            ["Asset", "Task / Source", "Purpose"],
            ["EarthRanger", "set_er_connection",
             "Fetch event records and resolve event detail display titles "
             "(used in all process_events_details calls)"],
            ["mnc_conservancy.gpkg", "fetch_and_persist_file (Dropbox)",
             "MNC community conservancy boundary, used to derive the conservancy "
             "outline, grazing zone, and Mara North Conservancy layers."],
            ["mnc_across_the_river_parcels.gpkg", "fetch_and_persist_file (Dropbox)",
             "MNC across-the-river land parcels. Used as an additional polygon "
             "layer on all three maps."],
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
      "produced by the workflow. This pipeline was substantially reworked from "
      "the previous revision — see the notes at the end of this section."),
    sp(6),
    h2("3.1  Conservancy boundary and grazing zone filters"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "fetch_and_persist_file",
             "Download <b>mnc_conservancy.gpkg</b> from Dropbox to "
             "ECOSCOPE_WORKFLOWS_RESULTS (overwrite_existing: false, retries: 3)."],
            ["2", "load_df",
             "Load the gpkg into a GeoDataFrame "
             "(layer: null, deserialize_json: false)."],
            ["3", "fix_invalid_geometries",
             "Repair any invalid geometries in the loaded boundary GeoDataFrame."],
            ["4", "filter_df",
             "Filter to <b>grazing_zone == 'Conservancy'</b> "
             "→ filter_conservancy_boundary, used for the conservancy outline layer."],
            ["5", "filter_df",
             "Filter to <b>name == 'Mara North Conservancy'</b> "
             "→ filter_mara_north, used to compute the shared map zoom/extent "
             "(Section 4.4)."],
            ["6", "filter_df",
             "Filter to <b>grazing_zone != 'Conservancy'</b> "
             "→ filter_grazing_zones, the coloured grazing-zone polygons."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("3.2  Grazing zone colouring and legend"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "apply_color_map",
             "Colour filter_grazing_zones by the <b>grazing_zone</b> column using "
             "the <b>GnBu</b> colormap → output column <b>zone_color</b>."],
            ["2", "build_legend_values_from_column",
             "Build the map legend entries directly from the grazing_zone / "
             "zone_color columns (sort: ascending)."],
        ],
        [1.2*cm, 5*cm, W - 6.2*cm],
    ),
    note("Grazing zone colours and legend entries are now generated dynamically "
         "from whatever zone names are present in the data, instead of a "
         "hardcoded style dictionary keyed on six fixed zone names. If new zones "
         "are added or renamed in the source boundary file, the map colouring "
         "and legend adapt automatically."),
    sp(6),
    h2("3.3  Parcels layer"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "fetch_and_persist_file",
             "Download <b>mnc_across_the_river_parcels.gpkg</b> from Dropbox "
             "(overwrite_existing: false, retries: 3)."],
            ["2", "load_df",
             "Load the parcels gpkg into a GeoDataFrame."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("3.4  Map layers"),
    p("All three static base layers are now created with the same task, "
      "<b>create_geojson_layer</b>:"),
    make_table(
        [
            ["Layer", "Style", "Legend"],
            ["create_conservancy_layer",
             "Unfilled, stroked grey outline (169,169,169,255), width 1.75",
             "“Boundaries” — Conservancy Boundary (#a9a9a9)"],
            ["create_grazing_zones_layer",
             "Filled and stroked, opacity 0.5, fill/line colour from zone_color",
             "“Grazing Zones” — dynamic, from Section 3.2"],
            ["create_parcels_layer",
             "Filled (189,183,107,60) / stroked (189,183,107,255), width 1.5",
             "“Boundaries” — Parcels (#bdb76b)"],
        ],
        [4.5*cm, 6*cm, W - 10.5*cm],
    ),
    note("The previous revision built these same three concepts very "
         "differently: it split the boundary file into a dict of six hardcoded "
         "zones (split_gdf_by_column / annotate_gdf_dict_with_geom_type / "
         "create_deckgl_layers_from_gdf_dict) and rendered a separate text-label "
         "layer showing the conservancy name at its centroid "
         "(create_custom_text_layer). Both the zone dict-splitting approach and "
         "the conservancy name text-label layer have been removed in this "
         "revision — maps no longer show a name label on the conservancy "
         "polygon. The parcels layer no longer needs a separate geometry-type "
         "detection step (get_gdf_geom_type) before rendering."),
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
            ["force_point_geometry",    "true"],
        ],
        [5*cm, W - 5*cm],
    ),
    note("force_point_geometry: true normalises all event geometries to points "
         "before they reach the branch pipelines and the map layers below."),
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
    h2("4.4  Shared map zoom and extent"),
    p("A task-group titled <b>“Map Zoom &amp; Extent”</b> computes a single view "
      "state, shared by all three maps in this workflow:"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "envelope_gdf",
             "Compute the bounding envelope of filter_mara_north "
             "(the Mara North Conservancy boundary, Section 3.1)."],
            ["2", "compute_view_state_from_gdf",
             "Derive a centre point and zoom level from that envelope "
             "(pitch: 0, bearing: 0, max_zoom: 15)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    note("This replaces the previous revision's approach, which computed a "
         "zoom value from the union of grazing zone geometries "
         "(view_state_deck_gdf on overall_grazing_zones) and used it only for "
         "the boma movement and illegal grazing maps — the livestock predation "
         "map used a separate, hand-picked fixed coordinate and zoom "
         "(lon: 35.2093, lat: -1.2578, zoom: 9.75). All three maps now share the "
         "same conservancy-derived view state."),
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
            ["event_type",            "Retained but not used for map colouring"],
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
             "Group by <b>date</b>; compute <b>nunique(id)</b> displayed as "
             "<b>boma_events</b> (decimal_places: 0). reset_index: true."],
            ["2", "persist_df",
             "Save as <b>mobile_boma_movement_summary_table.csv</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    note("The previous revision appended a grand “Total” row via add_totals_row "
         "before persisting. That step has been removed — the CSV now contains "
         "only one row per date."),
    sp(6),
    h2("5.4  Map"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "create_scatterplot_layer",
             "Render points from the map_mobile_boma table: fixed navy fill/line "
             "colour (0,0,128), get_radius: 3, opacity: 0.55, stroked: true. "
             "Legend title: “Movements”, single entry “Boma movement”."],
            ["2", "combine_deckgl_map_layers",
             "Static layers: create_grazing_zones_layer, create_parcels_layer, "
             "create_conservancy_layer (Section 3.4). Grouped: the boma point layer."],
            ["3", "draw_map",
             "Render map (max_zoom: 10, legend placement: bottom-right, "
             "tile_layers from configure_base_maps, "
             "view_state from the shared Map Zoom &amp; Extent group, Section 4.4)."],
            ["4", "persist_text",
             "Save HTML to <b>boma_movement_map.html</b>."],
            ["5", "create_map_widget_single_view",
             "Wrap the map as a dashboard widget titled "
             "“Mobile Boma Movement Map”."],
            ["6", "html_to_png",
             "Convert to PNG (device_scale_factor: 2.0, wait: 40 s, "
             "max_concurrent_pages: 1)."],
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
      "broken down by grazing zone per date, with a workflow-computed total. "
      "This branch produces no map."),
    sp(6),
    h2("6.1  Normalisation"),
    p("Steps 1–4 follow the common normalisation pattern in Section 4.3."),
    sp(6),
    h2("6.2  Column selection and renaming"),
    p("Task: <b>map_columns</b> (raise_if_not_found: false). The source "
      "<b>total_cattle_counted_from_all_zones</b> column is now dropped rather "
      "than retained — the workflow computes its own total instead (Section 6.3)."),
    make_table(
        [
            ["Source column (title after prefix drop)", "Renamed to"],
            ["date",                                    "date (retained, not renamed)"],
            ["# cattle in Zone 1 mobile boma",          "zone_1"],
            ["# cattle in Zone 2/3 mobile boma",        "zone_2_3"],
            ["# cattle in Zone 4",                      "zone_4"],
        ],
        [7*cm, W - 7*cm],
    ),
    sp(6),
    h2("6.3  Total, display renaming, and persistence"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "convert_column_values_to_numeric",
             "Coerce zone_1, zone_2_3, and zone_4 to numeric."],
            ["2", "ecoscope_workflows_ext_mnc.tasks.aggregation.apply_arithmetic_operation_over_rows",
             "Sum zone_1 + zone_2_3 + zone_4 row-wise into a new <b>total</b> "
             "column (operation: add)."],
            ["3", "map_columns",
             "Rename columns to display-friendly headers: date→Date, "
             "zone_1→Zone 1, zone_2_3→Zone 2/3, zone_4→Zone 4, total→Total."],
            ["4", "persist_df",
             "Save as <b>total_cattle_count_summary_table.csv</b>, using the "
             "display-renamed table."],
            ["5", "draw_table",
             "Render the display-renamed table as an HTML widget "
             "(widget_id: “Total Cattle Count Summary”; sorting and filtering "
             "enabled; download disabled)."],
            ["6", "persist_text",
             "Save the rendered HTML as a text file "
             "(filename: total_cattle_count_summary_table.html)."],
            ["7", "create_table_widget_single_view",
             "Wrap the persisted HTML into a dashboard widget titled "
             "“Total Cattle Count Summary”."],
        ],
        [1.2*cm, 6*cm, W - 7.2*cm],
    ),
    note("Previously, the source event's own "
         "total_cattle_counted_from_all_zones field was trusted and simply "
         "renamed to total_count. The workflow now computes the total itself "
         "from the three zone counts, and the table gains a dashboard widget "
         "it did not have before."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. BRANCH 3 — LIVESTOCK PREDATION
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Branch 3 — Livestock Predation"),
    hr(),
    p("Filters <b>livestock_predation_rep</b> events and produces a point map, "
      "a daily count-summary table, and a detailed record-level table."),
    sp(6),
    h2("7.1  Normalisation"),
    p("Steps 1–4 follow the common normalisation pattern in Section 4.3."),
    sp(6),
    h2("7.2  Column selection"),
    p("Task: <b>map_columns</b> (raise_if_not_found: false, rename_columns: {}). "
      "The following columns are retained and shared by the map, the "
      "count-summary table, and the detailed table:"),
    make_table(
        [
            ["Column retained", "Notes"],
            ["id",                       "Row identifier"],
            ["date",                     "Event date"],
            ["event_type",               "Retained but not used for map colouring"],
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
            ["1", "format_text_column",
             "Capitalise the <b>Livestock Species</b> column (method: capitalize), "
             "so inconsistent casing in the source data doesn't split a species "
             "into multiple colours/legend entries."],
            ["2", "apply_color_map",
             "Colour points by the capitalised <b>Livestock Species</b> using the "
             "<b>Set3</b> colormap → output column <b>colors</b>."],
            ["3", "create_scatterplot_layer",
             "Render points: fill/line colour from colors, get_radius: 3, "
             "opacity: 0.55, stroked: true. Legend title: “Livestock Species”, "
             "entries generated from the species/colour columns (sort: ascending)."],
            ["4", "combine_deckgl_map_layers",
             "Static layers: create_grazing_zones_layer, create_parcels_layer, "
             "create_conservancy_layer (Section 3.4). Grouped: the predation "
             "point layer."],
            ["5", "draw_map",
             "Render map (max_zoom: 10, legend: bottom-right, view_state from "
             "the shared Map Zoom &amp; Extent group, Section 4.4)."],
            ["6", "persist_text",
             "Save HTML to <b>livestock_predation_events.html</b>."],
            ["7", "create_map_widget_single_view",
             "Wrap the map as a dashboard widget titled "
             "“Livestock Predation Events Map”."],
            ["8", "html_to_png",
             "Convert to PNG (device_scale_factor: 2.0, wait: 40 s)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    note("Two things changed from the previous revision: (1) this map now uses "
         "the same shared conservancy-derived view state as the other two maps, "
         "instead of a fixed coordinate/zoom; and (2) it now sits on the full "
         "three-layer base (grazing zones + parcels + conservancy) rather than "
         "the conservancy-boundary-only layer set — grazing zone colours are now "
         "visible under the predation points."),
    sp(6),
    h2("7.4  Summary tables"),
    p("The livestock predation branch produces two independent CSVs from the "
      "same normalised DataFrame."),
    h3("7.4a  total_livestock_predation_summary_table.csv (dashboard widget: “Livestock Predation Summary”)"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "summarize_df",
             "Group by <b>date</b>; compute <b>nunique(id)</b> displayed as "
             "<b>livestock_predation_events</b> (decimal_places: 0). "
             "reset_index: true."],
            ["2", "map_columns",
             "Rename columns to display-friendly headers: date→Date, "
             "livestock_predation_events→Livestock Predation Events."],
            ["3", "persist_df",
             "Save as <b>total_livestock_predation_summary_table.csv</b>, using "
             "the display-renamed table."],
            ["4", "draw_table",
             "Render the display-renamed table as an HTML widget "
             "(widget_id: “Livestock Predation Summary”)."],
            ["5", "persist_text",
             "Save the rendered HTML "
             "(filename: livestock_predation_summary_table.html)."],
            ["6", "create_table_widget_single_view",
             "Wrap the persisted HTML into a dashboard widget titled "
             "“Livestock Predation Summary”."],
        ],
        [1.2*cm, 6*cm, W - 7.2*cm],
    ),
    note("The previous revision appended a grand “Total” row (add_totals_row) "
         "here instead of renaming columns and creating a widget. The output "
         "filename is unchanged, but its content and presentation differ."),
    note("This step's persisted HTML filename "
         "(livestock_predation_summary_table.html) differs only by extension "
         "from the unrelated detail CSV in Section 7.4b "
         "(livestock_predation_summary_table.csv) — don't confuse the two when "
         "browsing ECOSCOPE_WORKFLOWS_RESULTS."),
    sp(6),
    h3("7.4b  livestock_predation_summary_table.csv (no dashboard widget)"),
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
            ["2", "fill_missing_values",
             "Replace missing values in <b>suspected_predator</b> and "
             "<b>livestock_species</b> with <b>'Unknown'</b> (subset: both "
             "columns)."],
            ["3", "replace_column_values",
             "Map <b>'Other (specify in comments)'</b> → <b>'Unknown'</b> "
             "in the <b>suspected_predator</b> column (inplace: true, "
             "errors: ignore)."],
            ["4", "ecoscope_workflows_ext_mnc.tasks.transformation.convert_columns_to_int",
             "Cast <b>total_livestock_affected</b> to integer "
             "(errors: coerce, fill_value: 0)."],
            ["5", "persist_df",
             "Save as <b>livestock_predation_summary_table.csv</b>."],
        ],
        [1.2*cm, 6*cm, W - 7.2*cm],
    ),
    note("Unlike the other three summary tables in this workflow, this detail "
         "table is not passed through a display-renaming step — its columns "
         "remain snake_case (livestock_species, suspected_predator, "
         "total_livestock_affected), and it has no dashboard widget."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. BRANCH 4 — ILLEGAL GRAZING
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Branch 4 — Illegal Grazing"),
    hr(),
    p("Filters <b>illegal_grazing_rep</b> events and produces a point map of "
      "illegal grazing incidents. This branch produces no CSV summary table."),
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
            ["event_type",    "Retained but not used for map colouring"],
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
            ["1", "create_scatterplot_layer",
             "Render points: fixed navy fill/line colour (0,0,128), "
             "get_radius: 3, opacity: 0.55, stroked: true. Legend title: "
             "“Activity”, single entry “Illegal grazing”."],
            ["2", "combine_deckgl_map_layers",
             "Static layers: create_grazing_zones_layer, create_parcels_layer, "
             "create_conservancy_layer (Section 3.4). Grouped: the illegal "
             "grazing point layer."],
            ["3", "draw_map",
             "Render map (max_zoom: 10, legend: bottom-right, view_state from "
             "the shared Map Zoom &amp; Extent group, Section 4.4)."],
            ["4", "persist_text",
             "Save HTML to <b>illegal_grazing_map.html</b>."],
            ["5", "create_map_widget_single_view",
             "Wrap the map as a dashboard widget titled "
             "“Illegal Grazing Events Map”."],
            ["6", "html_to_png",
             "Convert to PNG (device_scale_factor: 2.0, wait: 40 s)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    note("The legend title changed from “Illegal grazing” to “Activity” (the "
         "single legend entry is still labelled “Illegal grazing”). More "
         "significantly, this map's static base layers now include the parcels "
         "layer — previously parcels were deliberately excluded from this map; "
         "all three maps now share the identical three-layer base."),
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
             "Daily boma event counts"],
            ["total_cattle_count_summary_table.csv",
             "Cattle Count",
             "Date, Zone 1, Zone 2/3, Zone 4, Total",
             "Cattle counts per zone per date, with a workflow-computed total"],
            ["total_livestock_predation_summary_table.csv",
             "Livestock Predation",
             "Date, Livestock Predation Events",
             "Daily unique predation event count"],
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
             "fixed (navy)",
             "Grazing zones, parcels, conservancy boundary"],
            ["livestock_predation_events.html / .png",
             "Livestock Predation",
             "Livestock Species",
             "Grazing zones, parcels, conservancy boundary"],
            ["illegal_grazing_map.html / .png",
             "Illegal Grazing",
             "fixed (navy)",
             "Grazing zones, parcels, conservancy boundary"],
        ],
        [5*cm, 3*cm, 3.5*cm, W - 11.5*cm],
    ),
    sp(6),
    h2("9.3  Dashboard widget HTML"),
    p("The two count-summary tables (cattle count, livestock predation) each "
      "have a matching rendered HTML table persisted (via draw_table → "
      "persist_text) alongside their CSV. These HTML files are the data source "
      "referenced by the corresponding create_table_widget_single_view widget — "
      "they are not intended to be opened directly."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 10. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("10. Workflow Execution Logic"),
    hr(),
    h2("10.1  Global skip conditions"),
    p("This workflow now defines a single <b>task-instance-defaults</b> block "
      "at the top of the spec, which applies the same skipif conditions to "
      "every task automatically. Individual tasks no longer repeat their own "
      "skipif block:"),
    make_table(
        [
            ["Condition", "Behaviour"],
            ["any_is_empty_df",        "Skip this task if any input DataFrame is empty"],
            ["any_dependency_skipped", "Skip this task if any upstream dependency was skipped"],
        ],
        [5*cm, W - 5*cm],
    ),
    note("This is a behaviour-preserving simplification over the previous "
         "spec, which declared the identical skipif block on every task "
         "individually. Because the conditions are unchanged, each of the "
         "four branches still propagates skips independently — for example, if "
         "no cattle_count events are returned, only the cattle count branch "
         "(and its widget) is skipped; the other three branches continue "
         "normally."),
    sp(6),
    h2("10.2  Four independent branches"),
    p("After the shared ingestion pipeline produces <b>events_temporal</b>, "
      "the workflow splits into four fully independent branches. Each branch "
      "reads directly from events_temporal with no cross-branch dependencies:"),
    make_table(
        [
            ["Branch", "Filter value", "CSV output", "Map / table widgets"],
            ["Mobile Boma",    "mobile_boma_rep",
             "mobile_boma_movement_summary_table.csv", "Map widget only"],
            ["Cattle Count",   "cattle_count",
             "total_cattle_count_summary_table.csv", "Table widget"],
            ["Livestock Predation", "livestock_predation_rep",
             "total_livestock_predation_summary_table.csv + "
             "livestock_predation_summary_table.csv",
             "Map + table widget (count table only)"],
            ["Illegal Grazing", "illegal_grazing_rep",
             "—", "Map widget only"],
        ],
        [3.5*cm, 3.5*cm, 5*cm, W - 12*cm],
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
      "max_concurrent_pages: 1, full_page: false. This happens in addition to, "
      "not instead of, each map's dashboard widget."),
    sp(6),
    h2("10.5  Dashboard"),
    p("The workflow concludes with <b>gather_dashboard</b> (id: "
      "mnc_events_dashboard, name: “MNC event report dashboard”), which "
      "packages workflow details, time range, groupers, and the <b>widgets</b> "
      "list. The widgets list now references five widgets — the three map "
      "widgets and the two table widgets (cattle count, livestock predation "
      "count-summary) — where previously this list was empty."),
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
            ["ecoscope-platform",              ">=2.15.0, <2.16.0"],
            ["ecoscope-workflows-ext-custom",  "0.1.0rc14.*"],
            ["ecoscope-workflows-ext-ste",     "0.0.0rc1.*"],
            ["ecoscope-workflows-ext-mnc",     "1.0.0.*"],
            ["pydeck",                         "0.9.2"],
            ["opentelemetry-sdk",              ">=1.20.0, <2.0.0"],
        ],
        [7*cm, W - 7*cm],
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF written → {OUTPUT_FILE}")
