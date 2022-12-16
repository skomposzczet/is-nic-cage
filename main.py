from gui.app import App

def stub(filaneme):
    return 'maybe it is Nic Cage, maybe not'

def main():
    app = App(stub)
    app.mainloop()

if __name__ == '__main__':
    main()