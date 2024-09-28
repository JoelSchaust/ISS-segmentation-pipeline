##this script is run from the devbio-napari or the base environment
import argparse
import napari
from pathlib import Path
from skimage import io, exposure
from skimage.io import imread
import numpy as np


parser = argparse.ArgumentParser(description='use Napari to view all results combined')
parser.add_argument('--hpi', type=int, default=6, required=False, help='hours past infection (hpi)')
parser.add_argument('--inc', type=int, default=6, required=False, help='Incubation')
parser.add_argument('--moi', type=int, default=1, required=False, help='r Infektion')
parser.add_argument('--s', type=int, default=5, required=False, help='s')
parser.add_argument('--fov', type=int, default=15, required=False, help='field of view')
parser.add_argument('--ft', type=float, default=1.0, required=False, help='Flow threshold')
parser.add_argument('--ct', type=float, default=-6.0, required=False, help='Cell probability threshold')
args = parser.parse_args()    


hpi = args.hpi
inc = args.inc
fov = args.fov
s = args.s 
moi = args.moi 
ft = args.ft
ct = args.ct


def main():


    image1_path = f'../data/raw/input_images_cyto/3nt3chan_rep2_1MOI_{hpi}hpi_fov{fov}_6Inc_round02_ch0-2-4_s{s}.tiff'
    image2_path = f'../data/raw/input_images_nuc/6Inc_PR8_Nepal_1MOI_{hpi}hpi_AllSegments_3R_50C__Region {fov}_Processed001_s0{s}_ch00.tif'  
  

    label1_path = f'../data/processed/output_images_cyto/ft{args.ft}_ct{args.ct}_3nt3chan_rep2_1MOI_{hpi}hpi_fov{fov}_6Inc_round02_ch0-2-4_s{s}_cp_masks.png'
    label2_path = f'../data/processed/postprocessed_images_cyto/RSO_ft1.0_ct-6.0_3nt3chan_rep2_1MOI_{hpi}hpi_fov{fov}_6Inc_round02_ch0-2-4_s{s}_cp_masks.png' #there currently are only outputs with these set ft and ct parameters. 
    label3_path = f'../data/processed/output_images_nuc/ft0.4_ct0.0_nuc_6Inc_PR8_Nepal_1MOI_{hpi}hpi_AllSegments_3R_50C__Region {fov}_Processed001_s0{s}_ch00_cp_masks.png' #only default parameters for ft and ct available at the moment, can be created with use_custom_model.py
    label4_path = f'../data/processed/postprocessed_images_nuc/RSO_ft0.4_ct0.0_nuc_6Inc_PR8_Nepal_1MOI_{hpi}hpi_AllSegments_3R_50C__Region {fov}_Processed001_s0{s}_ch00_cp_masks.png'
    label5_path = f'../data/processed/ground_truth_cyto/GT_3nt3chan_rep2_1MOI_{hpi}hpi_fov{fov}_6Inc_round02_ch0-2-4_s{s}.tif'
    label6_path = f'../data/processed/ground_truth_nuc/GT_nuc_6Inc_PR8_Nepal_1MOI_{hpi}hpi_AllSegments_3R_50C__Region {fov}_Processed001_s0{s}_ch00.tif'
    
    image1 = imread(image1_path)
    image2 = imread(image2_path)
    image3 = imread(image2_path)
    
    label1 = imread(label1_path)
    label2 = imread(label2_path)
    label3 = imread(label3_path)
    label4 = imread(label4_path)
    label5 = imread(label5_path)
    label6 = imread(label6_path)

    
    p1, p99 = np.percentile(image2, (1, 99))
    normalized = exposure.rescale_intensity(image2, in_range=(p1, p99), out_range=(0, 1))
  
    viewer = napari.Viewer()
    viewer.add_image(image1, name='3chan', visible=False)
    viewer.add_image(normalized, name='nuc/ch0 -normalized', visible=True)
    viewer.add_image(image3, name='nuc/ch0', visible=False)

    viewer.add_labels(label1, name=f'prediction cells raw, {args.ft}, {args.ct}', visible=False)
    viewer.add_labels(label2, name='postprocessed cell predictions (set ft+ct)', visible=True)
    viewer.add_labels(label3, name='prediction nuclei raw', visible=False)
    viewer.add_labels(label4, name='prediction nuclei postprocessed', visible=True)    
    viewer.add_labels(label5, name='Labels cells GT', visible=False)
    viewer.add_labels(label6, name='Labels nuc GT', visible=False)

    label_layer2 = viewer.layers['postprocessed cell predictions (set ft+ct)']
    label_layer2.contour = 7  

    label_layer4 = viewer.layers['prediction nuclei postprocessed']
    label_layer4.contour = 7 

    
    napari.run()

if __name__ == '__main__':
    main()
