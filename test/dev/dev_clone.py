# standard
import shutil
import time
from pathlib import Path

# 3rd party
from dulwich import porcelain

# -- VARIABLES
git_remote_repo = "https://github.com/faunalia/QGIS-Resources.git"

local_repo_dir_no_depth = Path("test/fixtures/git_without_depth")
local_repo_dir_git_no_depth = local_repo_dir_no_depth / ".git"

local_repo_dir_with_depth = Path("test/fixtures/git_with_depth")
local_repo_dir_git_with_depth = local_repo_dir_with_depth / ".git"

# -- CLONE OPERATION ---------------------------------------------------

# WITHOUT DEPTH
start_time = time.time()
repo = porcelain.clone(
    source=git_remote_repo,
    target=str(local_repo_dir_no_depth),
)
repo.close()
print("CLONE WITHOUT DEPTH: %s seconds" % (time.time() - start_time))

# WITH DEPTH
start_time = time.time()
repo = porcelain.clone(
    source=git_remote_repo,
    target=str(local_repo_dir_with_depth),
    depth=1
)
repo.close()
print("CLONE WITH DEPTH: %s seconds" % (time.time() - start_time))

# -- PULL OPERATION ------------------------------------------------------

# WITHOUT DEPTH
start_time = time.time()
repo = porcelain.pull(
    remote_location=git_remote_repo,
    repo=str(local_repo_dir_no_depth),
)
print("PULL WITHOUT DEPTH: %s seconds" % (time.time() - start_time))

# WITH DEPTH
start_time = time.time()
repo = porcelain.pull(
    remote_location=git_remote_repo,
    repo=str(local_repo_dir_with_depth)
)
print("PULL WITH DEPTH: %s seconds" % (time.time() - start_time))

# -- CLEANING
shutil.rmtree(local_repo_dir_no_depth)
shutil.rmtree(local_repo_dir_with_depth)
