import os
from urllib.parse import urljoin

import aiofiles


class Upload:

    def init_app(self, app):
        self.path = os.path.join(app.config.UPLOAD_PATH)
        self.upload_url = app.config.UPLOAD_URL

    async def save(self, file, path):
        filepath = os.path.join(self.path, path, file.name)
        async with aiofiles.open(
                os.path.join(filepath), mode='w') as f:
            await f.write(file)
        return os.path.join(path, file.name)

    async def url(self, path):
        return urljoin(self.upload_url, path)
