"""Windows compatibility shim for fcntl.flock."""

import os
import sys

LOCK_SH = 1
LOCK_EX = 2
LOCK_NB = 4
LOCK_UN = 8

try:
    import msvcrt

    def flock(fd, operation):
        try:
            fileno = fd.fileno() if hasattr(fd, "fileno") else int(fd)
        except Exception:
            return

        # msvcrt locking operates on byte ranges from the current file position
        # For compatibility with fcntl advisory locks, we handle LOCK_UN / LOCK_EX / LOCK_NB
        try:
            curr_pos = os.lseek(fileno, 0, os.SEEK_CUR)
            os.lseek(fileno, 0, os.SEEK_SET)
            if operation & LOCK_UN:
                try:
                    msvcrt.locking(fileno, msvcrt.LK_UNLCK, 1)
                except OSError:
                    pass
            elif operation & LOCK_NB:
                try:
                    msvcrt.locking(fileno, msvcrt.LK_NBLCK, 1)
                except OSError:
                    raise BlockingIOError(11, "Resource temporarily unavailable")
            else:
                try:
                    msvcrt.locking(fileno, msvcrt.LK_LOCK, 1)
                except OSError:
                    pass
            os.lseek(fileno, curr_pos, os.SEEK_SET)
        except Exception:
            pass

except ImportError:
    def flock(fd, operation):
        pass
