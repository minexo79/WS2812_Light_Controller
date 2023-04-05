import json 

class parseJson:
    def __init__(self) -> None:
        self.parsedata = None

    def parseToStructure(self, filename: str):
        self.parsedata = []

        fd = open(filename, 'r', encoding='utf-8')
        jd = json.load(fd)

        self.parsedata = []
        for data in jd:
            _time = data["time"]
            _light = [int(i, 16) for i in data["light"]]

            self.parsedata.append({
                "time": _time,
                "light": _light
            })