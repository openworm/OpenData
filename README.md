# OpenData
Repo for Google Summer of Code Open Data Project 2019.

Full documentation can be found [here](https://docs.google.com/document/d/17awS_bMScEyuUEsp_qPCEQG0esEeP5r0JWIU0xgLfJU/edit?usp=sharing)

# Introduction

OpenWorm is an attempt to build the first biophysical simulation of the model organism C. elegans. C. elegans are an important model organism in biological research and a large amount of data has been generated surrounding them at a behavioural, physiological, neuronal and molecular level. As the OpenWorm project reaches critical milestones, it is increasingly important to be able to validate simulations by incorporating all available data. However, the publication of biological data is often weakly structured and has no standardised format making assimilation challenging. To validate existing simulations and enter the next phase of development will require a significant increase and improvement of the amount of data available.

A key improvement required will be to store data in a way that is most useful for future use. Developed in 2016, the FAIR principles set out a framework for addressing this goal and are already being followed by other major data collators. The FAIR principles emphasise the importance of metadata; information that provides context to the main research data being published. Metadata can range from the protocol and conditions used to generate research data to the version of the data being published and how this fits in with complementary publications. The availability of good metadata increases the reusability of research generated data and can give insight into differences between experimental results. The framework emphasises: Findability, especially with an emphasis on machines being able to find and use the data; Accessibility, involving licence checks and levels of authorisation; Interoperability, ensuring that data fits in with other data sources by using the same format, vocabulary and linking to similar work; and Reusability, ensuring provenance, usage rights and protocols are clearly described to be most useful for future work.  

This Google Summer of Code project thus has two main aims. One: reformat existing data in line with the FAIR principles to make it more accessible for the OpenWorm community and for biological researchers as a whole. Two: increase the amount of data available by extracting features from already existing literature and data sources for easier access. To accomplish this I have focussed on 3 main sources of data: Worm movement videos, Calcium Imaging and Neuronal Coordinates.

## Movement

### Background

The integration of movement data is important for both building and validating the OpenWorm models of C. elegans. Neuromechanical models have so far given insight into how movement can be shaped by neuronal activity, helped classify mutants and have led to the identification of a minimum subset of features useful for quantifying behaviour. Classification and quantification allows for easier comparison of neural simulations to empirical movement data. A large dataset of worm movement videos has already been collated and stored alongside metadata in [Zenodo](https://zenodo.org/communities/open-worm-movement-database/?page=1&size=20), a data storage site which emphasises open science and metadata accessibility. An interactive website, [Open Worm Movement Database](http://movement.openworm.org/), exists to easily filter some metadata in the worm movement videos as required. Given these movement records are well maintained and appear to already contain easily accessible metadata it was decided that they would act as a good proof of principle for the two aims of the project.  

The first task was to establish how well the data currently conforms to the FAIR principles. In addition to the [2016 publication](https://www.nature.com/articles/sdata201618.pdf), additional guidance on conforming to the FAIR framework exists [here](https://www.go-fair.org/fair-principles/). Using this, existing metadata was grouped into categories and any missing metadata categories were flagged to be added at a later date.

Included already within OpenWorm is the codebase, [PyOpenWorm](https://github.com/openworm/PyOpenWorm). PyOpenWorm was designed specifically for the purpose of increasing searchability and accessibility of C. elegans research data. [Currently incorporated data](https://pyopenworm.readthedocs.io/en/latest/data_sources.html) is taken from WormBase, WormAtlas and personal communications with researchers in the C. elegans community. It can be divided into three categories: Neuronal Information, Muscle Cells and the Connectome. 

Once the movement data had been processed to ensure conformability with the FAIR framework the second task was to upload all data into PyOpenWorm in a format facilitating queriability by C. elegans researchers and model builders. 

### Methods

The integration of movement metadata into PyOpenWorm had six main phases as seen below.

![](/figures/Figure_%20FAIRPrinciples.jpg?raw=true)

First, following the [FAIR framework](https://www.go-fair.org/fair-principles/), a set of categories were determined. These categories were decided to ensure the recommendations of the FAIR principles were followed whilst keeping the data as easily accessible as possible. These were greatly informed by the guidance already set out in [WCON](https://github.com/openworm/tracker-commons/blob/master/WCON_format.md). Second, the metadata surrounding each movement record in [Zenodo](https://zenodo.org/communities/open-worm-movement-database/?page=1&size=20) was harvested whilst still in its current format. Third, the data harvested was changed to a standardised format, with missing categories added and set to “None” to ensure uniformity across records. Fourth, the standardised metadata could now be integrated into the PyOpenWorm codebase following the instructions in the [documentation](https://pyopenworm.readthedocs.io/en/latest/adding_data.html). Fifth, after integration unit tests are performed to check that data has been added completely and correctly. Sixth, any FAIR categories not filled by the existing metadata are filled through additional searches. 

#### 1. Establishing FAIR categories

Movement data and metadata is stored in Zenodo within the Community [“Open Worm Movement Database”](https://zenodo.org/communities/open-worm-movement-database). As of August 2019, within the community are 15000 records. Clicking on one of these records gives a link to both the data itself and the metadata associated.

![](/figures/Figure_Zenodorecord.png?raw=true)

[Document 1](movement/MovementMetadataCategories.xlsx) shows the categories decided to implement the FAIR principles for each record.  

#### 2. Harvesting Metadata

Zenodo already provides interoperability for all its records with the [Open Archives Initiatives](https://www.openarchives.org/pmh/), a protocol developed for metadata harvesting. Going back to the main Open Worm Movement Database Community page and clicking the link “OAI-PMH Interface” under “Harvesting API” on the right hand side allows us to access the metadata in the OAI format.

![](figures/Figure_Zenodorecordslist.png?raw=true)

In this [format](https://zenodo.org/oai2d?verb=ListRecords&set=user-open-worm-movement-database&metadataPrefix=oai_dc) we can use a premade OAI-PMH Metadata harvester, to cycle through each of the links using the token at the end of each page and harvest the metadata surrounding each record. I chose to use the prebuilt python package, [Sickle](https://pypi.org/project/Sickle/). 

Using Sickle we are able to access and extract data as needed from the “Open Worm Movement Database” Community.

```
import sickle
from sickle import Sickle
from sickle.iterator import OAIResponseIterator

#access Zenodo
sickle = Sickle("https://zenodo.org/oai2d")

#create object which contains all Zenodo records within the community "Open Worm Movement Database"
records = sickle.ListRecords(set='user-open-worm-movement-database', metadataPrefix='oai_dc')

```
Each record in records is in .xml format with the headers: OAI Identifier, Datestamp, setSpec, Author or Creator, Date, Description, Resource Identifier, Relation, Rights Management, Title, Resource Type.

![](figures/Figure_Zenodorecordxml.png)


