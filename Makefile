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

# Compile Part 1 and Part 2 reports locally (requires tectonic, latexmk, or Docker).
report:
	@if command -v tectonic >/dev/null 2>&1; then \
		tectonic ESE5700_Proj1_Part1.tex; \
		tectonic ESE5700_Proj1_Part2.tex; \
	elif command -v latexmk >/dev/null 2>&1; then \
		latexmk -pdf -file-line-error -halt-on-error -interaction=nonstopmode ESE5700_Proj1_Part1.tex; \
		latexmk -pdf -file-line-error -halt-on-error -interaction=nonstopmode ESE5700_Proj1_Part2.tex; \
	else \
		bash scripts/run-latex-ci-local.sh; \
	fi

# Recompute the read-SNM beta sweep from the raw Cadence exports.
snm:
	python3 scripts/check_snm_sweep.py --all

# Remove local TeX byproducts (the PDF stays tracked).
clean:
	rm -f ESE5700_Proj1_Part1.aux ESE5700_Proj1_Part1.log ESE5700_Proj1_Part1.out ESE5700_Proj1_Part1.toc ESE5700_Proj1_Part1.fls ESE5700_Proj1_Part1.fdb_latexmk ESE5700_Proj1_Part1.synctex.gz
	rm -f ESE5700_Proj1_Part2.aux ESE5700_Proj1_Part2.log ESE5700_Proj1_Part2.out ESE5700_Proj1_Part2.toc ESE5700_Proj1_Part2.fls ESE5700_Proj1_Part2.fdb_latexmk ESE5700_Proj1_Part2.synctex.gz
