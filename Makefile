# Makefile for cmsplugin-zinnia
#
# Aim to simplify development and release process
# Be sure you have run the buildout, before using this Makefile

NO_COLOR	= \033[0m
COLOR	 	= \033[32;01m
SUCCESS_COLOR	= \033[35;01m

all: kwalitee clean package

package:
	@echo "$(COLOR)* Creating source package for cmsplugin-innia$(NO_COLOR)"
	@python setup.py sdist

kwalitee:
	@echo "$(COLOR)* Running pyflakes$(NO_COLOR)"
	@./bin/pyflakes cmsplugin_zinnia
	@echo "$(COLOR)* Running pep8$(NO_COLOR)"
	@./bin/pep8 --count --show-source --show-pep8 --statistics --exclude=migrations cmsplugin_zinnia
	@echo "$(SUCCESS_COLOR)* No kwalitee errors, Congratulations ! :)$(NO_COLOR)"

clean:
	@echo "$(COLOR)* Removing useless files$(NO_COLOR)"
	@find demo_cmsplugin_zinnia cmsplugin_zinnia docs -type f \( -name "*.pyc" -o -name "\#*" -o -name "*~" \) -exec rm -f {} \;
	@rm -f \#* *~


