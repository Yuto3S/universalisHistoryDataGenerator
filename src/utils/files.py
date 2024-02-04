import json
import os


class MemoizeProjectPath:
    def __init__(self, func):
        self.project_path = None
        self.func = func

    def __call__(self):
        if self.project_path is None:
            self.project_path = self.func()

        return self.project_path


@MemoizeProjectPath
def get_project_path():
    if script_path := os.getenv("PYTHON_UNIVERSALIS_SCRIPT_PATH"):
        return script_path
    else:
        return os.path.dirname(os.path.realpath(__file__))


def get_files_tree_starting_on_folder(start_path):
    """
    Starts in a given folder and return the tree as a dict. This only works in our history formatted folder,
    where files are only at the lowest level and never in between.
    """
    tree_as_dict = {}
    parent_keys = []
    previous_level = -1

    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, "").count(os.sep)

        if previous_level >= level:
            for i in range(0, previous_level - level + 1):
                parent_keys.pop()

        parent_keys.append(os.path.basename(root))

        tmp_tree = tree_as_dict
        for i in range(0, len(parent_keys) - 1):
            tmp_tree = tmp_tree[parent_keys[i]]

        tmp_tree[os.path.basename(root)] = {}

        previous_level = level
        if files:
            tmp_tree[os.path.basename(root)] = [filename for filename in files]

    return tree_as_dict


def read_dict_from_file(file_path):
    with open(file_path, "r") as input_calculate_json_file:
        content = json.load(input_calculate_json_file)

    return content


def write_dict_content_on_file(file_content_as_dict, file_path):
    with open(file_path, "w") as file:
        file.write(json.dumps(file_content_as_dict))
