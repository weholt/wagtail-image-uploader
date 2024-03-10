class DummyPostProcessor:
    def process(self, image, metadata):
        print("Dummy post-processor", image, metadata)
        return (image, metadata)
