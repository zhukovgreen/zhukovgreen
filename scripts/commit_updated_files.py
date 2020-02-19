import logging
import pathlib
import sys

from envparse import env
from git import Repo
from github import Github
from github.GithubException import UnknownObjectException
from github.Repository import Repository

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__file__)


ROOT_PATH = pathlib.Path(__file__).parents[1]
env.read_envfile(ROOT_PATH / ".env")

local_repo = Repo(ROOT_PATH)

g = Github(login_or_token=env.str("GITHUB_TOKEN"))
logger.info("Github authenticated")

repo: Repository = g.get_repo("ZhukovGreen/CV")
logger.info("Repository loaded")
for file in (
    f
    for f in local_repo.untracked_files
    if f[-3:] == "pdf" or f == "README.md"
):
    try:
        contents_sha = repo.get_contents(
            file, ref=local_repo.active_branch.name
        ).sha
    except UnknownObjectException:
        contents_sha = ""
    response = repo.update_file(
        path=file,
        sha=contents_sha,
        content=(ROOT_PATH / file).read_bytes(),
        message=f"Added {file} [skip ci]",
        branch=local_repo.active_branch.name,
    )
    logger.info(f"File {file} was added with the commit {response['commit']}")
