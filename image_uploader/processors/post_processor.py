from wagtail.models import Collection


class AssignTitleFromMetadataPostProcessor:
    def process(self, image, metadata):
        if "title" in metadata:
            image.title = metadata.get("title") or image.title
        return (image, metadata)


class AssignTagsFromMetadataPostProcessor:
    def process(self, image, metadata):
        print("metadata", metadata)
        if "tags" in metadata:
            for tag in metadata.getlist("tags", []):
                image.tags.add(tag)
        return (image, metadata)


class AssignCollectionFromMetadataPostProcessor:
    def process(self, image, metadata):
        if "collections" in metadata:
            collections = metadata.get("collections").split("/")
            if collections:
                root_coll = Collection.get_first_root_node()
                for collection in collections:
                    children = [c for c in root_coll.get_children()]
                    if collection not in [c.name for c in children]:
                        root_coll = root_coll.add_child(name=collection)
                    else:
                        root_coll = [c for c in children if c.name == collection][0]

                image.collection = root_coll
        return (image, metadata)
