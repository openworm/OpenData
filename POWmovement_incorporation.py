import sickle
from sickle import Sickle
from sickle.iterator import OAIResponseIterator

sickle = Sickle("https://zenodo.org/oai2d")
recs = sickle.ListRecords(set='user-open-worm-movement-database', metadataPrefix='oai_dc')

import yaml
import zipfile

zip_file = zipfile.ZipFile("D:/exporty13.zip")
files = zip_file.namelist()
lenfiles = len(files)
#for now just one record
for i in range(lenfiles):
    with zip_file.open(files[i]) as yamlfile:
        yamldict = yaml.safe_load(yamlfile)
        doi = yamldict["identifier"]
        splitid = doi.split(".")
        wantedsplit = splitid[-1]
        xmlrec = sickle.GetRecord(identifier='oai:zenodo.org:{}'.format(wantedsplit), metadataPrefix='oai_dc')
        #to check this is working print identifier for yamldict and xmlrec
        print(xmlrec.metadata["identifier"])
        print(yamldict["identifier"])


from PyOpenWorm.dataObject import DataObject
from PyOpenWorm.context import Context

#what should namespace be? upload_movementmetadata(yamldict, xmlrec)?
def upload_movemementmetadata(namespace):
    # Make a new context. Takes care of specifying the `conf` argument and enables
    # validation for statements
    #ctx = namespace.new_context("http://example.org/example_context")
    ctx = namespace.Context(ident='http://example.org/{}'.format(doi))

    # ctx(DataObject)(key='a')
    # ctx(DataObject)(key='b')
    w = ctx(Worm)("C. elegans")
    md = ctx(Metadata)(key={}.format(doi))  # key = doi here
    u = ctx(Usage)(rights = xmlrec.metadata["rights"])
    p = ctx(Provenance)(citation = None,
                        complementarydata = None,
                        processing = None,
                        previouspublications = None,
                        previewlink = yamldict["preview link"])
    c = ctx(Collection)(lab=yamldict["lab"],
                        collector=yamldict["who"],
                        timestamp=yamldict["timestamp"],
                        humidity=yamldict["humidity"],
                        arena=yamldict["arena"],
                        food=yamldict["food"],
                        media=yamldict["media"],
                        habituation = yamldict["habituation"],
                        protocol=yamldict["protocol"],  # will need to add more detail to this
                        scope= None,  # need to get this - maybe abstract
                        limitations= None,  # need to find this
                        interpolation=None,
                        arena = yamldict["arena"])  # need to find this
    b = ctx(BioDetails)(sex = yamldict["sex"],
                        stage = yamldict["stage"],
                        age = yamldict["age"],
                        strain = yamldict["strain"],
                        strain_descr = yamldict["strain_description"],
                        gene = yamldict["gene"],
                        chromosome = yamldict["chromosome"],
                        allele = yamldict["allele"],
                        proteins = yamldict["protein"],
                        daysofadulthood = yamldict["days_of_adulthood"],
                        worm_id = yamldict["worm_id"])

    s = ctx(Software)(name = yamldict["software"],
                      featureID = yamldict["featureID"],
                      version = yamldict["version"],
                      settings = yamldict["settings"],
                      time = yamldict["total time (s)"],
                      framespersecond = yamldict["frames per second"],
                      mmperpixel = yamldict["video micrometers per pixel"],
                      nosegskel = yamldict["number of segmented skeletons"],
                      base_name = yamldict["base_name"],
                      ventralside = yamldict["ventral_side"])
    md.subject(w)
    md.collection(c)
    md.usage(u)
    md.provenance(p)
    md.software(s)
    md.provenance(p)
    md.biodetails(b)

    # Add an import of DataObject's context, but see openworm/PyOpenWorm#374 -- may be
    # automated eventually
    ctx.add_import(DataObject.definition_context)

    # Link to the namespace context -- our statements will not be saved otherwise
    namespace.context.add_import(ctx)


