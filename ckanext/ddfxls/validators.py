from ckan.plugins import toolkit


# Excel hard limits (per worksheet; XLSX_MAX_ROWS includes the header row).
# https://support.microsoft.com/en-us/office/excel-specifications-and-limits-1672b34d-7043-467e-8e27-269d656771c3
XLSX_MAX_COLS = 16384
XLSX_MAX_ROWS = 1048576


def xlsx_validate(resource_id):
    """Return None if the resource fits in a single XLSX sheet, or a
    translatable reason string otherwise.

    Cheap on the common path: datastore_search with limit=0 fetches
    no rows, and include_total uses CKAN's cached_table_row_count
    (a single PK lookup on _table_stats once the cache is primed).
    """
    result = toolkit.get_action('datastore_search')(
        {},
        {
            'resource_id': resource_id,
            'limit': 0,
            'include_total': True,
        },
    )
    n_cols = len(result['fields'])
    n_rows = result['total']

    if n_cols > XLSX_MAX_COLS:
        return toolkit._(
            'XLSX supports at most {max:,} columns; '
            'this resource has {n:,}. Use CSV or JSON for the full export.'
        ).format(max=XLSX_MAX_COLS, n=n_cols)

    if n_rows >= XLSX_MAX_ROWS:
        return toolkit._(
            'XLSX supports at most {max:,} rows; '
            'this resource has {n:,}. Use CSV or JSON for the full export.'
        ).format(max=XLSX_MAX_ROWS - 1, n=n_rows)

    return None
