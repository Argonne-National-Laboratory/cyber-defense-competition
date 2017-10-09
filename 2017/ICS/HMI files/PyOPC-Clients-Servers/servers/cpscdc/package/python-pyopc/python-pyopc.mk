#################################################################################
#
#python-pyopc
#
#################################################################################

PYTHON_PYOPC_VERSION = 0.1a
PYTHON_PYOPC_SOURCE = PyOPC-0.1a.zip
PYTHON_PYOPC_SITE = http://downloads.sourceforge.net/project/pyopc/pyopc/PyOPC-0.1a/PyOPC-0.1a.zip 
PYTHON_PYOPC_SETUP_TYPE = setuptools

define PYTHON_PYOPC_EXTRACT_CMDS
	unzip $(DL_DIR)/$(PYTHON_PYOPC_SOURCE) -d $(@D)
endef

define PYTHON_PYOPC_INSTALL_TARGET_CMDS
	mv $(@D)/PyOPC-0.1/PyOPC $(TARGET_DIR)/usr/lib/python2.7/site-packages
endef

$(eval $(generic-package))
