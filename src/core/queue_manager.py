import queue
import threading
import time

class TaskQueue:

    def __init__(self, max_workers=20):
        self.tasks = queue.Queue()
        self.max_workers = max_workers
        self.threads = []

    def worker(self):
        while True:
            try:
                task = self.tasks.get(block=False)
            except queue.Empty:
                break

            try:
                task()
            except Exception as e:
                print(f"[ERROR] Task failed: {e}")

            self.tasks.task_done()

    def add_task(self, func):
        self.tasks.put(func)

    def wait_completion(self):
        for _ in range(self.max_workers):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            self.threads.append(t)

        self.tasks.join()
