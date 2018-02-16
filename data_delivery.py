import os
import random

class DataSource:
    def _mkdir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def _add_delivery(self, key):
        def _part():
            file_count = 0
            while True:
                count = 0
                buffer = []
                while count < 100:
                    l = (yield).strip()
                    if l != "_flush":
                        buffer.append(l)
                        count += 1
                    else:
                        break

                filepath = os.path.join(self.path,
                                        "key={}".format(key),
                                        "{}.txt".format(file_count))
                file_count += 1
                with open(filepath, "w") as fid:
                    fid.write("\n".join(buffer) + "\n")

        m = _part()
        m.send(None)
        setattr(self, "_to_{}".format(key), m)

    def __init__(self, path, keys=[]):
        self.path = path
        self.keys = keys

        self._mkdir(path)
        for key in keys:
            self._mkdir(os.path.join(path, "key={}".format(key)))
            self._add_delivery(key)

    def gen_data(self, dataname, num):
        datapath = os.path.join(self.path, dataname)
        self.datapath = datapath

        with open(datapath, "w") as fid:
            for i in range(num):
                fid.write(random.choice(self.keys) + "\n")

    def delivery(self):
        with open(self.datapath, "r") as fid:
            for line in iter(fid.readline, ""):
                mame = line.strip()
                f = getattr(self, "_to_{}".format(mame))
                f.send(mame)

        for key in self.keys:
            f = getattr(self, "_to_{}".format(key))
            f.send("_flush")


if __name__ == "__main__":
    ds = DataSource(path="dd_result",
                    keys="abcdefghijklmnopqrstuvwxyz")
    ds.gen_data("data.txt", 100000)
    ds.delivery()

# for mame in {a..z}; do egrep $mame data.txt | wc -l && wc -l key\=$mame/* | tail -n 1; done
