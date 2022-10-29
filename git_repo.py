from configparser import ConfigParser
from pathlib import Path

from helpers import make_path
from exceptions import ConfigFileNotFound, NotGitRepoException

class GitRepository:
    
    def __init__(self, path: str | Path):

        # Represents the .git directory
        self.git_dir = make_path(path, ".git")

        # Working tree i.e the directory that git is watching
        self.working_tree = Path(path)

        # Validations
        if not self.git_dir.is_dir():
            raise NotGitRepoException(f"no git repository found at '{self.git_dir.resolve()}'")
        
        config_path = make_path(path, ".git", "config")
        if not config_path.exists():
            raise ConfigFileNotFound("config file was not found in `.git` directory")
        
        self.config = ConfigParser()
        self.config.read(config_path)
    
    

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