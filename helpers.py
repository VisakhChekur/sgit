from pathlib import Path
from configparser import ConfigParser


def initialize_repository(path: str):
        
        # Directory status
        repo_dir = Path(path)
        if not repo_dir.exists():
            raise FileExistsError(f"'{repo_dir.resolve()}' does not exist")
        if not repo_dir.is_dir():
            raise NotADirectoryError(f"'{repo_dir.resolve()}' is not a directory")

        git_dir = repo_dir / ".git"
        if git_dir.exists():
            raise FileExistsError(f"git repository already exists at '{repo_dir.resolve()}'")

        git_dir.mkdir()
        for dir in ("objects", "refs"):
            (git_dir / dir).mkdir()
        

        with open(git_dir / "description", "w+") as f:
            f.write("Unnamed repository\nEdit this file to name the repository\n")
        with open(git_dir / "HEAD", "w+") as f:
            f.write("ref: refs/head/master\n")
        
        config = create_default_config()
        with open(git_dir / "config", "w+") as f:
            config.write(f)

        print(f"\nInitialized repository at `{repo_dir.resolve()}`")

def find_git_repo_path(path: str=".") -> Path:
    """Tries to find a git repository by looking for a '.git' directory
    up the folder structure recursively until the root is reached."""

    repo_path = Path(path)
    root = repo_path.root

    while str(repo_path) != root:
        git_dir = repo_path / ".git"
        if git_dir.is_dir():
            return repo_path
        repo_path = repo_path / ".."

    # Checking the root directory as well
    if (repo_path / ".git").is_dir():
        return repo_path
    
    raise Exception("git repository not found")


def make_path(repo: str | Path, *paths: str | Path):
    return Path(repo).joinpath(*paths)

def create_default_config():
    
    config = ConfigParser()
    config.add_section("core")
    
    core_configurations: dict[str, str] = {
        "repositoryformatversion": "0",
        "filemode": "false",
        "bare": "false",
    }
    for key, value in core_configurations.items():
        config.set("core", key, value)
    return config