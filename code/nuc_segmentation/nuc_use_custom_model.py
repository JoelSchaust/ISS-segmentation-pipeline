#use this script with the cellpose environment
from cellpose import models, io
from glob import glob
import os
import argparse

parser = argparse.ArgumentParser(description='Use custom Cellpose model for nucleus segmentation')
parser.add_argument('--ct', type=float, default=0.0, help='cellprob threshold (-6.0 to 6.0')
parser.add_argument('--ft', type=float, default=0.4, help='flowthreshold (0.0 to 1.0')
parser.add_argument('--hpi', type=int, default=4, help='hours post infection (0-8)')
parser.add_argument('--fov', type=int, default="11", help='field of view number')
parser.add_argument('--inc', type=int, default=6, help='inc (1/2/3)')
parser.add_argument('--s', type=int, default=8, help='s-number (1-8)')
parser.add_argument('--MOI', type=float, default=1, help='1.0 or 0.3')
parser.add_argument('--model', type=str, default="../../results/models/Nucleus_Segmentation", help='custom model')
parser.add_argument('--input', type=str, default="../../data/raw/input_images_nuc/", help='input path')
parser.add_argument('--output', type=str, default="../../data/processed/output_images_nuc/", help='output path')
args = parser.parse_args()

ct = args.ct
ft = args.ft
s = args.s
hpi = args.hpi
MOI = args.MOI
fov = args.fov
inc = args.inc

model_path = args.model
input_path = args.input
output_path = args.output

#{inc}Inc_PR8_Nepal_{MOI}MOI_{hpi}hpi_AllSegments_3R_50C__Region {fov}_Processed001_s0{s}_ch00.tif
file = f"{input_path}{inc}Inc_PR8_Nepal_{MOI}MOI_{hpi}hpi_AllSegments_3R_50C__Region {fov}_Processed001_s0{s}_ch00.tif"
flow_threshold = ft
cellprob_threshold = ct
model = models.CellposeModel(gpu=True, pretrained_model=model_path)

img = io.imread(file)
masks, flows, styles = model.eval(img, diameter=None, flow_threshold = flow_threshold, cellprob_threshold = cellprob_threshold)
output_file = os.path.join(output_path, f"ft{ft}_ct{ct}_nuc_" + os.path.basename(file))
io.save_masks(img, masks, flows, output_file, png=True, save_txt=False)

