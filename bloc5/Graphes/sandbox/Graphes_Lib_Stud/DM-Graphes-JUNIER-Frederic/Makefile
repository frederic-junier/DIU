.PHONY : fresh clean all

all:
	python3 main_junier_frederic.py pdf
	pandoc -s activite-eleve.md  -o activite-eleve.pdf
	pandoc -s activite-eleve.md   -o activite-eleve.odt
    

clean:
	rm  activite-eleve.pdf activite-eleve.odt
	rm -r images

fresh: clean all

