from ckan import plugins
from ckan.plugins import toolkit

from ckanext.datastore.interfaces import IDatastoreDump
from ckanext.ddfxls.writers import xlsx_writer


class DdfxlsPlugin(plugins.SingletonPlugin):
    plugins.implements(IDatastoreDump)

    # IDatastoreDump

    def register_dump_formats(self):
        """Register XLSX format for datastore exports"""
        return {
            "xlsx": {
                "writer_factory": xlsx_writer,
                "records_format": "objects",
                "content_type": ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
                "file_extension": "xlsx",
            }
        }
