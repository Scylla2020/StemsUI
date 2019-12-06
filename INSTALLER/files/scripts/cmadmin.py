#Credit to user Noctis Skytower - https://stackoverflow.com/a/42787518/8739330

import ctypes
import enum
import subprocess
import sys
import os
import time

# Reference:
# msdn.microsoft.com/en-us/library/windows/desktop/bb762153(v=vs.85).aspx

cur_dir = os.getcwd()
bin_path = os.path.join(cur_dir,"ffmpeg-20191119-0321bde-win64-static","bin")

class SW(enum.IntEnum):
    HIDE = 0
    MAXIMIZE = 3
    MINIMIZE = 6
    RESTORE = 9
    SHOW = 5
    SHOWDEFAULT = 10
    SHOWMAXIMIZED = 3
    SHOWMINIMIZED = 2
    SHOWMINNOACTIVE = 7
    SHOWNA = 8
    SHOWNOACTIVATE = 4
    SHOWNORMAL = 1


class ERROR(enum.IntEnum):
    ZERO = 0
    FILE_NOT_FOUND = 2
    PATH_NOT_FOUND = 3
    BAD_FORMAT = 11
    ACCESS_DENIED = 5
    ASSOC_INCOMPLETE = 27
    DDE_BUSY = 30
    DDE_FAIL = 29
    DDE_TIMEOUT = 28
    DLL_NOT_FOUND = 32
    NO_ASSOC = 31
    OOM = 8
    SHARE = 26


def bootstrap():
    if ctypes.windll.shell32.IsUserAnAdmin():
        main()
        time.sleep(3)
    else:
       # noinspection SpellCheckingInspection
        hinstance = ctypes.windll.shell32.ShellExecuteW(
            None,
            'runas',
            sys.executable,
            subprocess.list2cmdline(sys.argv),
            None,
            SW.SHOWNORMAL
        )
        if hinstance <= 32:
            raise RuntimeError(ERROR(hinstance))


def main():
    os.system(f'python regedit.py +Path "{bin_path}"')
