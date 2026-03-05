def parse_repo_url(repo_url: str):
    parts = repo_url.rstrip("/").split("/")

    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL")

    owner = parts[-2]
    repo = parts[-1]

    return owner, repo