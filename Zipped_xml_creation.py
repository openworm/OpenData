
import sys
import matplotlib.pyplot as plt
import zipfile
import io

import sickle
from sickle import Sickle
from sickle.iterator import OAIResponseIterator

sickle = Sickle("https://zenodo.org/oai2d")
recs = sickle.ListRecords(set='user-open-worm-movement-database', metadataPrefix='oai_dc')

def main():
    zip_file_name = "D:/exportxml.zip"
    print("Creating archive: {:s}".format(zip_file_name))
    with zipfile.ZipFile(zip_file_name, mode="w") as zf:
        for r in recs:
            d = r.metadata["identifier"][1]
            y = d.replace("/", "_")
            y = y.replace(".", "_")
            c = r.raw.encode("utf8")
            img_name = "yamlfile_{}.yaml".format(y)
            print("  Writing image {:s} in the archive".format(img_name))
            zf.writestr(img_name, c)


if __name__ == "__main__":
    print("Python {:s} on {:s}\n".format(sys.version, sys.platform))
    main()
    print("Done.")

