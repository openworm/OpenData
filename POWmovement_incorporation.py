from PyOpenWorm.dataObject import DataObject
from PyOpenWorm.context import Context
from PyOpenWorm.worm import Worm
from PyOpenWorm.evidence import Evidence
import movementmetadata
from movementmetadata import MovementMetadata
from movementmetadata import Provenance, Usage, Collection, BioDetails, Software
import yaml
import zipfile
from urllib.request import urlopen
import io
from io import StringIO, BytesIO
import requests, zipfile, io
# r = requests.get(zip_file_url)
# z = zipfile.ZipFile(io.BytesIO(r.content))
# z.extractall()



# what should namespace be? upload_movementmetadata(yamldict, xmlrec)?
def pow_data(namespace):
    # Make a new context. Takes care of specifying the `conf` argument and enables
    # validation for statements
    # ctx = namespace.new_context("http://example.org/example_context")

    import sickle
    from sickle import Sickle
    from sickle.iterator import OAIResponseIterator

    sickle = Sickle("https://zenodo.org/oai2d")
    recs = sickle.ListRecords(set='user-open-worm-movement-database', metadataPrefix='oai_dc')
    r2 = requests.get("https://github.com/EST09/AccessibleData/raw/master/movementmetadata_yaml4.zip")
    zip_file = zipfile.ZipFile(io.BytesIO(r2.content))
    files = zip_file.namelist()
    lenfiles = len(files)
    for i in range(lenfiles):
        with zip_file.open(files[i]) as yamlfile:
            yamldict = yaml.safe_load(yamlfile)
            doi = yamldict["identifier"]
            splitid = doi.split(".")
            wantedsplit = splitid[-1]
            arena = yamldict["arena"]
            lab = yamldict["lab"]
            software = yamldict["software"]
            # xmlrec = sickle.GetRecord(identifier='oai:zenodo.org:{}'.format(wantedsplit), metadataPrefix='oai_dc')

            ctx = namespace.new_context('http://openworm.org/data/movement/{}'.format(doi))

            # ctx(DataObject)(key='a')
            # ctx(DataObject)(key='b')
            w = ctx(Worm)("C. elegans")
            md = ctx(MovementMetadata)(key=doi)  # key = doi here
            # u = ctx(Usage)(rights = xmlrec.metadata["rights"])
            p = ctx(Provenance)(key=doi,
                                citation=None,
                                complementarydata=None,
                                processing=None,
                                previouspublications=None,
                                previewlink=yamldict["preview link"])
            c = ctx(Collection)(key=doi,
                                lab_name=lab["name"] if "name" in lab else None,
                                lab_location=lab["location"] if "location" in lab else None,
                                collector=yamldict["who"],
                                timestamp=yamldict["timestamp"],
                                arena_style=arena["style"] if "style" in arena else None,
                                arena_size=arena["size"] if "size" in arena else None,
                                arena_orientation=arena["orientation"] if "orientation" in arena else None,
                                food=yamldict["food"],
                                media=yamldict["media"],
                                habituation=yamldict["habituation"],
                                protocol=yamldict["protocol"],  # will need to add more detail to this
                                scope=None,  # need to get this - maybe abstract
                                limitations=None,  # need to find this
                                interpolation=None)  # need to find this
            # humidity=yamldict["humidity"],?
            b = ctx(BioDetails)(key=doi,
                                sex=yamldict["sex"],
                                stage=yamldict["stage"],
                                strain=yamldict["strain"],
                                strain_descr=yamldict["strain_description"],
                                # gene = yamldict["gene"],
                                # chromosome = yamldict["chromosome"],
                                allele=yamldict["allele"],
                                daysofadulthood=yamldict["days_of_adulthood"],
                                worm_id=yamldict["worm_id"])

            for chr in yamldict['chromosome'].split(';'):
                b.chromosome(chr)
            for gen in yamldict['gene'].split(';'):
                b.gene(gen)
            # age = yamldict["age"],?
            # proteins = yamldict["protein"], ?
            s = ctx(Software)(key=doi,
                              software_name=software["name"] if "name" in software else None,
                              software_version=software["version"] if "version" in software else None,
                              software_featureID=software["featureID"] if "featureID" in software else None,
                              time=yamldict["total time (s)"],
                              framespersecond=yamldict["frames per second"],
                              mmperpixel=yamldict["video micrometers per pixel"],
                              nosegskel=yamldict["number of segmented skeletons"],
                              base_name=yamldict["base_name"],
                              ventralside=yamldict["ventral_side"])
            # featureID = yamldict["featureID"],?
            # version = yamldict["version"],
            # settings = yamldict["settings"],

            md.subject(w)
            md.collection(c)
            # md.usage(u)
            md.provenance(p)
            md.software(s)
            md.biodetails(b)

            # Add an import of DataObject's context, but see openworm/PyOpenWorm#374 -- may be
            # automated eventually
            ctx.add_import(Worm.definition_context)
            ctx.add_import(MovementMetadata.definition_context)
            # ctx.add_import(Usage.definition_context)
            ctx.add_import(Provenance.definition_context)
            ctx.add_import(Collection.definition_context)
            ctx.add_import(Software.definition_context)
            ctx.add_import(BioDetails.definition_context)

            # Link to the namespace context -- our statements will not be saved otherwise
            namespace.context.add_import(ctx)
