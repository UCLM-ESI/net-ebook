.PHONY: all buildpdf check clean code-checks

BOOK_SOURCES := $(shell find . -type f -name '*.md' ! -path '*/publish/*')
BOOK_PDF = _build/latex/book.pdf

all: check _build

_build: ${BOOK_SOURCES}
	jb build -W .

# ${BOOK_PDF}: ${BOOK_SOURCES}
# 	jb build -W -n --builder pdflatex .

# publish: _build ${BOOK_PDF}
publish: _build
	mv _build/html $@
	# mv ${BOOK_PDF} $@/ssdd-lab.pdf
	# cp -r assets $@
	# cp -r src $@

clean:
	jb clean .
	find . -name "*~" -delete
	rm -rf _build publish

check:
	pre-commit run --all

# code-checks:
# 	pylint exercise/*.py
# 	pycodestyle exercise/*.py
# 	pydocstyle exercise/*.pydocstyle
