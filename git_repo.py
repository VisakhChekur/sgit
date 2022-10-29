from configparser import ConfigParser
from pathlib import Path
from file_handler import FileHandler
from exceptions import ConfigFileNotFound, NotGitRepoException

class GitRepository:
    
    def __init__(self, path: str):

        # Represents the .git directory
        self.git_dir = FileHandler.make_path(path, ".git")

        # Working tree i.e the directory that git is watching
        self.working_tree = Path(path)

        # Validations
        if not self.git_dir.is_dir():
            raise NotGitRepoException(f"no git repository found at '{self.git_dir.resolve()}'")
        
        config_path = FileHandler.make_path(path, ".git", "config")
        if not config_path.exists():
            raise ConfigFileNotFound("config file was not found in `.git` directory")
        
        self.config = ConfigParser()
        self.config.read(config_path)
    
    @staticmethod
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
        
        config = GitRepository.create_default_config()
        with open(git_dir / "config", "w+") as f:
            config.write(f)

        print(f"\nInitialized repository at `{repo_dir.resolve()}`")
        return GitRepository(path)

    @staticmethod
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

"""
INIT

Create repository.
    - if directory doesn't exist, raise an exception
    - if directory exists, but isn't empty raise an exception
    - create .git directory
    - create the following subdirectories:
        - objects
        - refs
    - create the following files:
        - HEAD - ref: refs/heads/master\n
        - config - use configparser to create default configurations


"""