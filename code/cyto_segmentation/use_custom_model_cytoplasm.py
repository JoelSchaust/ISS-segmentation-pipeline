#this script is run from the cellpose environment 
from cellpose import models, io
from glob import glob
import os
import argparse

#to run this script, change the arguments according to the parameters you want to use, especially if your name scheme doesnt fit 
parser = argparse.ArgumentParser(description='Use custom Cellpose model for cytoplasm segmentation')
parser.add_argument('--ct', type=float, default=-6.0, help='cellprob threshold (-6.0 to 6.0')
parser.add_argument('--ft', type=float, default=1.0, help='flowthreshold (0.0 to 1.0')
parser.add_argument('--hpi', type=int, default=6, help='hours post infection (0-8)')
parser.add_argument('--s', type=int, default=5, help='what is s exactly? can be 1-9')
parser.add_argument('--rep', type=int, default=2, help='repetition (0-2')
parser.add_argument('--rnd', type=int, default=2, help='round (01-02')
parser.add_argument('--fov', type=int, default=15, help='field of view (0-9 usually)')
parser.add_argument('--moi', type=float, default=1, help='1.0 or 0.3')
parser.add_argument('--model', type=str, default='../../results/models/Cytoplasm_Segmentation', help='custom model')
parser.add_argument('--input', type=str, default='../../data/raw/input_images_cyto/', help='input path')
parser.add_argument('--output', type=str, default='../../data/processed/output_images_cyto/', help='output path')
args = parser.parse_args()

rnd = args.rnd
ct = args.ct
s = args.s
ft = args.ft
hpi = args.hpi
moi = args.moi
fov = args.fov
rep = args.rep
model_path = args.model
input_path = args.input
output_path = args.output

file = f'{input_path}3nt3chan_rep{rep}_{moi}MOI_{hpi}hpi_fov{fov}_6Inc_round0{rnd}_ch0-2-4_s{s}.tiff' #specific to name format of your data
flow_threshold = ft
cellprob_threshold = ct
model = models.CellposeModel(gpu=True, pretrained_model=model_path)

img = io.imread(file)
masks, flows, styles = model.eval(img, diameter=None, flow_threshold = flow_threshold, cellprob_threshold = cellprob_threshold, channels=[2,1])
output_file = os.path.join(output_path, f'ft{ft}_ct{ct}_' + os.path.basename(file))
io.save_masks(img, masks, flows, output_file, png=True, save_txt=False)
