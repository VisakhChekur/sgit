from git_repo import GitRepository
from helpers import initialize_repository, find_git_repo_path

def handle_init(path: str):

    try:
        initialize_repository(path)
        GitRepository(path)
    except Exception as e:
        print(f"ERROR: {str(e)}")
    
def handle_trial(path: str):

    git_repo_path = find_git_repo_path(path)
    print(GitRepository(git_repo_path.resolve()).working_tree)