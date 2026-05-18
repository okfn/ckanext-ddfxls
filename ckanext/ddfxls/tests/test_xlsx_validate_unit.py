"""Unit tests for ``xlsx_validate`` (no DB; ``datastore_search`` is mocked)."""

import unittest.mock as mock
from ckanext.ddfxls.validators import xlsx_validate, XLSX_MAX_COLS, XLSX_MAX_ROWS


def _mock_search(fields_count, total):
    """Stub out the ``datastore_search`` action with a canned result.

    Uses the same pattern as CKAN core (see
    ``ckan/tests/logic/action/test_patch.py``): patch
    ``ckan.logic._actions`` so any ``get_action('datastore_search')``
    call — from toolkit, plugins, or logic — picks up the mock.
    """
    fake_result = {
        "fields": [{"id": f"f{i}"} for i in range(fields_count)],
        "total": total,
    }
    fake_action = mock.MagicMock(return_value=fake_result)
    return mock.patch.dict(
        "ckan.logic._actions", {"datastore_search": fake_action}
    )


class TestXlsxValidateUnit:
    def test_within_limits_returns_none(self):
        with _mock_search(fields_count=10, total=100):
            assert xlsx_validate("res-id") is None

    def test_exactly_at_row_limit_is_rejected(self):
        # Excel allows 1,048,576 rows *including* the header row, so a
        # resource with 1,048,576 data rows would overflow by one.
        with _mock_search(fields_count=2, total=XLSX_MAX_ROWS):
            reason = xlsx_validate("res-id")
        assert reason is not None
        assert "rows" in reason.lower()

    def test_just_under_row_limit_is_allowed(self):
        with _mock_search(
            fields_count=2, total=XLSX_MAX_ROWS - 1
        ):
            assert xlsx_validate("res-id") is None

    def test_too_many_rows_is_rejected(self):
        with _mock_search(fields_count=2, total=5_000_000):
            reason = xlsx_validate("res-id")
        assert reason is not None
        assert "rows" in reason.lower()
        assert "5,000,000" in reason

    def test_too_many_columns_is_rejected(self):
        with _mock_search(
            fields_count=XLSX_MAX_COLS + 1, total=10
        ):
            reason = xlsx_validate("res-id")
        assert reason is not None
        assert "columns" in reason.lower()

    def test_column_limit_takes_precedence_over_row_limit(self):
        # When both are over the limit, the column message is returned
        # first. Pins the current behavior; if it changes, update.
        with _mock_search(
            fields_count=XLSX_MAX_COLS + 1,
            total=XLSX_MAX_ROWS + 1,
        ):
            reason = xlsx_validate("res-id")
        assert reason is not None
        assert "columns" in reason.lower()
