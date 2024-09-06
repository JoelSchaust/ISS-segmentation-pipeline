from cellpose import models, io
from glob import glob
import os
import argparse

parser = argparse.ArgumentParser(description='Use custom Cellpose model for cytoplasm segmentation')
parser.add_argument('--ct', type=float, default=-6.0, help='cellprob threshold (-6.0 to 6.0')
parser.add_argument('--ft', type=float, default=1.0, help='flowthreshold (0.0 to 1.0')
parser.add_argument('--hpi', type=int, default=6, help='hours post infection (0-8)')
parser.add_argument('--s', type=int, default=5, help='what is s exactly? can be 1-9')
parser.add_argument('--rep', type=int, default=2, help='repetition (0-2')
parser.add_argument('--rnd', type=int, default=2, help='round (01-02')
parser.add_argument('--fov', type=int, default=15, help='field of view (0-9 usually)')
parser.add_argument('--MOI', type=float, default=1, help='1.0 or 0.3')
parser.add_argument('--model', type=str, default="/home/s361852/Schreibtisch/in-situ-seq-segmentation/code/models/3nt3chan_v1", help='custom model')
parser.add_argument('--input', type=str, default="/home/s361852/Schreibtisch/in-situ-seq-segmentation/data/segmentation_3nt_3chan_non_mutant/Verdünnungsreihe_v3/input_images/", help='input path')
parser.add_argument('--output', type=str, default="/home/s361852/Schreibtisch/in-situ-seq-segmentation/data/segmentation_3nt_3chan_non_mutant/Verdünnungsreihe_v3/output_images/", help='output path')
args = parser.parse_args()

#3nt3chan_rep{rep}_{MOI}MOI_{hpi}hpi_fov{fov}_6Inc_round{rnd}_ch0-2-4_s{s}.tiff
rnd = args.rnd
ct = args.ct
s = args.s
ft = args.ft
hpi = args.hpi
MOI = args.MOI
fov = args.fov
rep = args.rep
model_path = args.model
input_path = args.input
output_path = args.output

#3nt3chan_rep2_1MOI_6hpi_fov15_6Inc_round02_ch0-2-4_s5.tiff
file = f"{input_path}3nt3chan_rep{rep}_{MOI}MOI_{hpi}hpi_fov{fov}_6Inc_round0{rnd}_ch0-2-4_s{s}.tiff"
flow_threshold = ft
cellprob_threshold = ct
model = models.CellposeModel(gpu=True, pretrained_model=model_path)

img = io.imread(file)
masks, flows, styles = model.eval(img, diameter=None, flow_threshold = flow_threshold, cellprob_threshold = cellprob_threshold, channels=[2,1])
output_file = os.path.join(output_path, f"ft{ft}_ct{ct}_" + os.path.basename(file))
io.save_masks(img, masks, flows, output_file, png=True, save_txt=False)