from patch import Patch
from typing import List
from common import JSONable


class PatchHolder(JSONable):
        def __init__(self, version: int):
                self.version = version
                self.patches = {}

        def create_patch(self) -> Patch:
                last = self.version
                self._increment_version()
                current = self.version
                patch = Patch(last, current)
                self.patches[last] = patch
                return patch

        def _increment_version(self):
                self.version += 1

        def get_patches(self, foreign_version: int) -> List[Patch]:
                patches = []
                while foreign_version != self.version:
                        patch = self.patches[foreign_version]
                        patches.append(patch)
                        foreign_version = patch.current
                return patches
