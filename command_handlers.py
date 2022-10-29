from git_repo import GitRepository
from helpers import initialize_repository

def handle_init(path: str):

    try:
        initialize_repository(path)
        return GitRepository(path)
    except Exception as e:
        print(f"ERROR: {str(e)}")
    
