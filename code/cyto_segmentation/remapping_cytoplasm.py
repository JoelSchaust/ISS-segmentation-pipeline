#this script is run from the base environment
import numpy as np
import imageio
import argparse
import os 

parser = argparse.ArgumentParser(description='remapping of 3nt images with different ct and ft thresholds')
parser.add_argument('--ct', type=float, default=-6.0, help='cellprob threshold (-6.0 to 6.0 for this peculiar experiment in steps of 2)')
parser.add_argument('--ft', type=float, default=1.0, help='flowthreshold (0.0 to 1.0 in steps of 0.25)')
parser.add_argument('--hpi', type=float, default=6, help='hours past infection')
parser.add_argument('--fov', type=float, default=15, help='field of view')
parser.add_argument('--moi', type=float, default=1, help='')
parser.add_argument('--s', type=float, default=5, help='')
parser.add_argument('--input', type=str, default="../../data/processed/postprocessed_images_cyto/", help='input path')
parser.add_argument('--output', type=str, default="../../data/processed/remapped_images_cyto/", help='output path')
args = parser.parse_args()

hpi = args.hpi
fov = args.fov
s = args.s
moi = args.moi
ct = args.ct
ft = args.ft
input_path = args.input
output_path = args.output


file_name = f"RSO_ft{ft}_ct{ct}_3nt3chan_rep2_{moi}MOI_{hpi}hpi_fov{fov}_6Inc_round02_ch0-2-4_s{s}_cp_masks.png"
gt_path = "../../data/processed/ground_truth_cyto/"
file_name_gt = f"GT_3nt3chan_rep2_{moi}MOI_{hpi}hpi_fov{fov}_6Inc_round02_ch0-2-4_s{s}.tif"

labels_image1_path = os.path.join(gt_path, file_name_gt) #1 is ground truth 
labels_image2_path = os.path.join(input_path, file_name) #segmentation result
labels_image1 = imageio.v2.imread(labels_image1_path)
labels_image2 = imageio.v2.imread(labels_image2_path)

def compute_overlap_matrix(labels1, labels2):
    max_label1 = labels1.max()
    max_label2 = labels2.max()
    overlap_matrix = np.zeros((max_label1 + 1, max_label2 + 1), dtype=np.int32)

    for label1 in range(1, max_label1 + 1):
        mask1 = (labels1 == label1)
        for label2 in range(1, max_label2 + 1):
            mask2 = (labels2 == label2)
            overlap_matrix[label1, label2] = np.sum(mask1 & mask2)

    return overlap_matrix


overlap_matrix = compute_overlap_matrix(labels_image1, labels_image2)

label_mapping = {}
rows, cols = overlap_matrix.shape

for label1 in range(1, rows):
    max_overlap = 0
    best_match = 0
    for label2 in range(1, cols):
        overlap = overlap_matrix[label1, label2]
        if overlap > max_overlap:
            max_overlap = overlap
            best_match = label2
    if best_match != 0:
        label_mapping[label1] = best_match

remapped_image = np.zeros_like(labels_image2)
for label1, label2 in label_mapping.items():
    remapped_image[labels_image2 == label2] = label1


remapped_image_save_path = f"{output_path}output_remapped_ft{ft}_ct{ct}_3nt3chan_rep2_{moi}MOI_{hpi}hpi_fov{fov}_6Inc_round02_ch0-2-4_s{s}_cp_masks.png"

remapped_image_uint8 = remapped_image.astype(np.uint8)

imageio.imwrite(remapped_image_save_path, remapped_image_uint8)




