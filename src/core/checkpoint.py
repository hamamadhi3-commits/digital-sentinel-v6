import json
import os

class CheckpointManager:

    def __init__(self, filename="checkpoint.json"):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({"completed": []}, f)

    def load(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except:
            return None

    def update_completed(self, target):
        data = self.load()
        data["completed"].append(target)
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)
