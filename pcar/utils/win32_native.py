# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

import atexit
import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
kernel32 = ctypes.windll.kernel32

KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_KEYUP   = 0x0002
TH32CS_SNAPPROCESS = 0x00000002
MAX_PATH = 260

ULONG_PTR = wintypes.WPARAM


class PROCESSENTRY32W(ctypes.Structure):
    _fields_ = [("dwSize", wintypes.DWORD),
                ("cntUsage", wintypes.DWORD),
                ("th32ProcessID", wintypes.DWORD),
                ("th32DefaultHeapID", ULONG_PTR),
                ("th32ModuleID", wintypes.DWORD),
                ("cntThreads", wintypes.DWORD),
                ("th32ParentProcessID", wintypes.DWORD),
                ("pcPriClassBase", wintypes.LONG),
                ("dwFlags", wintypes.DWORD),
                ("szExeFile", wintypes.WCHAR * MAX_PATH)]

 
gdi32.GetPixel.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
gdi32.GetPixel.restype  = ctypes.c_uint32
hdc = user32.GetDC(0)


# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def hold(hexScanCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexScanCode, KEYEVENTF_SCANCODE, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def release(hexScanCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexScanCode, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def press(hexScanCode):
    hold(hexScanCode)
    release(hexScanCode)


# ------------------------------------------------------------
# Mouse Helpers
# ------------------------------------------------------------

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long)]

def get_mouse_pos():
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

# ------------------------------------------------------------
# Pixel Reader
# ------------------------------------------------------------

def get_pixel(x, y):
    """Fast pixel read using WinAPI GetPixel.""" 
    color = gdi32.GetPixel(hdc, x, y) 

    r = color & 0xFF
    g = (color >> 8) & 0xFF
    b = (color >> 16) & 0xFF
    return (r, g, b)


def get_color(x, y):
    """Get color number at (x, y).""" 
    color = gdi32.GetPixel(hdc, x, y) 
    return color

# ------------------------------------------------------------
# Window Helpers
# ------------------------------------------------------------

def find_window(title: str):
    """Find window by exact title."""
    return user32.FindWindowW(None, title)

def find_window_partial(partial: str):
    """Find window by partial title."""
    hwnd_list = []

    def enum_proc(hwnd, lParam):
        text = ctypes.create_unicode_buffer(512)
        user32.GetWindowTextW(hwnd, text, 512)
        if partial.lower() in text.value.lower():
            hwnd_list.append(hwnd)
        return True

    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(EnumWindowsProc(enum_proc), 0)

    return hwnd_list[0] if hwnd_list else None

def get_window_rect(hwnd):
    """Return (left, top, right, bottom)."""
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    return rect.left, rect.top, rect.right, rect.bottom

def focus_window(hwnd):
    """Bring window to foreground."""
    user32.SetForegroundWindow(hwnd)

def find_hwnd_by_process_name(name):
    """Find the first top-level window handle owned by a process name."""
    process_ids = set()
    entry = PROCESSENTRY32W()
    entry.dwSize = ctypes.sizeof(PROCESSENTRY32W)
    snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)

    if snapshot == ctypes.c_void_p(-1).value:
        return None

    try:
        has_process = kernel32.Process32FirstW(snapshot, ctypes.byref(entry))
        while has_process:
            if entry.szExeFile.lower() == name.lower():
                process_ids.add(entry.th32ProcessID)
            has_process = kernel32.Process32NextW(snapshot, ctypes.byref(entry))
    finally:
        kernel32.CloseHandle(snapshot)

    if not process_ids:
        return None

    hwnd_list = []

    def enum_proc(hwnd, lParam):
        process_id = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
        if process_id.value in process_ids and user32.IsWindowVisible(hwnd):
            hwnd_list.append(hwnd)
            return False
        return True

    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(EnumWindowsProc(enum_proc), 0)

    return hwnd_list[0] if hwnd_list else None

def find_hwnd_by_pid(pid):
    hwnd_list = []

    def enum_proc(hwnd, lParam):
        process_id = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
        if process_id.value == pid and user32.IsWindowVisible(hwnd):
            hwnd_list.append(hwnd)
            return False
        return True

    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(EnumWindowsProc(enum_proc), 0)
    return hwnd_list[0] if hwnd_list else None

#------------------------------------------------------------
# Cleanup on exit
#------------------------------------------------------------
def cleanup():
    print("Cleaning up: releasing HDC")
    user32.ReleaseDC(0, hdc)

atexit.register(cleanup)
