from .._common import *


class Install:
    def run(s):
        run_cmd(
            cmd=Command("npm i -g mathjax@3"),
        )


def main():
    i = Install()
    i.run()


if __name__ == "__main__":
    main()
