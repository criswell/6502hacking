import sys
import importlib

from invoke import task
from invoke.tasks import call
from pathlib import Path

# Find the directories with workable invoke task files
sub_projects = [
    x for x in list(Path('.').glob('**/tasks.py')) if len(x.parts) > 1
]


def _validate_paths(paths):
    """
    Will validate a list of paths by comparing against the known project paths.
    If any element of the list of paths is invalid, will exit with error.

    Parameters:
        paths: A list of paths to check
    """
    # We do some dumb assumptions here on purpose to limit how this can be run
    # We want it to only run on paths we already know about
    valid_paths = [x.parts[0] for x in sub_projects]
    invalid = []
    [invalid.append(x) for x in paths if x not in valid_paths]

    if len(invalid) > 0:
        print("\nThe following paths were invalid:")
        [print(f"\t* {i}") for i in invalid]
        sys.exit(1)


def _run(c, file_path, method, fail_on_missing=False):
    """
    Will open up a python file and run a method in it, passing ``c`` as the
    only argument. This is how we chainload the runners.

    Parameters:
        c: the argument to pass
        file_path: the file path of the python file
        method: the method name to call
        fail_on_missing: whether or not a missing method should be a failure
    """
    spec = importlib.util.spec_from_file_location("runner", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        m = getattr(module, method)
    except AttributeError:
        print(f"{file_path} has no {method}() method")
        if fail_on_missing:
            sys.exit(1)
        return
    else:
        m(c)


def exec_task(c, path, method):
    """
    Abstracted task executor.

    Parameters:
        c: This is the argument to pass. It should be the invoke context
        path: This is the path as passed by user or None
        method: This is the method to call in the task runner
    """
    c.config['run']['echo'] = True
    if path:
        path = path.split(',')
        _validate_paths(path)
        for p in path:
            file_path = f"{p}/tasks.py"
            c.config['work_dir'] = p
            _run(c, file_path, method)
    else:
        for p in sub_projects:
            file_path = "/".join(p.parts)
            c.config['work_dir'] = "/".join(p.parts[0:-1])
            _run(c, file_path, method)


@task(optional=['path'])
def clean(c, path=None) -> None:
    """
    Clean a project or projects.

    Parameters:
        path: Can be a path to a project to clean, or a list of paths. If
              ``path`` is absent, all projects ``clean`` will be run.
    """
    exec_task(c, path, "clean")


@task(optional=['path'])
def build(c, path=None) -> None:
    """
    Build a project or projects.

    Parameters:
        path: Can be a path to a project to build, or a list of paths. If
              ``path`` is absent, all projects ``build`` will be run.
    """
    # We don't use the pre invoke option because we want to pass path and that
    # currently isn't possible in invoke
    clean(c, path)
    exec_task(c, path, "build")


@task(optional=['path'])
def test(c, path=None) -> None:
    """
    Test a project or projects.

    Parameters:
        path: Can be a path to a project to test, or a list of paths. If
              ``path`` is absent, all projects ``test`` will be run.
    """
    build(c, path)
    exec_task(c, path, "test")
