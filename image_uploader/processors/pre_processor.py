class UploadAbortedException(Exception):
    "Exception raised by a pre-processor to stop file from being uploaded."

    def __init__(self, pre_processor, msg):
        super().__init__()
        self.msg = msg
        self.pre_processor = pre_processor

    def __str__(self) -> str:
        return f"Upload aborted by pre-processor {self.pre_processor.__class__.__name__}: {self.msg}"


class DummyPreProcessor:
    "Just an example pre-processor manipulating the metadata before the file is being uploaded."

    def process(self, filename, metadata):
        print("Dummy pre-processor", filename, metadata)
        metadata["dummy_was_here"] = True
        return (filename, metadata)


class AbortPreProcessor:
    "This is only to test the pre-processor."

    def process(self, filename, metadata):
        raise UploadAbortedException(self, "The thing that should not be")
