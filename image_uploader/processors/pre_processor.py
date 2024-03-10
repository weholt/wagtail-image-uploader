class DummyPreProcessor:
    def process(self, filename, metadata):
        print("Dummy pre-processor", filename, metadata)
        metadata["dummy_was_here"] = True
        return (filename, metadata)
