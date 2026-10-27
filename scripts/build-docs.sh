#!/usr/bin/env bash
# Build the static technical manual with Asciidoctor.
# No dependency installation happens here; install Asciidoctor first:
#   macOS:  brew install asciidoctor
#   Linux:  sudo apt-get install -y asciidoctor   (or: gem install asciidoctor)
#   Other:  gem install asciidoctor
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO_ROOT/docs/index.adoc"
OUT_DIR="$REPO_ROOT/build/docs"
OUT_FILE="$OUT_DIR/index.html"

if ! command -v asciidoctor >/dev/null 2>&1; then
  echo "error: asciidoctor not found on PATH." >&2
  echo "Install it first:" >&2
  echo "  macOS:  brew install asciidoctor" >&2
  echo "  Debian/Ubuntu: sudo apt-get install -y asciidoctor" >&2
  echo "  RubyGems (any OS with Ruby): gem install asciidoctor" >&2
  exit 1
fi

if [ ! -f "$SRC" ]; then
  echo "error: missing source $SRC" >&2
  exit 1
fi

# Rebuild from a clean output directory so removed pages and assets cannot ship.
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR/theme" "$OUT_DIR/images"
python3 "$REPO_ROOT/scripts/ingest-logs.py"
if [ -d "$REPO_ROOT/docs/diagrams" ]; then
  python3 "$REPO_ROOT/scripts/render-docs-diagrams.py"
fi
if [ -d "$REPO_ROOT/docs/charts" ]; then
  python3 "$REPO_ROOT/scripts/render-docs-charts.py"
fi
python3 "$REPO_ROOT/scripts/prepare-docs.py" head

# Version stamp, RISC-V-spec style ("Version <sha>, <date>" under the
# title). Derived from git at build time; falls back to the build date
# outside a git checkout. Pure Asciidoctor revision attributes.
REVDATE="$(git -C "$REPO_ROOT" log -1 --format=%cs 2>/dev/null || date +%F)"
REVNUM="$(git -C "$REPO_ROOT" rev-parse --short HEAD 2>/dev/null || echo unversioned)"

# Single-page manual. docinfo=shared + docinfodir pulls docs/theme/docinfo.html
# (CSS/JS injection) without editing generated HTML afterwards.
HAS_LOGS=0
if [ -f "$REPO_ROOT/docs/sections/generated/engineering-log.adoc" ]; then
  HAS_LOGS=1
fi

if [ "$HAS_LOGS" -eq 1 ]; then
  asciidoctor \
    --backend html5 \
    --safe-mode unsafe \
    --attribute docinfo=shared \
    --attribute docinfodir="$OUT_DIR/theme" \
    --attribute revdate="$REVDATE" \
    --attribute revnumber="$REVNUM" \
    --attribute has-logs \
    --out-file "$OUT_FILE" \
    "$SRC"
else
  asciidoctor \
    --backend html5 \
    --safe-mode unsafe \
    --attribute docinfo=shared \
    --attribute docinfodir="$OUT_DIR/theme" \
    --attribute revdate="$REVDATE" \
    --attribute revnumber="$REVNUM" \
    --out-file "$OUT_FILE" \
    "$SRC"
fi

# Theme assets live next to the HTML so relative paths in docinfo.html resolve.
cp "$REPO_ROOT/docs/theme/docs.css" "$OUT_DIR/theme/docs.css"
cp "$REPO_ROOT/docs/theme/nav.js"   "$OUT_DIR/theme/nav.js"
cp "$REPO_ROOT/docs/theme/search.js" "$OUT_DIR/theme/search.js"

# Figures referenced via :imagesdir: images.
if [ -d "$REPO_ROOT/docs/images" ]; then
  cp -R "$REPO_ROOT/docs/images/." "$OUT_DIR/images/"
  rm -f "$OUT_DIR/images/.gitkeep"
fi

# Cadence screenshots: single source of truth is media/cadence/; stage them
# next to the figures so image::inv_*.png[] resolves in the built manual.
if [ -d "$REPO_ROOT/media/cadence" ]; then
  cp "$REPO_ROOT/media/cadence/"*.png "$OUT_DIR/images/" 2>/dev/null || true
fi

# Part 1 report figures: source of truth is media/part1/; stage whatever
# has landed so image::bitcell-*.png / butterfly-*.png / functional-*.png
# resolve once exported from Virtuoso.
if [ -d "$REPO_ROOT/media/part1" ]; then
  cp "$REPO_ROOT/media/part1/"*.png "$OUT_DIR/images/" 2>/dev/null || true
fi
if [ -d "$REPO_ROOT/media/part1/current" ]; then
  cp "$REPO_ROOT/media/part1/current/"*.png "$OUT_DIR/images/" 2>/dev/null || true
fi

# Curated Part 2 JPEGs (cropped). Do not copy all of media/ or report/part2/img.
P2_IMG="$REPO_ROOT/report/part2/img/small"
for f in \
  sram_macro_schematic.jpg \
  write_driver_schematic_nfin8.jpg \
  precharge_schematic.jpg \
  read_path_schematic_library_view_2to2.jpg \
  out_latch_schematic.jpg \
  decoder_predec_schematic.jpg \
  tb_sram_macro_row15_wl_bl_we_clk_dout_zoom_BEST.jpg \
  tb_sram_macro_tclk_access_680_700ps.jpg \
  tb_sram_macro_power_sweep_with_standby.jpg \
  write_driver_tran_nfin8.jpg \
  tb_fo4_tran.jpg \
  tb_dec_pre_addr_to_wl.jpg \
  read_path_vtc_2to2.jpg \
  tb_sram_macro_ade_results_err.jpg
do
  if [ -f "$P2_IMG/$f" ]; then
    cp "$P2_IMG/$f" "$OUT_DIR/images/"
  fi
done

# Curated Part 3 PNGs. Skip debug dumps (*_unreadable*, *_overzoomed*, *_prefix*).
P3_IMG="$REPO_ROOT/report/part3/img"
for f in \
  mac_top_schematic.png \
  mac_top_schematic_right.png \
  dff_schematic.png \
  tb_dff_clk_to_q.png \
  dff_setup_rise_40ps.png \
  dff_hold_rise_10ps.png \
  mult4x4_schematic.png \
  tb_multiplier4b_errS.png \
  adder12_schematic.png \
  controller_schematic.png \
  tb_controller_tran.png \
  stimuli_timing_dir.png \
  tb_top_B_2p5.png \
  tb_top_A_4ns.png \
  tb_top_A_2ns.png \
  tb_top_A_1p5ns.png \
  tb_top_rden_bug.png \
  tb_top_A_eng_2p5.png \
  tb_top_C_2p5.png \
  counter4b_schematic.png \
  tb_counter4b_tran.png \
  dff_energy_idle.png \
  dff_energy_toggle.png \
  tb_top_B_eng_2p5.png \
  tb_top_C_eng_2p5.png \
  tgate_schematic.png \
  xor2_schematic.png
do
  if [ -f "$P3_IMG/$f" ]; then
    cp "$P3_IMG/$f" "$OUT_DIR/images/"
  fi
done

python3 "$REPO_ROOT/scripts/prepare-docs.py" page
python3 "$REPO_ROOT/scripts/prepare-docs.py" not-found
if [ -f "$REPO_ROOT/docs/ese5700-project1.pdf" ]; then
  cp "$REPO_ROOT/docs/ese5700-project1.pdf" "$OUT_DIR/ese5700-project1.pdf"
fi
if [ -f "$REPO_ROOT/report/part1/ESE5700_Proj1_Part1.pdf" ]; then
  cp "$REPO_ROOT/report/part1/ESE5700_Proj1_Part1.pdf" "$OUT_DIR/report.pdf"
fi
if [ -f "$REPO_ROOT/report/part2/ESE5700_Proj1_Part2.pdf" ]; then
  cp "$REPO_ROOT/report/part2/ESE5700_Proj1_Part2.pdf" "$OUT_DIR/report-part2.pdf"
fi
if [ -f "$REPO_ROOT/report/part3/ESE5700_Proj1_Part3.pdf" ]; then
  cp "$REPO_ROOT/report/part3/ESE5700_Proj1_Part3.pdf" "$OUT_DIR/report-part3.pdf"
fi
python3 "$REPO_ROOT/scripts/export-docs-template.py"

echo "Built $OUT_FILE"
