from .d_exceptions import *


def get_logger(file_name: str, level: int) -> logging.Logger:
    logger = logging.getLogger(file_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


logger = get_logger(__file__, LOGGING_LEVEL)


def run_cmd(
    cmd: Command,
    stdin=bytes(),
    raise_on_error=True,
) -> Tuple[StdOut, StdErr]:
    print(f"Running {cmd}...")
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        shell=True,
    )
    stdout, stderr = process.communicate(input=stdin)
    process.wait()
    if raise_on_error and process.returncode != 0:
        raise AdocMathException(stdout.decode() + stderr.decode())
    else:
        return StdOut(stdout.decode()), StdErr(stderr.decode())


def for_each_apply_method(
    ps: Iterable[Union[str, plib.Path]],  # path strs
    method: Callable[[plib.Path], None],
):
    """Calls a method with an argument of all of ps.
    If a p is a directory, it searches it recursively.
    The idea is that the method is bound to some object (such as set), and this function allows easy updating of that set over a tree of files.
    """
    for p_path_or_str in ps:
        p = plib.Path(p_path_or_str).resolve(strict=True)
        if p.is_dir():
            for_each_apply_method(
                ps=sorted(p.glob("*")),
                method=method,
            )
        elif p.is_file():
            method(p)
        else:
            raise AdocMathException(DEAD_CODE_MSG)


def log(*args):
    """Useful for debuggin :-P

    https://stackoverflow.com/a/2749857/4204961"""

    frame = inspect.currentframe()
    frame = inspect.getouterframes(frame)[1]
    string = inspect.getframeinfo(frame[0]).code_context[0].strip()  # type: ignore
    params = string[string.find("(") + 1 : -1].split(",")

    names = []
    for i in params:
        if i.find("=") != -1:
            names.append(i.split("=")[1].strip())

        else:
            names.append(i)

    for name, val in zip(names, args):
        logger.debug(f"\n    {name} =\n{' ' * 14}{pprint.pformat(val)}")


def join_with(
    it: Iterable[str],
    joiner: str,
) -> str:
    """Reverses the arguments of x.join(y)"""

    return joiner.join(it)
