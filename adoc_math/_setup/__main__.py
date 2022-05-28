from . import a_install, b_link


def main():
    i = a_install.Install()
    i.run()
    l = b_link.Link()
    l.run()


if __name__ == "__main__":
    main()
