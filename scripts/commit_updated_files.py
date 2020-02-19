import logging
import pathlib
import sys

from envparse import env
from git import Repo, Head
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
    branch_name = ""
    for branch in local_repo.branches:
        branch: Head
        if branch.commit.hexsha == local_repo.head.commit.hexsha:
            branch_name = branch.name
    try:
        contents_sha = repo.get_contents(
            file, ref=local_repo.head.object.hexsha
        ).sha
    except UnknownObjectException:
        contents_sha = ""
    response = repo.update_file(
        path=file,
        sha=contents_sha,
        content=(ROOT_PATH / file).read_bytes(),
        message=f"Added {file} [skip ci]",
        branch=branch_name,
    )
    logger.info(f"File {file} was added with the commit {response['commit']}")
