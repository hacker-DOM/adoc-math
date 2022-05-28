from .._common import *


class Link:
    def run(s):
        run_cmd(cmd=Command("npm link mathjax@3"))


def main():
    l = Link()
    l.run()


if __name__ == "__main__":
    main()
