import os


class Filepaths:
    __MAIN_WINDOW = 'ui_files/main-window.ui'
    __MAIN_WINDOW_V2 = 'ui_files/main-window-v2.ui'

    @staticmethod
    def MAIN_WINDOW():
        return os.path.abspath(Filepaths.__MAIN_WINDOW)
    
    @staticmethod
    def MAIN_WINDOW_V2():
        return os.path.abspath(Filepaths.__MAIN_WINDOW_V2)



if __name__ == '__main__':
    print(Filepaths.MAIN_WINDOW())
