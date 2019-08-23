## Calcium Imaging

### Background

Having uploaded movement metadata into PyOpenWorm and developed a proof of principle for conforming to the FAIR principles, the next step was to apply this to other data sources. Calcium imaging of neurons is a key tool for understanding neuronal activity. On electrical activation of a neuron, calcium levels can rise up to 10-100x their 50-100nM baseline levels. By linking calcium to chemical or genetically encoded fluorescent indicators and imaging the change in fluorescence we are able to monitor neuronal activation. Recently imaging advances have meant it is now possible to record transient intracellular calcium levels at a single cell resolution in the head of a freely moving *C. elegans*. This will make important advances in linking neuronal activity to movement data. The primary aim of OpenWorm is to create a model of the *C. elegans* nervous system from which we are able to predict behaviour. Having access to data which empirically links neuronal activation and movement will provide invaluable insight for both model creation and validation.

### Methods

Having created categories for movement metadata which conform to the FAIR principles, extending these categories makes them suitable for increasing accessibility of metadata concerning simultaneous neuronal and movement experiments. Unlike movement data sources, accessible in Zenodo, this information is mostly collected from individual research groups and is not yet collated into one source. In addition, as simultaneous tracking of movement and neuronal activity is a relatively new technique, it is necessary to supplement neuronal activity collected via calcium imaging with data from sedated worms. Once the data sources had been collated, I followed the same steps as before for the movement metadata. One, create categories to conform to the FAIR principles; Two, harvest metadata; Three, standardise the metadata as required; Four, upload to OpenWorm; Five, create unit tests to check incorporation; Six, extend metadata as required.     

#### 1. Gathering Data sources

OSF, like Zenodo, provides a platform for data sharing and includes key datasets concerning neuronal activity in C. elegans. I decided to split datasets into two divisions: Dynamical - calcium imaging with the head free to move and Fixed - where the worms are sedated.

Key non-dynamical/fixed data sources include:

- Data collated by [Manuel Zimmer](https://osf.io/a64uz/)

Key dynamical data sources include:

- Data collated by [Andrew Leifer](https://www.pnas.org/content/113/8/E1074)

Whilst these sources are currently sufficient to start planning integration categories which conform to the FAIR principles, ultimately more sources of data, especially dynamical, will be required. Using [Octoparse](https://www.octoparse.com/), web scraping of publications citing the Leifer dataset was carried out but was largely [unsuccessful](Citing%20doi.org_10.1073_pnas1507110112%20and%20include%20_elegans_.xlsx) at returning new datasets of interest. 

#### 2. Establishing FAIR categories

To integrate dynamical neuronal activity, an extension to the FAIR categories for movement metadata was decided as shown in [Document 2](CalciumImagingMetadataCategories.xlsx). These categories will need to be made more robust by evaluating more publications. 

#### Next steps: 

1. Gather more data sources and collate in a central location
2. Increase the robustness of the FAIR categories for integration into PyOpenWorm (possibly extend WCON documentation too)
3. Harvest metadata (possibly via paper scraping from key words)
4. Write classes and integrate
5. Write tests for integration 
