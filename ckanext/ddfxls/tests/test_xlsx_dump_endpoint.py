"""Happy-path integration test for the xlsx dump endpoint.

The validator contract itself (rejection with 400, helper marking
formats unavailable, template rendering a disabled dropdown item) is
covered in CKAN core's ``TestDatastoreDumpValidate`` using
``sample_dump_plugin``. Here we only check that ddfxls's specific
xlsx wiring (label, Content-Type, file extension) is correct
end-to-end against the real ``/datastore/dump`` route.
"""

import pytest

import ckan.tests.factories as factories
import ckan.tests.helpers as helpers


@pytest.mark.ckan_config("ckan.plugins", "datastore ddfxls")
@pytest.mark.usefixtures("clean_datastore", "with_plugins")
class TestXlsxDumpEndpoint:

    def test_dump_succeeds_when_within_limits(self, app):
        resource = factories.Resource(url_type="datastore")
        helpers.call_action(
            "datastore_create",
            resource_id=resource["id"],
            records=[{"book": "annakarenina"}, {"book": "warandpeace"}],
        )

        response = app.get(
            f"/datastore/dump/{resource['id']}?format=xlsx"
        )
        assert response.status_code == 200
        assert (
            response.headers["Content-Type"]
            == "application/vnd.openxmlformats-"
              "officedocument.spreadsheetml.sheet"
        )
        assert (
            f'filename="{resource["id"]}.xlsx"'
            in response.headers["Content-disposition"]
        )
