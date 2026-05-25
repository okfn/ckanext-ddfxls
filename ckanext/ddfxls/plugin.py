from ckan import plugins
from ckan.plugins import toolkit
from ckanext.datastore.interfaces import IDatastoreDump
from ckanext.ddfxls.writers import xlsx_writer

# Excel hard limits (per worksheet). XLSX_MAX_ROWS is the number of data
# rows that fit alongside the single header row (1,048,576 total - 1).
# https://support.microsoft.com/en-us/office/excel-specifications-and-limits-1672b34d-7043-467e-8e27-269d656771c3
XLSX_MAX_COLS = 16384
XLSX_MAX_ROWS = 1048575


class DdfxlsPlugin(plugins.SingletonPlugin):
    plugins.implements(IDatastoreDump)

    # IDatastoreDump

    def register_dump_formats(self):
        """Register XLSX format for datastore exports.

        Availability is enforced by CKAN core via the declarative
        ``max_columns``/``max_rows`` limits below: core compares them
        against the *filtered* export scope and disables the format (and
        returns HTTP 400) when exceeded, generating the reason message
        itself. The XLSX writer buffers the whole workbook in memory, so
        these limits also bound that memory to a single worksheet.
        """
        return {
            "xlsx": {
                "label": toolkit._('Excel'),
                "writer_factory": xlsx_writer,
                "records_format": "objects",
                "content_type": ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
                "file_extension": "xlsx",
                "max_columns": XLSX_MAX_COLS,
                "max_rows": XLSX_MAX_ROWS,
            }
        }
