# -*- coding: utf-8 -*-

try:
    # Import the main pytest API entry point:
    import pytest

except ImportError:
    pass

else:
    @pytest.hookspec(firstresult=True)
    def pytest_delete_temporary_default():
        """ Return the default value for the “delete-temporary” option """
