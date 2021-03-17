__copyright__ = "Copyright (c) 2020 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import shutil

import os
from jina.drivers import BaseRecursiveDriver, FlatRecursiveMixin

from jina.hub.crafters.image.ImageNormalizer import _load_image


class PngToDiskDriver(FlatRecursiveMixin, BaseRecursiveDriver):
    def __init__(self, workspace=None, prefix='', top=10, *args, **kwargs):
        self.prefix = prefix
        self.top = top
        self.done = 0
        self.workspace = workspace or os.getenv('JINA_WORKSPACE') or 'workspace'
        self.folder = os.path.join(self.workspace, self.prefix)
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        super().__init__(*args, **kwargs)


    def _apply_all(
            self,
            docs: 'DocumentSet',
            *args,
            **kwargs,
        ) -> None:        
            for d in docs:
                if self.done <= self.top:
                    img = _load_image(d.blob, -1)
                    path = os.path.join(self.folder, f'{self.done}.png')
                    img.save(path)
                    self.done += 1
