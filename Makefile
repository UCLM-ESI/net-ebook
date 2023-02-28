.PHONY: all buildpdf check clean code-checks

BOOK_SOURCES := *.md *.ipynb
BOOK_PDF = _build/latex/book.pdf

all: code check _build

_build: ${BOOK_SOURCES}
	# jb build -W .
	jb build .

# ${BOOK_PDF}: ${BOOK_SOURCES}
# 	jb build -W -n --builder pdflatex .

# publish: _build ${BOOK_PDF}
publish: _build
	mv _build/html $@
	cp -r src $@
	# mv ${BOOK_PDF} $@/ssdd-lab.pdf
	# cp -r assets $@

clean:
	jb clean .
	find . -name "*~" -delete
	rm -rf _build publish

check:
	pre-commit run --all

code-checks:
	pylint src/*/*.py
	pycodestyle src/*/**.py
	pydocstyle src/*/*.pydocstyle

view: _build
	xdg-open _build/html/index.html

code:
	git clone https://github.com/UCLM-ARCO/net-book-code.git code
