from typing import Protocol, Self, TypeVar

from django.http import QueryDict
from wagtail.models import Collection

Image = TypeVar("Image")


class PostProcessor(Protocol):
    def __init__(self, image: Image, metadata: QueryDict) -> Self:
        ...

    def process(self, *args, **kwargs) -> bool | None:
        """
        Return true if actions have been taken.
        """


class PostProcessorBase:
    "A base class for post-processors with a few helper methods."

    def __init__(self, image: Image, metadata: QueryDict) -> Self:
        self.image = image
        self.metadata = metadata
        self.actions: list[str] = []

    def process(self, *args, **kwargs) -> bool | None:
        return False

    def result(self) -> tuple[Image, QueryDict, list[str]]:
        return (self.image, self.metadata, self.actions)


class AssignTitleFromMetadataPostProcessor(PostProcessorBase):
    def process(self, *args, **kwargs):
        if "title" in self.metadata:
            self.image.title = self.metadata.get("title") or self.image.title
            self.actions.append("Added title")


class AssignTagsFromMetadataPostProcessor(PostProcessorBase):
    def process(self, *args, **kwargs):
        if "tags" in self.metadata:
            for tag in self.metadata.getlist("tags", []):
                self.image.tags.add(tag)
                self.actions.append("Added tags")


class AssignCollectionFromMetadataPostProcessor(PostProcessorBase):
    def process(self, *args, **kwargs):
        if "collections" in self.metadata:
            collections = self.metadata.get("collections").split("/")
            if collections:
                root_coll = Collection.get_first_root_node()
                for collection in collections:
                    children = [c for c in root_coll.get_children()]
                    if collection not in [c.name for c in children]:
                        root_coll = root_coll.add_child(name=collection)
                    else:
                        root_coll = [c for c in children if c.name == collection][0]

                self.image.collection = root_coll
                self.actions.append(f"Assigned collection {root_coll}")
