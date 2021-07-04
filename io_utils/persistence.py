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
       Creates that dir if not present.
       Call at the beginning of a session.

    Args:
        sessions_root (str): path for data of all data
        name (str): lecture name, will be subdir in sessions_root

    Returns:
        str: path of new dir
    """
    now = datetime.now()
    path = os.path.join(sessions_root, name, now.strftime('%Y%m%d%H'))
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def get_latest_session_path(sessions_root, name):
    """Return path to dir of latest session with name.

    Args:
        sessions_root (str): path for data of all data
        name (str): lecture name, will be subdir in sessions_root

    Returns:
        str: path of latest dir
    """
    return get_sorted_session_paths(sessions_root, name)[-1]


def get_sorted_session_paths(sessions_root, name):
    """Return time-sorted paths to dirs of session with name.

    Args:
        sessions_root (str): path for data of all data
        name (str): lecture name, will be subdir in sessions_root

    Returns:
        list: sorted list of paths of dirs
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
    dates = [os.path.join(sessions_root, name, date.strftime('%Y%m%d%H')) for date in sorted(dates)]
    return dates


def save_session(sessions_root, name, ids, scores, keep=1.0):
    # TODO Handle (merge?) multiple started session in the same hour in case of crash.
    """Save ids & scores to disk.
       
    Args:
        sessions_root (str): path for data of all data
        name (str): lecture name, will be subdir in sessions_root
        ids (np.array): array of face encodings
        scores (np.array): array of engagement scores
        keep (float, optional): ratio of how much of score's last dim to keep. Defaults to 1.0.
    """
    if scores.ndim == 3 and keep != 1.0:
        scores = sparsify(scores, keep=keep)
    dir = get_latest_session_path(sessions_root, name)
    print(ids.shape, scores.shape)
    np.save(os.path.join(dir, "ids.npy"), ids)
    np.save(os.path.join(dir, "scores.npy"), scores)


def load_all_sessions(sessions_root, name):
    """Loads ALL previous sessions of the lecture into memory.
       Memory consumption in Byte for one session: N*(128*sizeof(float)+T*4*sizeof(float))

    Args:
        sessions_root (str): path for data of all data
        name (str): lecture name, will be subdir in sessions_root

    Returns:
        tuple: of lists, ids and scores, time-sorted
    """
    session_paths = get_sorted_session_paths(sessions_root, name)
    ids = [np.load(os.path.join(x, "ids.npy")) for x in session_paths]
    scores = [np.load(os.path.join(x, "scores.npy")) for x in session_paths]
    return ids, scores


def load_last_session(sessions_root, name):
    """Loads most recent sessions of the lecture into memory.

    Args:
        sessions_root (str): path for data of all data
        name (str): lecture name, will be subdir in sessions_root

    Returns:
        tuple: ids and scores
    """
    session_path = get_latest_session_path(sessions_root, name)
    ids = np.load(os.path.join(session_path, "ids.npy"))
    scores = np.load(os.path.join(session_path, "scores.npy"))
    return ids, scores


if __name__ == "__main__":
    sessions_root = yaml.safe_load(open("config.yml"))["sessions_root"]
    # os.makedirs(get_current_session_path(sessions_root, "test"))
    print(get_latest_session_path(sessions_root, "test"))
    print(get_sorted_session_paths(sessions_root, "test"))
    # a = np.array([np.arange(0, 20), np.arange(0, 20)])
    # print(sparsify(a, 0, 0.5))
    pass
