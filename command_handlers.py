from git_repo import GitRepository

def handle_init(path: str):

    try:
        return GitRepository.initialize_repository(path)
    except Exception as e:
        print(f"ERROR: {str(e)}")