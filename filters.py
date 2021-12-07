import cv2
import numpy as np
import streamlit as st

@st.cache
def bw_filter(img):
    img_gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    return img_gray

@st.cache
def vignette(img, level=2):
    height, width = img.shape[:2]

    # Generate vignette mask using Gaussian kernels.
    X_resultant_kernel = cv2.getGaussianKernel(width, width / level)
    Y_resultant_kernel = cv2.getGaussianKernel(height, height / level)

    # Generating resultant_kernel matrix.
    kernel = Y_resultant_kernel * X_resultant_kernel.T
    mask = kernel / kernel.max()

    img_vignette = np.copy(img)

    # Apply the mask to each channel in the input image.
    for i in range(3):
        img_vignette[:, :, i] = img_vignette[:, :, i] * mask

    return img_vignette

@st.cache
def sepia(img):
        img_sepia = img.copy()
        # Converting to RGB as sepia matrix below is for RGB.
        img_sepia = cv2.cvtColor(img_sepia, cv2.COLOR_BGR2RGB)
        img_sepia = np.array(img_sepia, dtype=np.float64)
        img_sepia = cv2.transform(img_sepia, np.matrix([[0.393, 0.769, 0.189],
                                                        [0.349, 0.686, 0.168],
                                                        [0.272, 0.534, 0.131]]))
        # Clip values to the range [0, 255].
        img_sepia = np.clip(img_sepia, 0, 255)
        img_sepia = np.array(img_sepia, dtype=np.uint8)
        img_sepia = cv2.cvtColor(img_sepia, cv2.COLOR_RGB2BGR)
        return img_sepia

@st.cache
def pencil_sketch(img, ksize=5):
    img_blur = cv2.GaussianBlur(img, (ksize, ksize), 0, 0)
    img_sketch, _ = cv2.pencilSketch(img_blur)
    return img_sketch

@st.cache
def bright(img, level=0):
    if level == 0:
        return img
    
    matrix = np.ones(img.shape, dtype = 'uint8') * abs(level)

    if level > 0:
        img = cv2.add(img, matrix)
    else:
        img = cv2.subtract(img, matrix)

    return img

@st.cache
def contrast(img, level=1):
    if level == 1:
        return img
    
    matrix = np.ones(img.shape) * level

    img = np.uint8(cv2.multiply(np.float64(img), matrix))

    return img

@st.cache
def blur(img, ksize=1):
    if ksize == 1:
        return img

    img_blur = cv2.GaussianBlur(img, (ksize, ksize), 0, 0)

    return img_blur

@st.cache
def sharp(img, level='None'):
    if level == 'None':
        return img

    if level == 'Normal':
        kernel = np.array([[ 0, -1,  0],
                   [-1,  5, -1],
                   [ 0, -1,  0]])

    if level == 'Extreme':
        kernel = np.array([[ 0, -4,  0],
                   [-4,  17, -4],
                   [ 0, -4,  0]])

    img = cv2.filter2D(img, ddepth=-1, kernel=kernel)

    return img
