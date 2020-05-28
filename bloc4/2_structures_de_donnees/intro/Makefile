all: intro_structures.tex
	rubber -v --warn all --pdf $<

push: intro_structures.pdf
	cp $< ..

clean:
	rm -f *.aux
	rm -f *.log
	rm -f *.out
	rm -f *.snm
	rm -f *.toc
	rm -f *.vrb
	rm -f *.nav
	rm -f *~
	rm -f flags.tex
