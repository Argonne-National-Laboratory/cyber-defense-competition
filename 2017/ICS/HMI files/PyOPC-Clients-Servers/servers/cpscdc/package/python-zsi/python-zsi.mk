#################################################################################
#
#python-zsi
#
#################################################################################

PYTHON_ZSI_VERSION = 2.0-rc3
PYTHON_ZSI_SOURCE = ZSI-2.0-rc3.tar.gz
PYTHON_ZSI_SITE = https://pypi.python.org/packages/source/Z/ZSI
PYTHON_ZSI_SETUP_TYPE = setuptools

$(eval $(python-package))
