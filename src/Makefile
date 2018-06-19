BUILD=../build/
TEST=../test/
TAR_FILE=apc.tar.gz
TEMP_FILES=*.pyc *.pyo
TEMP_DIRS=__pycache__
ADAFRUIT=../lib/Adafruit_Python_DHT

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
	tar -zcvf ${TAR_FILE} launcher.sh *.py ${ADAFRUIT}
	mkdir ${BUILD}
	mv ${TAR_FILE} ${BUILD}
	@echo
