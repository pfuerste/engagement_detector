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
    path = os.path.join(sessions_root, name, now.strftime('%Y%m%d%H%M'))
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def get_latest_session_path(sessions_root, name):
    """Return path to dir of latest session with name.

    Args:
        sessions_root (str): path for data of all lectures
        name (str): lecture name, will be subdir in sessions_root

    Returns:
        str: path of latest dir
    """
    if not os.path.isdir(os.path.join(sessions_root, name)) or not os.listdir(os.path.join(sessions_root, name)):
        return []
    return get_sorted_session_paths(sessions_root, name)[-1]


def get_sorted_session_paths(sessions_root, name):
    """Return time-sorted paths to dirs of session with name.

    Args:
        sessions_root (str): path for data of all lectures
        name (str): lecture name, will be subdir in sessions_root

    Returns:
        list: sorted list of paths of dirs
    """
    if not os.path.isdir(os.path.join(sessions_root, name)):
        return []
    paths = os.listdir(os.path.join(sessions_root, name))
    paths = [os.path.join(sessions_root, name, x) for x in paths]
    dirs = [x for x in paths if os.path.isdir(x)]
    dates = list()
    for dir in dirs:
        try:
            date = dir.split(os.sep)[-1]
            date = datetime.strptime(date, '%Y%m%d%H%M')
            dates.append(date)
        except ValueError:
            pass
    dates = [os.path.join(sessions_root, name, date.strftime('%Y%m%d%H%M')) for date in sorted(dates)]
    return dates


def save_session(save_in, ids, scores, keep=1.0):
    """Save ids & scores to disk.
       Num for handling interruptions / crashes during one lecture.

    Args:
        # sessions_root (str): path for data of all lectures
        # name (str): lecture name, will be subdir in sessions_root
        save_in (str): path of current lecture dir
        ids (np.array): array of face encodings
        scores (np.array): array of engagement scores
        keep (float, optional): ratio of how much of score's last dim to keep. Defaults to 1.0.
    """
    if scores.ndim == 3 and keep != 1.0:
        scores = sparsify(scores, keep=keep)
    dir = save_in

    # delete half-sessions:
    if os.path.isfile(os.path.join(dir, "ids.npy")):
        os.remove(os.path.join(dir, "ids.npy"))
    if os.path.isfile(os.path.join(dir, "scores.npy")):
        os.remove(os.path.join(dir, "scores.npy"))
    # Saving after one iteration needs a new dim
    if scores.ndim == 2:
        scores = np.expand_dims(scores, axis=2)
        ids = np.expand_dims(ids, axis=2)
    np.save(os.path.join(dir, "ids.npy"), ids)
    np.save(os.path.join(dir, "scores.npy"), scores)


def load_all_sessions(sessions_root, name, as_lists=False):
    """Loads ALL previous sessions of the lecture into memory.
       Memory consumption in Byte for one session: N*(128*sizeof(float)+T*4*sizeof(float))

    Args:
        sessions_root (str): path for data of all lectures
        name (str): lecture name, will be subdir in sessions_root

    Returns:
        tuple: of lists, ids and scores, time-sorted
    """
    session_paths = get_sorted_session_paths(sessions_root, name)
    # print(session_paths)
    ids = [np.load(os.path.join(x, "ids.npy"), allow_pickle=True) for x in session_paths]
    scores = [np.load(os.path.join(x, "scores.npy"), allow_pickle=True) for x in session_paths]
    # for score in scores:
    #     print(score.shape)
    if as_lists:
        ids = [[list(person) for person in session] for session in ids]
        scores = [[[list(emotion) for emotion in person] for person in session] for session in scores]
    return ids, scores


def load_last_session(sessions_root, name, as_lists=False):
    """Loads most recent sessions of the lecture into memory.

    Args:
        sessions_root (str): path for data of all lectures
        name (str): lecture name, will be subdir in sessions_root
        as_lists (bool): return lists or arrays
    Returns:
        tuple: ids and scores as arrays or as lists if as_lists
    """
    session_path = get_latest_session_path(sessions_root, name)
    try:
        ids = np.load(os.path.join(session_path, "ids.npy"), allow_pickle=True)
        scores = np.load(os.path.join(session_path, "scores.npy"), allow_pickle=True)
        if as_lists:
            ids = [list(person) for person in ids]
            scores = [[list(emotion) for emotion in person] for person in scores]
        return ids, scores
    except FileNotFoundError:
        return [], []


def last_session_difference(sessions_root, name):
    """Returns time since last session of name started.

    Args:
        sessions_root (str): path for data of all lectures
        name (str): lecture name

    Returns:
        float: time in minutes
    """
    if not get_latest_session_path(sessions_root, name):
        return np.inf
    now = datetime.now()
    old_date = get_latest_session_path(sessions_root, name).split(os.sep)[-1]
    old_date = datetime.strptime(old_date, '%Y%m%d%H%M')
    time_diff = (now - old_date).total_seconds() / 60
    return time_diff


def get_old_lecture_names(sessions_root):
    """Get list of all names of lectures in log_dir.

    Args:
        sessions_root (str): path for data of all lectures

    Returns:
        list: all lecture names
    """
    if not os.path.isdir(sessions_root):
        os.makedirs(sessions_root)
    return os.listdir(sessions_root)


if __name__ == "__main__":
    sessions_root = yaml.safe_load(open("config.yml"))["logs"]
    print(get_old_lecture_names(sessions_root))
    # os.makedirs(get_current_session_path(sessions_root, "test"))
    #load_last_session(sessions_root, "Test", True)
    #print(get_sorted_session_paths(sessions_root, "test"))
    # a = np.array([np.arange(0, 20), np.arange(0, 20)])
    # print(sparsify(a, 0, 0.5))
    pass
