import os
import numpy as np
from skimage import io, morphology, measure
from skimage.morphology import remove_small_objects
import argparse

# change the parameters according to the ones you want to use (especially minsize, ct and ft))
parser = argparse.ArgumentParser(description='Remove small holes and area closing')
parser.add_argument('--ct', type=float, default=-6.0, help='cellprob threshold (-6.0 to 6.0')
parser.add_argument('--ft', type=float, default=1.0, help='flowthreshold (0.0 to 1.0')
parser.add_argument('--hpi', type=int, default=6, help='hours post infection (0-8)')
parser.add_argument('--s', type=int, default=5, help='what is s exactly? can be 1-9')
parser.add_argument('--rep', type=int, default=2, help='repetition (0-2')
parser.add_argument('--rnd', type=int, default=2, help='repetition (0-2')
parser.add_argument('--minsize', type=int, default=10000, help='minimum size for an area to be closed') #change to set the area closing threshold
parser.add_argument('--fov', type=int, default=15, help='field of view (0-9 usually)')
parser.add_argument('--moi', type=float, default=1, help='1.0 or 0.3')
parser.add_argument('--input', type=str, default="path/to/output/folder/of/3nt_use_custom_model_skript/", help='input path')
parser.add_argument('--output', type=str, default="path/to/final/output/folder", help='output path')
args = parser.parse_args()

rnd = args.rnd
s = args.s
ct = args.ct
ft = args.ft
hpi = args.hpi
moi = args.moi
fov = args.fov
rep = args.rep
min_size =args.minsize
input_path = args.input
output_path = args.output

#the name scheme is set according to the output of 3nt_use_custom_model.py skript (change if your name scheme doesnt fit)
file_name = f"ft{ft}_ct{ct}_3nt3chan_rep{rep}_{moi}MOI_{hpi}hpi_fov{fov}_6Inc_round0{rnd}_ch0-2-4_s{s}_cp_masks.png"
input_image_path = os.path.join(input_path, file_name)

segmentation_image = io.imread(input_image_path)
processed_image = morphology.remove_small_objects(segmentation_image, min_size=min_size, connectivity=2)
closed_image = morphology.closing(processed_image, selem=np.ones((5, 5)))
area_closed_image = morphology.area_closing(closed_image, area_threshold=200)
output_image_path = os.path.join(output_path, f"RSO_{file_name}")
io.imsave(output_image_path, area_closed_image)



