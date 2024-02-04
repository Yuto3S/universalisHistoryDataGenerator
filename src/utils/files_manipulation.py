import os


def get_files_tree_starting_on_folder(startpath):
    """
    Starts in a given folder and return the tree as a dict. This only works in our history formatted folder,
    where files are only at the lowest level and never in between.
    """
    tree_as_dict = {}
    parent_keys = []
    previous_level = -1

    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, "").count(os.sep)

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
