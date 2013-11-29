# Makefile for cmsplugin-zinnia
#
# Aim to simplify development and release process
# Be sure you have run the buildout, before using this Makefile

NO_COLOR	= \033[0m
COLOR	 	= \033[32;01m
SUCCESS_COLOR	= \033[35;01m

all: kwalitee clean package

package:
	@echo "$(COLOR)* Creating source package for cmsplugin-zinnia$(NO_COLOR)"
	@python setup.py sdist

translations:
	@echo "$(COLOR)* Linking demo templates$(NO_COLOR)"
	@ln -s ../../demo_cmsplugin_zinnia/templates/cms/ cmsplugin_zinnia/templates/
	@echo "$(COLOR)* Generating english translation$(NO_COLOR)"
	@cd cmsplugin_zinnia && ../bin/demo makemessages --extension=.html,.txt -s -l en
	@echo "$(COLOR)* Pushing translation to Transifex$(NO_COLOR)"
	@tx push -s
	@echo "$(COLOR)* Remove english translation$(NO_COLOR)"
	@rm -rf cmsplugin_zinnia/locale/en/
	@echo "$(COLOR)* Remove symbolic links$(NO_COLOR)"
	@rm -rf cmsplugin_zinnia/templates/cms

kwalitee:
	@echo "$(COLOR)* Running flake8$(NO_COLOR)"
	@./bin/flake8 --count --show-source --show-pep8 --statistics --exclude=migrations cmsplugin_zinnia
	@echo "$(SUCCESS_COLOR)* No kwalitee errors, Congratulations ! :)$(NO_COLOR)"

clean:
	@echo "$(COLOR)* Removing useless files$(NO_COLOR)"
	@find demo_cmsplugin_zinnia cmsplugin_zinnia docs -type f \( -name "*.pyc" -o -name "\#*" -o -name "*~" \) -exec rm -f {} \;
	@rm -f \#* *~


