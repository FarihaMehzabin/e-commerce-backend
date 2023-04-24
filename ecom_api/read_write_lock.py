import threading

class ReadWriteLock:
    def __init__(self):
        self._read_lock = threading.Lock()
        self._write_lock = threading.Lock()
        self._reader_count = 0

    def acquire_read(self):
        with self._read_lock:
            self._reader_count += 1
            if self._reader_count == 1:
                self._write_lock.acquire()

    def release_read(self):
        with self._read_lock:
            self._reader_count -= 1
            if self._reader_count == 0:
                self._write_lock.release()

    def acquire_write(self):
        self._write_lock.acquire()

    def release_write(self):
        self._write_lock.release()
