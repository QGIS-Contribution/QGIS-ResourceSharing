# Imports
from .base import BasePlatform
from .github import GitHubPlatform
from .bitbucket import BitbucketPlatform
from .friendcode import FriendCodePlatform
from .assembla import AssemblaPlatform
from .gogs import GogsPlatform
from .gitlab import GitLabPlatform


# Supported platforms
PLATFORMS = (
    # name -> Platform object
    ('github', GitHubPlatform()),
    ('bitbucket', BitbucketPlatform()),
    ('friendcode', FriendCodePlatform()),
    ('assembla', AssemblaPlatform()),
    ('gogs', GogsPlatform()),
    ('gitlab', GitLabPlatform()),

    # Match url
    ('base', BasePlatform()),
)

PLATFORMS_MAP = dict(PLATFORMS)
