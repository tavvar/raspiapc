BUILD="../build/"
TAR_FILE="apc_build.tar"
TEMP_FILES=*.pyc *.pyo
TEMP_DIRS=__pycache__

clean-pyc:
	@echo Cleaning temp files!
	rm -f ${TEMP_FILES}
	rm -rf ${TEMP_DIRS}
	@echo 

clean-build:
	@echo Cleaning build directory!
	rm --force --recursive ${BUILD}
	@echo

clean: clean-pyc clean-build

build-tar: clean-build
	@echo Building tar...
	tar -cf ${TAR_FILE} *.py
	mkdir ${BUILD}
	mv ${TAR_FILE} ${BUILD}
	@echo
