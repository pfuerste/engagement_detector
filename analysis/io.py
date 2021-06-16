import os
import yaml
import numpy as np
from datetime import datetime


def sparsify(arr, ax=2, keep=0.25):
    """Returns a new array with only every keep*axis-lenght element along axis.

    Args:
        arr (np.array): initial array
        ax (int, optional): axis on which to delete elements. Defaults to 2.
        keep (float, optional): ratio of how may elements to keep along axis. Defaults to 0.25.

    Returns:
        np.array: reduced array
    """
    inds = np.arange(0, arr.shape[ax], 1 / keep, dtype=int)
    inds = [x for x in np.arange(arr.shape[ax]) if x not in inds]
    arr = np.delete(arr, inds, ax)
    return arr


def get_current_session_path(sessions_root, name):
    """Returns session_root/name/x with x being an identifier of the current time.
       Call at the beginning of a session.
    Args:
        sessions_root (str): path for data of all data
        name (str): lecture name, will be subdir in sessions_root

    Returns:
        str: path of new dir
    """
    now = datetime.now()
    return os.path.join(sessions_root, name, now.strftime('%Y%m%d%H'))  # +str(now.hour))


def get_latest_session_path(sessions_root, name):
    """Return path to dir of latest session with name.

    Args:
        sessions_root (str): path for data of all data
        name (str): lecture name, will be subdir in sessions_root

    Returns:
        str: path of latest dir
    """
    paths = os.listdir(os.path.join(sessions_root, name))
    paths = [os.path.join(sessions_root, name, x) for x in paths]
    dirs = [x for x in paths if os.path.isdir(x)]
    dates = list()
    for dir in dirs:
        try:
            date = dir.split(os.sep)[-1]
            date = datetime.strptime(date, '%Y%m%d%H')
            dates.append(date)
        except ValueError:
            pass
    return os.path.join(sessions_root, name, max(dates).strftime('%Y%m%d%H'))


def save_session(name, ids, scores, keep=1.0):
    if scores.ndim == 3 and keep != 1.0:
        scores = sparsify(scores, keep=keep)
    # TODO
    pass


def load_session():
    # TODO
    pass


if __name__ == "__main__":
    sessions_root = yaml.safe_load(open("config.yml"))["sessions_root"]
    #os.makedirs(get_current_session_path(sessions_root, "test"))
    print(get_latest_session_path(sessions_root, "test"))
    # a = np.array([np.arange(0, 20), np.arange(0, 20)])
    # print(sparsify(a, 0, 0.5))
    pass
