from git import Repo

from src.consts import FILE_PATH_GENERATED_HISTORY
from src.consts import FILE_PATH_GENERATED_HISTORY_TREE
from src.utils.files import get_root_project_path


def push_generated_to_git(folder_name, list_of_servers, timeframe_hours):
    project_path = get_root_project_path()
    try:
        repo = Repo(f"{project_path}")
        repo.git.add(f"{project_path}{FILE_PATH_GENERATED_HISTORY}")
        repo.git.add(f"{project_path}{FILE_PATH_GENERATED_HISTORY_TREE}")
        repo.index.commit(
            f"New shopping list informations for {folder_name} - "
            f"{[server.value for server in list_of_servers]} - "
            f"over the last {timeframe_hours.value} hours. "
        )
        origin = repo.remote(name="origin")
        origin.push()
    except Exception as e:
        print(f"Some error occured while pushing the code with {e}")
