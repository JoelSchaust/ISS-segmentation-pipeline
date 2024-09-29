# Overwiew

This repository is intended as a supplement to the Master's thesis "Integrated Pipeline for Whole-Cell and Nuclear Segmentation in In-situ Sequencing Data". 

The thesis is directly linked to the project and focuses on the development of nucleus- and cell-segmentation models, which are intended to be used for cell and nucleus segmentation within the framework of the project.
> Ahmad S, Gribling-Burrer AS, Schaust J, Fischer SC, Ambil UB, Ankenbrand MJ, Smyth RP.
> *Visualizing the transcription and replication of influenza A viral RNAs in cells by multiple direct RNA padlock probing and in-situ sequencing (mudRapp-seq)*
> (in revision)

The official GitHub repository of the paper can be accessed at: [mudRapp-seq](https://github.com/BioMeDS/mudRapp-seq/tree/main).

# computational environments

To re-create the python environments with [`mamba`](https://github.com/mamba-org/mamba) run:

```bash
mamba env create -f envs/base_environment.yml 
mamba env create -f envs/cellpose_environment.yml 
mamba env create -f envs/devbio_napari_environment.yml 
```

Additional information about [devbio-napari](https://github.com/haesleinhuepf/devbio-napari) and [Cellpose](https://github.com/MouseLand/cellpose)

# Documentation

This repository contains data from 5 fields of view, which were used as a test dataset in the course of the thesis, as well as the environments and all scripts involved in the processing.

Some scripts are equipped with arguments that must be provided when calling them. The data for the fields of view are as follows:

- 6hpi fov15 s5
- 6hpi fov15 s3
- 5hpi fov13 s8
- 5hpi fov13 s7
- 4hpi fov11 s8

The cell and nucleus segmentation produce separate outputs. For an overview of all input and output data, as well as raw and normalized data, you can access it via [inspect_results.py](https://github.com/JoelSchaust/ISS-segmentation-pipeline/blob/main/code/inspect_results_thesis.py)

```bash
mamba activate base_environment.yml #the inspect_results.py can also be used with the devbio-napari.yml
python code/inspect_results_thesis.py --hpi 6 --fov 15 --s 5 # change the arguments in order to call different fovs
```

# Repository structure

The input images (after preprocessing) can be found in the [raw data folder](https://github.com/JoelSchaust/ISS-segmentation-pipeline/tree/main/data/raw). 
This folder contains the data for both [nucleus](https://github.com/JoelSchaust/ISS-segmentation-pipeline/tree/main/data/raw/input_images_nuc) and [cytoplasm](https://github.com/JoelSchaust/ISS-segmentation-pipeline/tree/main/data/raw/input_images_cyto) segmentation.

The segmentation process in both separate models – for nuclei and cytoplasmic segmentation – is divided into three main steps: First, the application of the model to the corresponding image data to identify the regions of interest. Next, postprocessing is performed to reduce small objects and close small holes in the segmentation. Finally, the remapping of labels is carried out according to the [ground truth](https://github.com/JoelSchaust/ISS-segmentation-pipeline/tree/main/data/processed/ground_truth_nuc) to ensure accurate evaluation and further analysis of the segmentation results.

To replicate the results, the following scripts must be run in sequence:

## Nucleus segmentation
- [Use custom model](https://github.com/JoelSchaust/ISS-segmentation-pipeline/tree/main/code/nuc_segmentation/nuc_use_custom_model.py)
```bash
mamba activate cellpose_environment.yml 
python code/nuc_use_custom_model.py --hpi 6 --fov 15 --s 5 # change the arguments in order to call different fovs
```
Output folder: [Nuclei output](https://github.com/JoelSchaust/ISS-segmentation-pipeline/tree/main/data/processed/output_images_nuc)

- [Postprocessing](https://github.com/JoelSchaust/ISS-segmentation-pipeline/tree/main/code/nuc_segmentation/nuc_Postprocessing.py)
```bash
mamba activate base_environment.yml 
python code/nuc_Postprocessing.py --hpi 6 --fov 15 --s 5 # change the arguments in order to call different fovs
```
Output folder: [Postprocessed nuclei](https://github.com/JoelSchaust/ISS-segmentation-pipeline/tree/main/data/processed/postprocessed_images_nuc)

## Cytoplasm segmentation
- [Use custom model](https://github.com/JoelSchaust/ISS-segmentation-pipeline/tree/main/code/cyto_segmentation/use_custom_model_cytoplasm.py)
```bash
mamba activate cellpose_environment.yml 
python code/nuc_use_custom_model.py --hpi 6 --fov 15 --s 5 # change the arguments in order to call different fovs
```
Output folder: [Cytoplasm output](https://github.com/JoelSchaust/ISS-segmentation-pipeline/tree/main/data/processed/output_images_cyto)

- [Postprocessing](https://github.com/JoelSchaust/ISS-segmentation-pipeline/tree/main/code/cyto_segmentation/Postprocessing_cytoplasm.py)
```bash
mamba activate base_environment.yml 
python code/nuc_Postprocessing.py --hpi 6 --fov 15 --s 5 # change the arguments in order to call different fovs
```
Output folder: [Postprocessed cytoplasm](https://github.com/JoelSchaust/ISS-segmentation-pipeline/tree/main/data/processed/postprocessed_images_cyto)

- [Remapping](https://github.com/JoelSchaust/ISS-segmentation-pipeline/tree/main/code/cyto_segmentation/remapping_cytoplasm.py)
```bash
mamba activate base_environment.yml 
python code/nuc_Postprocessing.py --hpi 6 --fov 15 --s 5 # change the arguments in order to call different fovs
```
Output folder: [Remapped cytoplasm](https://github.com/JoelSchaust/ISS-segmentation-pipeline/tree/main/data/processed/remapped_images_cyto)

However, the scripts can also be called individually, as all intermediate files already exist in the [data folder](https://github.com/JoelSchaust/ISS-segmentation-pipeline/tree/main/data).

Additionally, the hyperparameters flow threshold and cell probability threshold can be provided as arguments to experiment with different values. If this is desired, all scripts must be run sequentially with the specified parameters, as all intermediate results currently depend on certain flow thresholds and cell probability thresholds ((refer to: https://cellpose.readthedocs.io/en/latest/settings.html) (cytoplasm segmentation: ft 1.0, ct -6.0; nucleus segmentation ft 0.4, ct 0.0)).

# Evaluation 

The evaluation of the DICE scores was carried out based on the generalized DICE scores between ground truth and prediction, as well as subjected to a nucleus-cytoplasm coexistence analysis.

Dice scores with different threshold settings aswell as label counts of the respective predictions can be found in [Dice scores](https://github.com/JoelSchaust/ISS-segmentation-pipeline/blob/main/docs/Hyperparameter%20heatmaps.html); the nucleus cytoplasm coexistence is shown in this [notebook](https://github.com/JoelSchaust/ISS-segmentation-pipeline/blob/main/docs/nuc_cyto_coexistence.html).















