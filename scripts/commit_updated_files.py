import logging
import pathlib
import sys

from envparse import env
from git import Repo, Head
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
    for f in local_repo.untracked_files
    if f[-3:] == "pdf" or f == "README.md"
):
    branch_name = ""
    for branch in local_repo.branches:
        branch: Head
        logger.debug(
            f"Checking branch {branch.name} with "
            f"head at {branch.commit.hexsha}. Looking "
            f"for {local_repo.head.commit.hexsha}"
        )
        if branch.commit.hexsha == local_repo.head.commit.hexsha:
            branch_name = branch.name
            logger.debug(
                f"Branch {branch_name} matches the "
                f"commit {local_repo.head.commit.hexsha}"
            )
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
        branch=branch_name,
    )
    logger.info(f"File {file} was added with the commit {response['commit']}")
