.PHONY: report snm clean

# Compile the Part 1 report locally (requires tectonic, latexmk, or Docker).
report:
	@if command -v tectonic >/dev/null 2>&1; then \
		tectonic ESE5700_Proj1_Part1.tex; \
	elif command -v latexmk >/dev/null 2>&1; then \
		latexmk -pdf -file-line-error -halt-on-error -interaction=nonstopmode ESE5700_Proj1_Part1.tex; \
	else \
		bash scripts/run-latex-ci-local.sh; \
	fi

# Recompute the read-SNM beta sweep from the raw Cadence exports.
snm:
	python3 scripts/check_snm_sweep.py --all

# Remove local build products (report aux files only; the PDF stays tracked).
clean:
	rm -f ESE5700_Proj1_Part1.aux ESE5700_Proj1_Part1.log ESE5700_Proj1_Part1.out ESE5700_Proj1_Part1.toc ESE5700_Proj1_Part1.fls ESE5700_Proj1_Part1.fdb_latexmk ESE5700_Proj1_Part1.synctex.gz
