import sys
import matplotlib.pyplot as plt
import zipfile
import io

import sickle
from sickle import Sickle
from sickle.iterator import OAIResponseIterator

sickle = Sickle("https://zenodo.org/oai2d")
recs = sickle.ListRecords(set='user-open-worm-movement-database', metadataPrefix='oai_dc')

#basic idea compare the keys in yaml to the standardise list of keys that I want to include
#if they all match brilliant - proceed
#if they don't match
#find out which keys are missing in the yaml file compared to the standardised list
#append <missing_key> : nan


#taken from subclasses.py
standardised_list = ['allele', 'arena', 'base_name', 'chromosome', 'food', 'frames per second', 'gene', 'habituation', 'identifier', 'lab', 'media', 'number of segmented skeletons', 'preview link', 'protocol', 'sex', 'software', 'stage', 'strain', 'strain_description', 'timestamp', 'total time (s)', 'ventral_side', 'video micrometers per pixel', 'who', 'days_of_adulthood', 'worm_id']

def main():
    zip_file_name = "D:/exporty13.zip"
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
            included_standard_elements = sorted([element for element in standardised_list if (element in b)])
            unincluded_standard_elements = list(set(standardised_list).difference(included_standard_elements))
            for i in unincluded_standard_elements:
                addel = "\n{}".format(i) + " : nan"
                b = b + addel
            g = b.split('\n', 1)[1]
            c = var3 + g
            img_name = "yamlfile_{}.yaml".format(y)
            print("  Writing image {:s} in the archive".format(img_name))
            zf.writestr(img_name, c)

if __name__ == "__main__":
    print("Python {:s} on {:s}\n".format(sys.version, sys.platform))
    main()
    print("Done.")

