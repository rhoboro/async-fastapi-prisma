import os
import logging
from pathlib import Path
from pydantic import BaseModel

from . import platform
from .utils import download
from .. import config


__all__ = ('Binary',)

log: logging.Logger = logging.getLogger(__name__)


class Binary(BaseModel):
    name: str
    env: str

    def download(self) -> None:
        # TODO: respect schema binary options
        url = self.url
        dest = self.path

        if dest.exists():
            log.debug('%s is cached, skipping download', self.name)
            return

        log.debug('Downloading from %s to %s', url, dest)
        download(url, str(dest.absolute()))
        log.debug('Downloaded %s to %s', self.name, dest.absolute())

    @property
    def url(self) -> str:
        return platform.check_for_extension(config.prisma_url).format(
            version=config.prisma_version, platform=platform.name()
        )

    @property
    def path(self) -> Path:
        env = os.environ.get(self.env)
        if env is not None:
            log.debug(
                'Using environment variable location: %s for %s',
                env,
                self.name,
            )
            return Path(env)

        return config.binary_cache_dir.joinpath(
            platform.check_for_extension(self.name)
        )
