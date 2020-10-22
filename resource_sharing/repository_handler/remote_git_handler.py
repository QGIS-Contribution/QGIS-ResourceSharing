# coding=utf-8
import logging
import shutil
import traceback
import warnings
from pathlib import Path

from dulwich import porcelain
from giturlparse import parse, validate
from qgis.core import QgsApplication
from resource_sharing.repository_handler.base import BaseRepositoryHandler
from resource_sharing.utilities import local_collection_path

LOGGER = logging.getLogger("QGIS Resource Sharing")


class writeOut:
    """Stderr mock"""

    @classmethod
    def write(cls, m):
        LOGGER.debug("Dulwich/Porcelain (github): " + m.decode("utf8"))

    @classmethod
    def flush(cls):
        pass

    @classmethod
    def isatty(cls):
        return False


class RemoteGitHandler(BaseRepositoryHandler):
    """Class to handle generic git remote repository."""

    IS_DISABLED = True

    def __init__(self, url: str):
        """Constructor."""
        BaseRepositoryHandler.__init__(self, url)
        self._git_platform = None
        self._git_host = None
        self._git_owner = None
        self._git_repository = None

        # Call proper setters here
        self.url = url

    def can_handle(self):
        return False

    @BaseRepositoryHandler.url.setter
    def url(self, url: str):
        """Setter to the repository's URL."""
        if validate(url):
            self._url = url
            git_parse = parse(url)
            self._git_platform = git_parse.platform
            self._git_host = git_parse.host
            self._git_owner = git_parse.owner
            self._git_repository = git_parse.repo
            LOGGER.debug("git parse URL: " + str(url))
            LOGGER.debug(" platform: " + str(git_parse.platform))
            LOGGER.debug(" host: " + str(git_parse.host))
            LOGGER.debug(" owner: " + str(git_parse.owner))
            LOGGER.debug(" repository: " + str(git_parse.repo))

    @property
    def git_platform(self):
        return self._git_platform

    @property
    def git_host(self):
        return self._git_host

    @property
    def git_owner(self):
        return self._git_owner

    @property
    def git_repository(self):
        return self._git_repository

    def download_collection(self, id: str, register_name: str) -> tuple:
        """Download a collection given its ID.

        For remote git repositories, we will clone the repository (or
        pull if the repo is already cloned), and copy the collection to
        the collections directory.

        :param id: The ID of the collection.
        :type id: str
        :param register_name: The register name of the collection (the
            section name of the collection)
        :type register_name: unicode
        :return: (success (True or False), error message (None if success))
        :rtype: (boolean, string)
        """
        # Hack to avoid irritating Dulwich / Porcelain ResourceWarning
        warnings.filterwarnings("ignore", category=ResourceWarning)
        # Clone or pull the repositories first
        local_repo_dir = Path(
            QgsApplication.qgisSettingsDirPath(),
            "resource_sharing",
            "repositories",
            self.git_host,
            self.git_owner,
            self.git_repository,
        )
        # Hack to try to avoid locking errors
        # if local_repo_dir.exists():
        #     try:
        #         shutil.rmtree(str(local_repo_dir))
        #     except Exception:
        #         pass
        if not (local_repo_dir / ".git").exists():
            local_repo_dir.mkdir(parents=True)
            try:
                repo = porcelain.clone(
                    source=self.url,
                    target=str(local_repo_dir),
                    errstream=writeOut,
                    depth=1,
                )
                repo.close()  # Try to avoid WinErr 32
            except Exception as e:
                # Try to clone with https if it is a ssh url
                git_parsed = parse(self.url)
                if self.url == git_parsed.url2ssh:
                    try:
                        repo = porcelain.clone(
                            source=git_parsed.url2https,
                            target=str(local_repo_dir),
                            errstream=writeOut,
                            depth=1,
                        )
                        repo.close()  # Try to avoid WinErr 32
                    except Exception as e:
                        error_message = "Error: %s" % str(e)
                        LOGGER.exception(traceback.format_exc())
                        return False, error_message
                else:
                    error_message = "Error: %s" % str(e)
                    LOGGER.exception(traceback.format_exc())
                    return False, error_message

            if not repo:
                error_message = (
                    "Error: Cloning the repository of the collection failed."
                )
                return False, error_message
        else:
            # Hack until dulwich/porcelain handles file removal ???!!!
            # if local_repo_dir.exists():
            #     shutil.rmtree(str(local_repo_dir))
            try:
                porcelain.pull(
                    repo=str(local_repo_dir),
                    remote_location=self.url,
                    refspecs=b"refs/heads/master",
                    errstream=writeOut,
                )
            except Exception as e:
                # Try to pull with https if it's ssh url
                git_parsed = parse(self.url)
                if self.url == git_parsed.url2ssh:
                    try:
                        porcelain.pull(
                            repo=str(local_repo_dir),
                            remote_location=git_parsed.url2https,
                            refspecs=b"refs/heads/master",
                            errstream=writeOut,
                        )
                    except Exception as e:
                        error_message = "Error: %s" % str(e)
                        LOGGER.exception(traceback.format_exc())
                        return False, error_message
                else:
                    error_message = "Error: %s" % str(e)
                    LOGGER.exception(traceback.format_exc())
                    return False, error_message

        # Copy the specific downloaded collection to the collections dir
        src_dir = local_repo_dir / "collections" / register_name
        if not src_dir.exists():
            error_message = "Error: The collection does not exist in the repository."
            return False, error_message

        dest_dir = local_collection_path(id)
        if dest_dir.exists():
            # Remove the existing collection directory
            shutil.rmtree(str(dest_dir))
        shutil.copytree(str(src_dir), str(dest_dir))

        return True, None
