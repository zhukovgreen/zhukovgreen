import logging
import pathlib
import sys

from envparse import env
from git import Repo
from github import Github
from github.GithubException import UnknownObjectException
from github.Repository import Repository


ROOT_PATH = pathlib.Path(__file__).parents[1]
env.read_envfile(ROOT_PATH / ".env")

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO
    if not env.bool("DEBUG", default=False)
    else logging.DEBUG,
)
logger = logging.getLogger(__file__)

local_repo = Repo(ROOT_PATH)

g = Github(login_or_token=env.str("GITHUB_TOKEN"))
logger.info("Github authenticated")

repo: Repository = g.get_repo("ZhukovGreen/CV")
logger.info("Repository loaded")
for file in (
    f
    for f in [f.a_path for f in local_repo.index.diff(None)]
    + local_repo.untracked_files
    if f[-3:] == "pdf" or f == "README.md"
):
    try:
        contents_sha = repo.get_contents(
            file, ref=local_repo.head.commit.hexsha
        ).sha
    except UnknownObjectException:
        contents_sha = ""
    response = repo.update_file(
        path=file,
        sha=contents_sha,
        content=(ROOT_PATH / file).read_bytes(),
        message=f"Added {file} [skip ci]",
        branch="master",
    )
    logger.info(f"File {file} was added with the commit {response['commit']}")
