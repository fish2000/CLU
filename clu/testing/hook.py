# -*- coding: utf-8 -*-

try:
    # Import the main pytest API entry point:
    import pytest

except (ImportError, RuntimeError):
    pass

else:
    @pytest.hookspec(firstresult=True)
    def pytest_delete_temps_default():
        """ Return the default value for the “delete-temps” option """
