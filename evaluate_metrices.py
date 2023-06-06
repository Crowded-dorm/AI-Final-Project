import cv2
import numpy as np
import argparse
import glob
import os

def masks_to_boundary(masks, dilation_ratio=0.02):
    """
    Convert binary masks to boundary masks.
    :param masks (numpy array, uint8): binary masks
    :param dilation_ratio (float): ratio to calculate dilation = dilation_ratio * image_diagonal
    :return: boundary masks (numpy array)
    """
    _, h, w = masks.shape
    img_diag = np.sqrt(h ** 2 + w ** 2)
    dilation = int(round(dilation_ratio * img_diag))
    if dilation < 1:
        dilation = 1
    kernel = np.ones((3, 3), dtype=np.uint8)
    mask_erode = np.stack([cv2.erode(im, kernel, iterations=dilation) for im in masks])
    # G_d intersects G in the paper.
    return masks - mask_erode

def isimage(path):
    ext = os.path.splitext(path)[-1].lower()
    return ext == ".png" or ext == ".jpg" or ext == ".jpeg"

def load_binary_masks(mask_root):
    mask_paths = sorted(list(filter(isimage, glob.glob(f"{mask_root}/*"))))
    masks = np.stack([cv2.imread(p, 0) for p in mask_paths])
    binary_masks = np.stack([cv2.threshold(im, 127, 255, cv2.THRESH_BINARY)[1].astype(np.float32) / 255 for im in masks])
    return binary_masks

def zero_padding(masks):
    # Pad image so mask truncated by the image border is also considered as boundary.
    padded_masks = np.stack([cv2.copyMakeBorder(im, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0) for im in masks])
    return padded_masks

def fixed_iou_score(pred, target):
    N = len(pred)
    intersect = np.stack([cv2.bitwise_and(pred[i], target[i]) for i in range(N)])
    union = np.stack([cv2.bitwise_or(pred[i], target[i]) for i in range(N)])
    intersect = intersect.sum()
    union = union.sum()
    return (intersect + 1e-6) / (union + 1e-6)

def boundry_iou_score(pred, target):
    boundry_pred = masks_to_boundary(pred)
    boundry_target = masks_to_boundary(target)
    
    return fixed_iou_score(boundry_pred, boundry_target)

def find_refine_root(seq_root):
    mask_dir = sorted(glob.glob(f"{seq_root}/*_refine"))
    return mask_dir[-1]

def find_mask_root(seq_root):
    mask_dir = sorted(glob.glob(f"{seq_root}/*_masks"))
    return mask_dir[-1]

def main(dataset, mode, pattern):
    seq_root = os.path.join('outputs', pattern)
    if mode == 'deform':
        predicted_mask_root = find_refine_root(seq_root)
    elif mode == 'no_tex':
        predicted_mask_root = find_mask_root(seq_root)
    else:
        raise "Shouldn't reach here."
    predicted_mask_root = os.path.join(predicted_mask_root, 'masks_0')
    if dataset == 'davis':
        ground_truth_mask_root = os.path.join('../DAVIS/Annotations/480p', pattern)
    else:
        ground_truth_mask_root = os.path.join('custom_dataset/gt_masks', pattern)
    print(f'Load predicted masks: {os.path.abspath(predicted_mask_root)}')
    print(f'Load ground truth masks: {os.path.abspath(ground_truth_mask_root)}')
    predicted_binary_masks = load_binary_masks(predicted_mask_root)
    gt_binary_masks = load_binary_masks(ground_truth_mask_root)
    _, H, W = gt_binary_masks.shape
    predicted_binary_masks = np.stack([cv2.resize(im, (W, H)) for im in predicted_binary_masks])
    assert(predicted_binary_masks.shape == gt_binary_masks.shape)
    
    IoU_score = fixed_iou_score(predicted_binary_masks, gt_binary_masks)
    Boundary_IoU_score = boundry_iou_score(predicted_binary_masks, gt_binary_masks)
    
    print('IoU score:', IoU_score)
    print('Boundary IoU score:', Boundary_IoU_score)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument('-i', '--image', default=None)
    parser.add_argument('-d', '--dataset', choices=['davis', 'custom'], default='davis')
    parser.add_argument('-m', '--mode', choices=['deform', 'no_tex'], default='deform')
    parser.add_argument('-p', '--pattern', default='bear')
    #parser.add_argument('-p', '--predicted_mask_root', required=True)
    #parser.add_argument('-g', '--ground_truth_mask_root', required=True)
    args = parser.parse_args()
    
    main(args.dataset, args.mode, args.pattern)