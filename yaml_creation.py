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
    zip_file_name = "D:/exporty12.zip"
    print("Creating archive: {:s}".format(zip_file_name))
    with zipfile.ZipFile(zip_file_name, mode="w") as zf:
        for r in recs:
            a = r.metadata["description"]
            d = r.metadata["identifier"][1]
            y = d.replace("/", "_")
            y = y.replace(".", "_")
            e = "\nidentifier: "
            var3 = e + d
            a = [s[1:] for s in a]
            a = [w.replace('@', '') for w in a]
            a = [w.replace('DA609: npr-1(ad609)X.', 'DA609 npr1(ad609)X.') for w in a]
            a = [w.replace('AX994: daf-22(m130)II; npr-1(ad609)X.', 'AX994 daf22(m130)II npr1(ad609)X.') for w in a]
            a = [w.replace('N2: lab reference strain.', 'N2 lab reference strain.') for w in a]
            a = [w.replace('AX994: daf-22(m130)II.', 'AX994 daf22(m130)II.') for w in a]
            a = [w.replace('OMG2: mIs12[myo-2p::GFP]II; npr-1(ad609)X. OMG19: rmIs349[myo3p::RFP]; npr-1(ad609)X.', 'OMG2 mIs12[myo2pGFP]II npr1(ad609)X. OMG19 rmIs349[myo3pRFP] npr1(ad609)X.') for w in a]
            a = [w.replace('OMG10: mIs12[myo-2p::GFP]II. OMG24: rmIs349[myo3p::RFP].', 'OMG10 mIs12[myo2pGFP]II. OMG24 rmIs349[myo3pRFP].') for w in a]
            a = [w.replace('\n\t', '\n') for w in a]
            a = [w.replace('\n\n', '\n') for w in a]
            a = [w.replace('\t', '  ') for w in a]
            b = a[0]
            g = b.split('\n', 1)[1]
            c = var3 + g
            img_name = "yamlfile_{}.yaml".format(y)
            print("  Writing image {:s} in the archive".format(img_name))
            zf.writestr(img_name, c)


if __name__ == "__main__":
    print("Python {:s} on {:s}\n".format(sys.version, sys.platform))
    main()
    print("Done.")
