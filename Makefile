.PHONY: docs docs-check docs-clean docs-open report snm clean

# Build the complete static documentation into build/docs/.
docs:
	bash scripts/build-docs.sh

# Validate the published site and the reusable template build.
docs-check: docs
	python3 scripts/check-docs.py build/docs
	python3 scripts/test-docs-template.py

# Remove generated documentation.
docs-clean:
	rm -rf build/docs

# Serve the built manual locally (requires `make docs` first).
# Uses only the Python standard library; no npm or extra tooling.
docs-open: docs
	python3 -m http.server --directory build/docs 8000

# Compile the Part 1 report locally (requires tectonic, latexmk, or Docker).
report:
	@if command -v tectonic >/dev/null 2>&1; then \
		cd report/part1 && tectonic ESE5700_Proj1_Part1.tex; \
	elif command -v latexmk >/dev/null 2>&1; then \
		cd report/part1 && latexmk -pdf -file-line-error -halt-on-error -interaction=nonstopmode ESE5700_Proj1_Part1.tex; \
	else \
		bash scripts/run-latex-ci-local.sh; \
	fi

# Recompute the read-SNM beta sweep from the raw Cadence exports.
snm:
	python3 scripts/check_snm_sweep.py --all

# Remove local TeX byproducts (the PDF stays tracked).
clean:
	rm -f report/part1/ESE5700_Proj1_Part1.aux report/part1/ESE5700_Proj1_Part1.log report/part1/ESE5700_Proj1_Part1.out report/part1/ESE5700_Proj1_Part1.toc report/part1/ESE5700_Proj1_Part1.fls report/part1/ESE5700_Proj1_Part1.fdb_latexmk report/part1/ESE5700_Proj1_Part1.synctex.gz
