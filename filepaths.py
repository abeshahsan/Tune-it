import os


class Filepaths:
    __MAIN_WINDOW = 'ui_files/main-window.ui'

    @staticmethod
    def MAIN_WINDOW():
        return os.path.abspath(Filepaths.__MAIN_WINDOW)



if __name__ == '__main__':
    print(Filepaths.MAIN_WINDOW())
