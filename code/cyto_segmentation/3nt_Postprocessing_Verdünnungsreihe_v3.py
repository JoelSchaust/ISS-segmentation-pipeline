import os
import numpy as np
from skimage import io, morphology, measure
from skimage.morphology import remove_small_objects
import argparse

parser = argparse.ArgumentParser(description='Remove small holes and area closing')

parser.add_argument('--ct', type=float, default=-6.0, help='cellprob threshold (-6.0 to 6.0')
parser.add_argument('--ft', type=float, default=1.0, help='flowthreshold (0.0 to 1.0')
parser.add_argument('--hpi', type=int, default=6, help='hours post infection (0-8)')
parser.add_argument('--s', type=int, default=5, help='what is s exactly? can be 1-9')
parser.add_argument('--rep', type=int, default=2, help='repetition (0-2')
parser.add_argument('--rnd', type=int, default=2, help='repetition (0-2')
parser.add_argument('--minsize', type=int, default=10000, help='minimum size for an area to be closed')
parser.add_argument('--fov', type=int, default=15, help='field of view (0-9 usually)')
parser.add_argument('--MOI', type=float, default=1, help='1.0 or 0.3')
parser.add_argument('--input', type=str, default="/home/s361852/Schreibtisch/in-situ-seq-segmentation/data/segmentation_3nt_3chan_non_mutant/Verdünnungsreihe_v3/output_images", help='input path')
parser.add_argument('--output', type=str, default="/home/s361852/Schreibtisch/in-situ-seq-segmentation/data/segmentation_3nt_3chan_non_mutant/Verdünnungsreihe_v3/postprocessed/", help='output path')
args = parser.parse_args()

rnd = args.rnd
s = args.s
ct = args.ct
ft = args.ft
hpi = args.hpi
MOI = args.MOI
fov = args.fov
rep = args.rep
min_size =args.minsize
input_path = args.input
output_path = args.output

file_name = f"ft{ft}_ct{ct}_3nt3chan_rep{rep}_{MOI}MOI_{hpi}hpi_fov{fov}_6Inc_round0{rnd}_ch0-2-4_s{s}_cp_masks.png"
input_image_path = os.path.join(input_path, file_name)

segmentation_image = io.imread(input_image_path)
processed_image = morphology.remove_small_objects(segmentation_image, min_size=min_size, connectivity=2)
closed_image = morphology.closing(processed_image, selem=np.ones((5, 5)))
area_closed_image = morphology.area_closing(closed_image, area_threshold=200)
output_image_path = os.path.join(output_path, f"RSO_{file_name}")
io.imsave(output_image_path, area_closed_image)



