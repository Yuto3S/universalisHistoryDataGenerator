from git import Repo


def push_generated_to_git(folder_name, list_of_servers, timeframe_hours, custom_path):
    try:
        repo = Repo(f"{custom_path}")
        repo.git.add(f"{custom_path}assets/generated/history")
        repo.git.add(f"{custom_path}assets/generated/history_tree.json")
        repo.index.commit(
            f"New shopping list informations for {folder_name} - "
            f"{[server.value for server in list_of_servers]} - "
            f"over the last {timeframe_hours.value} hours. "
        )
        origin = repo.remote(name="origin")
        origin.push()
    except Exception:
        print("Some error occured while pushing the code")
