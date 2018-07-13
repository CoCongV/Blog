from whoosh import index
from whoosh.fields import Schema


class SanicIndexSerivce:

    def init_app(self, app, session=None, whoosh_base=None):
        self.indexdir = app.config.get('WHOOSH_INDEX_DIR', '/tmp/indexdir')
    
    # def register_schema(self, index: str, schema: Schema):
