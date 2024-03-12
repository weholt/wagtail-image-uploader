import json
import os


class JsonPreProcessor:
    """
    Looks for a JSON file using the filename+.json pattern
    and adds any such data to the metadata for that file.
    """

    def process(self, filename: str, metadata: dict) -> tuple[str, dict]:
        if os.path.exists(filename + ".json"):
            with open(filename + ".json") as f:
                metadata.update(**json.load(f))
        return (filename, metadata)
