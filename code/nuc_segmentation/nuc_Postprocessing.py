import os
import numpy as np
from skimage import io, morphology, measure
from skimage.morphology import remove_small_objects
import argparse


parser = argparse.ArgumentParser(description='Remove small holes and area closing')
parser.add_argument('--ct', type=float, default=0.0, help='cellprob threshold (-6.0 to 6.0')
parser.add_argument('--ft', type=float, default=0.4, help='flowthreshold (0.0 to 1.0')
parser.add_argument('--hpi', type=int, default=4, help='hours post infection (0-8)')
parser.add_argument('--fov', type=int, default="11", help='name of mutant')
parser.add_argument('--inc', type=int, default=6, help='inc (1/2/3)')
parser.add_argument('--minsize', type=int, default=7000, help='size remove small objects')
parser.add_argument('--s', type=int, default=8, help='s-number (1-8)')
parser.add_argument('--MOI', type=float, default=1, help='1 or 0.3')
parser.add_argument('--input', type=str, default="../../data/processed/output_images_nuc/", help='input path')
parser.add_argument('--output', type=str, default="../../data/processed/postprocessed_images_nuc/", help='output path')
args = parser.parse_args()

ct = args.ct
ft = args.ft
s = args.s
hpi = args.hpi
MOI = args.MOI
fov = args.fov
inc = args.inc
min_size = args.minsize


min_size =args.minsize
input_path = args.input
output_path = args.output

file_name = f"{inc}Inc_PR8_Nepal_{MOI}MOI_{hpi}hpi_AllSegments_3R_50C__Region {fov}_Processed001_s0{s}_ch00_cp_masks.png"
input_image_path = os.path.join(input_path, file_name)

segmentation_image = io.imread(input_image_path)
processed_image = morphology.remove_small_objects(segmentation_image, min_size=min_size, connectivity=2)
closed_image = morphology.closing(processed_image, selem=np.ones((5, 5)))
area_closed_image = morphology.area_closing(closed_image, area_threshold=200)
output_image_path = os.path.join(output_path, f"RSO_{file_name}")
io.imsave(output_image_path, area_closed_image)



