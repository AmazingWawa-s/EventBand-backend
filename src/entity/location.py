class Location():
    def __init__(self,id,name,capacity):
        self.id = id
        self.name = name
        self.description=""
        self.capacity = capacity
        self.available=["id","name","description","capacity"]
    def get(self,attr_list):
        return [getattr(self,attr) for attr in attr_list]

    def set(self,attr_dict):
        for attr,value in attr_dict.items():
            if attr[9:] not in self.available:
                raise ValueError("Not available from Location")
            elif attr[9:0] in self.available:
                setattr(self,attr[9:],value)
    