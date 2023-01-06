from classifier.api import check_if_nick
from gui.app import App

def main():
    app = App(check_if_nick)
    app.mainloop()

if __name__ == '__main__':
    main()