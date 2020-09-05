class PartInfo(object):
    uid = None
    name = None
    description = None
    location = None
    image_url = None

    def __init__(self, uid=None, name=None, description=None, 
                 location=None, image_url=None):
        self.uid = uid
        self.name = name
        self.description = description
        self.location = location
        self.image_url = image_url
