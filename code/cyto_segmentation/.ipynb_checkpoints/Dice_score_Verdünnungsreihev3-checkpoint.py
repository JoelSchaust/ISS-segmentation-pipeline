import numpy as np
import imageio
import argparse
import os
import matplotlib.pyplot as plt
from skimage import io
import pandas as pd
from skimage.segmentation import relabel_sequential
from scipy.optimize import linear_sum_assignment

parser = argparse.ArgumentParser(description='compare ground truth to threshold runs (remapped)')

parser.add_argument('--ct', type=float, default=0.0, help='cellprob threshold (-6.0 to 6.0 for this peculiar experiment in steps of 2)')
parser.add_argument('--ft', type=float, default=0.0, help='flowthreshold (0.0 to 1.0 in steps of 0.25)')
parser.add_argument('--input', type=str, default="/home/s361852/Schreibtisch/in-situ-seq-segmentation/data/segmentation_3nt_3chan_non_mutant/Verdünnungsreihe_v3/postprocessed/6hpi/remapped/", help='input path')
parser.add_argument('--output', type=str, default="/home/s361852/Schreibtisch/in-situ-seq-segmentation/data/segmentation_3nt_3chan_non_mutant/Verdünnungsreihe_v3/postprocessed/Dice_scores/", help='output path')
args = parser.parse_args()

ct = args.ct
ft = args.ft

input_path = args.input
output_path = args.output
gt_path = "/home/s361852/Schreibtisch/in-situ-seq-segmentation/data/segmentation_3nt_3chan_non_mutant/Verdünnungsreihe_v3/ground_truth/"

output_file_name_pattern = f"ft{ft}_ct{ct}_3nt3chan_rep2_1MOI_5hpi_fov13_6Inc_round02_ch0-2-4_s8.txt"
file_name_gt_pattern = f"GT_3nt3chan_rep2_1MOI_5hpi_fov13_6Inc_round02_ch0-2-4_s8.tif"
file_name_pattern = f"remapped_ft{ft}_ct{ct}_3nt3chan_rep2_1MOI_5hpi_fov13_6Inc_round02_ch0-2-4_s8_cp_masks.png"

output_path = os.path.join(output_path, output_file_name_pattern)
remapped_image_path = os.path.join(input_path, file_name_pattern)
ground_truth_path = os.path.join(gt_path, file_name_gt_pattern)

labels_image1 = imageio.imread(remapped_image_path) #remapped image 
labels_image2 = imageio.imread(ground_truth_path) #ground truth

relabelled_image_seq1, _, _ = relabel_sequential(labels_image1)
relabelled_image_seq2, _, _ = relabel_sequential(labels_image2)

num_labels_image1 = np.unique(relabelled_image_seq1).size - 1  # Subtrahiere 1, um den Hintergrund (0) auszuschließen (wichtig)
num_labels_image2 = np.unique(relabelled_image_seq2).size - 1 

num_classes = max(num_labels_image1, num_labels_image2)

cost_matrix = np.zeros((num_classes, num_classes), dtype=int)

for i in range(num_classes):
    for j in range(num_classes):
        cost_matrix[i, j] = np.sum((relabelled_image_seq1 == i) & (relabelled_image_seq2 == j))


cost_matrix_df = pd.DataFrame(cost_matrix, columns=[f"Class_{i}" for i in range(num_classes)], index=[f"Class_{i}" for i in range(num_classes)])

row_ind, col_ind = linear_sum_assignment(-cost_matrix)
mapping = dict(zip(row_ind, col_ind))

remapped_image1 = np.zeros_like(relabelled_image_seq1)
for src_class, tgt_class in mapping.items():
    remapped_image1[relabelled_image_seq1 == src_class] = tgt_class


def generalized_dice_score(pred, gt, num_classes):
    dice_scores = []
    for i in range(1, num_classes):
        pred_i = (pred == i).astype(int)
        gt_i = (gt == i).astype(int)
        intersection = np.sum(pred_i * gt_i)
        union = np.sum(pred_i) + np.sum(gt_i)
        if union == 0:
            dice_scores.append(1)  # Perfekte Übereinstimmung, wenn keine Elemente vorhanden sind
        else:
            dice_scores.append(2. * intersection / union)
    return np.mean(dice_scores), dice_scores
   

generalized_dice, dice_scores = generalized_dice_score(remapped_image1, relabelled_image_seq2, num_classes)

with open(output_path, 'w') as file:
    file.write(f"Generalized Dice Score: {generalized_dice}\n")
    file.write("Dice Score jeder Klasse:\n")
    for i, score in enumerate(dice_scores, start=1):
        file.write(f"Class {i}: {score}\n")




