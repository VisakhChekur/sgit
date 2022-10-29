from pathlib import Path

class FileHandler:



    @staticmethod
    def make_path(repo: str, *paths: str):
        
        return Path(repo).joinpath(*paths)




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
