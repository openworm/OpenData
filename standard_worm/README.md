## Standard Worm

### Background

This year, 2019, researchers finally completed the whole animal connectome of both *C. elegans* sexes. This will improve modelling of the nervous system whilst more detailed neuronal architecture may increase our understanding of the function of neurons within circuits. However, whilst the connectivity was mapped, no atlas of neuronal 3D coordinates currently exists. Previous attempts to build a 3D atlas have successfully segmented, identified and mapped 357/558 nuclei in the L1 stage. Using DAPI and RFP stained confocal Z stacks, this project attempted to apply the principles set out in Long et al. to produce a reference atlas of the 3D neuronal coordinates to which *C. elegans* phenotypes could be quickly and easily compared. Key steps include: straightening worms, marking nuclei centroids, aligning the z stacks and transforming the coordinate space. With advent of NeuroPal, a multicolour transgene able to resolve unique neuron identities, the creation of a more robust atlas should become easier. 

### Methods

#### 1. Imaging

Specimens were one day old *C. elegans*. Using a DAPI stain, which attaches to AT rich regions of DNA, nuclei were visualised and the worm captured as a confocal stack. 

#### 2. Visualisation

Individual stacks were visualised in Fiji (Fiji Is Just ImageJ). Stacks were imported through *File -> Import -> Image Sequence* and then the first image of the stack was selected. Settings were left on default. 

![](/figures/Figure_importstack.png)

#### 3. Straightening
  
Although each stack contained only a single worm these worms were often in curved or random orientations making comparison between worms harder. To make identification of neurons and transformation easier the worms were first straightened using Fiji’s Straighten option. 

Once the stack was loaded, we scrolled through the stack until a central slice was chosen which showed the width and length of the worm’s body clearly. If no such slice exists the contrast can be adjusted using *Image -> Adjust -> Brightness/Contrast*. To reset the Brightness/Contrast settings to the original press *Auto*. 

Once the worm body is visible select the polygon symbol on the Fiji tool panel and draw along the length of the worm following its curves by creating sections of straight lines. Connect the final point to the first.

![](/figures/Figure_polygonspline.png)

To create a line rather than polygon: *Edit -> Selection -> Area to Line*. To create a smoother centre line: *Edit -> Selection ->  Fit Spline*. 

You now have a spline mimicking the worms centre. Fiji’s Straightening tool uses this to perform straightening via spline interpolation. The Straighten tool creates another finely spaced spline (1 pixel width) from your spline (ROI). You are asked to assign a width to the spline (ROI) you drew, generally enough to cover the width of the *C. elegans*. Then for each small spline segment it interpolates, using a line perpendicular to that segment which is the width of the original ROI and is centred on the spline, from the original image to the final result. This creates a straightened worm. 

![](/figures/Figure_straightenedworm.png)

#### 4. Marking Neurons

Nuclei were marked manually as the centroid of a spot of DAPI fluorescence. To do this each section of the worm was considered in turn and spots which were the brightest throughout the stack for the same xy coordinates were considered the centroid. Only somatic/neuronal nuclei were marked. Nuclei within the gonad and embryonic region were left unmarked as these would not remain stable between worms. For example, everything in blue would be left unmarked in the figure below.

![](/figures/Figure_gonalregion.png)

To accomplish the marking of neurons, we used the multipoint selection and zoomed in on each section. If neurons were difficult to visualise the contrast of the image could again be adjusted and reset as before: *Image -> Adjust -> Brightness/Contrast*

![](/figures/Figure_markingcentroid.png)

This eventually led to a stack of points (ROIs) representing the centre of each somatic/neuronal nuclei.  

![](/figures/Figure_centroidstack.png)

The next step is to save these points for further use. Pressing *Ctrl + M* (or alternatively *Analyse -> Measure*) allows you to save each yellow point’s x, y, z coordinates to a csv, alongside other information such as Area, Min and Max etc. To load the ROIs at a later date onto the image stack, they must also be saved as a .roi file through *File -> Save As -> Selection*. To load the .roi file at any time: first import the image stack (*File -> Import -> Image Sequence*, select the first image in the sequence), then load the .roi file through the ROI manager.  *Analyse -> Tools -> ROI manager*. Once the box appears select *More*, then *Open* and then select the .roi file which you want to load. 

![](/figures/Figure_loadcentroidstack.png)

#### 5. Transformation to the same coordinate space

However some worms may be bigger than others or in a different coordinate space. To solve this problem to subsequently compare the ROIs selected in each worm to decide which are stable and which may be unstable. To do this we used a plugin called BigWarp which uses an affine transform to transform one worm into the space of another. An affine transform preserves points, straight lines and planes and keeps parallel lines parallel. 

BigWarp cannot deal with stacks so we define the coordinate space using two corresponding slices. Currently, we do not know which slice corresponds to another slice in a corresponding stack. For the sake of testing the script, I compared slice 13 of one RFP stack which I designated the reference to slice 13 of all other DAPI stacks. 
   
Open the corresponding slices from each image through *File -> Open* and then open them both in BigWarp: *Plugins -> BigDataViewer -> BigWarp*. Specify which image will be your target/reference image and which will be your moving image (i.e. the image you transform). With both images on the screen, click on the moving image to make it active, press *F8* and select *Affine* in the pop up window then close the pop up image. Press the space bar to enter landmark mode.

![](/figures/Figure_bigwarp.png)

Select a point on the moving image and then select the corresponding point on the target image. Ensure that you are considering dorso-ventral and anterior-posterior orientation. Worms are not necessarily imaged in the same orientation. The excretory pore is a good marker for identifying dorso-ventral orientation. These are your landmark points. Continue with this until all your landmark points are selected. 

![](/figures/Figure_bigwarplandmarks.png)

Save the landmark file as a .csv file: *File -> Export landmarks*

Close all windows except for the orignal Fiji Toolbar. Press the [ key on your keyboard to open up a script interpreter

![](/figures/Figure_scriptinterpreter.png)

Open excel and save a blank worksheet as a .csv file.

Within the space under the *New_ tab* copy and paste this [script](https://raw.githubusercontent.com/openworm/OpenData/master/standard_worm/bigwarpstacktransform_credit_johnbogovicj.groovy). Set *Language->groovy*.  Press Run and fill in the boxes in the pop up window. 

![](/figures/Figure_runscript.png)

Under landmark file, select the .csv file which you used to store the landmark coordinates from BigWarp. Create a copy of the .csv file you earlier created from the ROI (yellow dots) xyz locations for the moving image. Delete all columns other than X, Y and Slice and delete the header row. Use this newly formatted file for input points. For output points select the blank .csv file that you just created. Press OK.

Open the previously blank .csv file. This should now have 3 columns. The first corresponding to the transformed X coordinates of your ROIs, the second corresponding to the transformed Y coordinates of your ROI and the third a column of zeros. Replace the column of zeros with the Slice column from your original ROI file.   

These are your transformed worm coordinates which can then be plotted using this script. 

However, there are major flaws with this approach. Worms do not lie flat along the Z plane and so will need to be straightened along the Z axis. Current suggestions include identifying the four landmark points as the first visualisation of the head/tail and last visualisation of the  head/tail through the image stack and applying a transform. Another issue is the reliability of centroid marking. This was done manually and may not lead to the correct centroid identification. The key issue, however, is that there no easy/obvious fiducial marker was identified to anchor worm stacks to each other. Currently, alignment is heavily reliant on being able to identify patterns of nuclei shared between worms.

Possible Fiducial Markers discussed for finding corresponding slices between stacks were:

1. Pharynx/other internal structures: unlikely to be useful in this as not fixed.
2. Vulva/Excretory Pore: may be more useful but not visible right now in current images (excretory pore is visible).
3. Discussed the use of myo-3:GFP as in [Myers paper](https://www.nature.com/articles/nmeth.1366.pdf). Peter Sun, in Scott Emmons Lab, has created images with different fluorescence identifying different types of cells. Scott raised the point that the inside of the worm will be more squishy than outside. 
4. Right now looking along the lines of being able to identify similar patterns in nuclei to align stacks: to aid in this future images will reduce the number of nuclei by switching from DAPI to less sensitive RFP.
5. No start or end point of worm stack/slices per stack seem to be more different than would be expected. This is an issue for identifying an accurate cuticle and an accurate cuticle might be a nice fiducial marker.

