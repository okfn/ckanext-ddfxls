# Re-export the ``clean_datastore`` fixture defined in CKAN core's
# ``ckanext/datastore/tests/conftest.py``. Pytest only auto-discovers
# conftests inside the project rootdir, so without this re-export
# the fixture isn't visible to extension tests.
from ckanext.datastore.tests.conftest import clean_datastore  # noqa: F401
