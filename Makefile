# convenience Makefile to run validation tests
# src: source path discovered in run time
# minimum_test_coverage: minimun test coverage allowed
# pep8_ignore: ignore listed PEP 8 errors and warnings
# max_complexity: maximum McCabe complexity allowed
# csslint_ignore: skip file names matching find pattern (use ! -name PATTERN)
# jshint_ignore: skip file names matching find pattern (use ! -name PATTERN)

SHELL = /bin/bash

src = `find . -type d | grep -m 1 "sc/contentrules/metadata"`
minimum_test_coverage = 80
pep8_ignore = E501
max_complexity = 12
csslint_ignore = ! -name jquery\*
jshint_ignore = ! -name jquery\*

NO_COLOR = \x1b[0m
OK_COLOR = \x1b[32;01m
ERROR_COLOR = \x1b[31;01m
WARN_COLOR = \x1b[33;01m

OK_STRING = $(OK_COLOR)[ok]$(NO_COLOR)
ERROR_STRING = $(ERROR_COLOR)[errors]$(NO_COLOR)
WARN_STRING = $(WARN_COLOR)[warnings]$(NO_COLOR)

code-validation:
	bin/flake8 --ignore=$(pep8_ignore) --max-complexity=$(max_complexity) $(src)

python-validation: code-validation
	@echo -e "$(WARN_COLOR)python-validation is deprecated; use code-validation instead$(NO_COLOR)"

css-validation:
	npm install csslint -g 2>/dev/null
	find $(src) -type f -name *.css $(csslint_ignore) | xargs csslint

js-validation:
	npm install jshint -g 2>/dev/null
	find $(src) -type f -name *.js $(jshint_ignore) | xargs jshint

coverage-validation:
	bin/coverage.sh $(minimum_test_coverage)

zpt-validation:
	find $(src) -type f -name *.pt | xargs /Users/erico/Simples/Produtos/sc.contentrules.metadata/bin/zptlint

i18n-validation:
	bin/i18ndude find-untranslated -n $(src)

basic-validation: code-validation zpt-validation i18n-validation
