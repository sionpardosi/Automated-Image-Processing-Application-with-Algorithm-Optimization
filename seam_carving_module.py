import numpy as np
import cv2
import os
from flask import Flask, render_template, request, send_file, url_for, send_from_directory


def calculate_cumulative_energy(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    energy = np.sqrt(grad_x**2 + grad_y**2)
    cumulative_energy = energy.copy()

    for i in range(1, energy.shape[0]):
        for j in range(energy.shape[1]):
            left = cumulative_energy[i-1, j-1] if j > 0 else np.inf
            center = cumulative_energy[i-1, j]
            right = cumulative_energy[i-1, j+1] if j < energy.shape[1] - 1 else np.inf
            cumulative_energy[i, j] += min(left, center, right)

    return cumulative_energy

def find_vertical_seam(cumulative_energy):
    seam = [np.argmin(cumulative_energy[-1])]

    for i in range(cumulative_energy.shape[0] - 2, -1, -1):
        prev_j = seam[-1]
        candidates = [prev_j - 1, prev_j, prev_j + 1]
        valid_candidates = [j for j in candidates if 0 <= j < cumulative_energy.shape[1]]
        seam.append(min(valid_candidates, key=lambda j: cumulative_energy[i, j]))

    return seam[::-1]

def remove_vertical_seam(image, seam):
    h, w, _ = image.shape
    reduced_image = np.zeros((h, w - 1, 3), dtype=np.uint8)

    for i in range(h):
        j_remove = seam[i]
        reduced_image[i, :, :] = np.delete(image[i, :, :], j_remove, axis=0)

    return reduced_image

def process_seam_carving(file_path, new_width,):
    original_image = cv2.imread(file_path)
    energy = calculate_cumulative_energy(original_image)

    for _ in range(original_image.shape[1] - new_width):
        seam = find_vertical_seam(energy)
        original_image = remove_vertical_seam(original_image, seam)
        energy = calculate_cumulative_energy(original_image)

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'seam_carving_result.jpg')
    cv2.imwrite(output_path, original_image)

    return output_path