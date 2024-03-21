from image_uploader.client import UploadClient
from image_uploader.config import UploadClientConfiguration
from image_uploader.factory import pre_processors_from_strings

url = "http://localhost:8000/upload-image"
api_key = "U0n7bUrr1J98npj2SBo6XHmpsK5j8VlHZu3fO1FYpLIxsiWLo1SEwugRI4XjfAvbxUXMcx1khWvyf0shTAAu19OmMIyMAV74fvWexm7cCAv0rxZWuBdZrGxfShMtPfeh"
pre_processors_string = ["image_uploader.processors.pre_processor.JsonPreProcessor"]
config = UploadClientConfiguration(api_key=api_key, url=url, defaults={"collections": "default/folder"}, pre_processors=pre_processors_from_strings(pre_processors_string))
client = UploadClient.create_from_config(config, verbose=True)
client.upload_files(*["test.png"])
