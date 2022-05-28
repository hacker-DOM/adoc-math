from .._common import *


class Link:
    def run(s):
        install_dir = plib.Path(__file__).parent.parent.parent
        with change_cwd(install_dir):
            run_cmd(cmd=Command("npm link mathjax@3"))


def main():
    l = Link()
    l.run()


if __name__ == "__main__":
    main()
