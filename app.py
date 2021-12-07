import io
import base64
import cv2
from PIL import Image
from filters import *

# Generating a link to download a particular image file.
def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format = 'JPEG')
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href

# Set title.
st.title('Image Filters')

# Upload image.
uploaded_file = st.file_uploader('Choose an image file:', type=['png','jpg'])

if uploaded_file is not None:
    # Convert the file to an opencv image.
    raw_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(raw_bytes, cv2.IMREAD_COLOR)
    input_col, output_col = st.columns(2)
    with input_col:
        st.header('Original')
        # Display uploaded image.
        st.image(img, channels='BGR')

    
    brightness_level = st.slider('Brighness', -255, 255, 0)
    contrast_level = st.slider('Contrast', 0.0, 2.0, 1.0, step=.01)
    blur_level = st.slider('Blur', 1, 15, 1, step=2)
    sharp_option = st.selectbox('Sharp:',
                          ( 'None',
                            'Normal',
                            'Extreme',
                         ))

    output = img.copy()
    if brightness_level != 0:
        output = bright(output, level=brightness_level)

    if contrast_level != 1.0:
        output = contrast(output, level=contrast_level)

    if blur_level > 1:
        output = blur(output, ksize=blur_level)

    if sharp_option != 'None':
        output = sharp(output, level=sharp_option)

    # Display a selection box for choosing the filter to apply.
    option = st.selectbox('Select a filter:',
                          ( 'None',
                            'Black and White',
                            'Sepia / Vintage',
                            'Vignette Effect',
                            'Pencil Sketch',
                         ))

    # Colorspace of output image.
    color = 'BGR'

     # Generate filtered image based on the selected option.
    if option == 'None':
        # Don't show output image.
        pass
    elif option == 'Black and White':
        output = bw_filter(output)
        color = 'GRAY'
    elif option == 'Sepia / Vintage':
        output = sepia(output)
    elif option == 'Vignette Effect':
        level = st.slider('level', 0, 5, 2)
        output = vignette(output, level)
    elif option == 'Pencil Sketch':
        ksize = st.slider('Blur kernel size', 1, 11, 5, step=2)
        output = pencil_sketch(output, ksize)
        color = 'GRAY'

    with output_col:
        st.header('Output')
        st.image(output, channels=color)
        # fromarray convert cv2 image into PIL format for saving it using download link.
        if color == 'BGR':
            result = Image.fromarray(output[:,:,::-1])
        else:
            result = Image.fromarray(output)
        # Display link.
        st.markdown(get_image_download_link(result,'output.png','Download '+'Output'),
                    unsafe_allow_html=True)

    st.header('Filter Examples:')
    # Define columns for thumbnail images.
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.caption('Black and White')
        st.image('./images/sample/filter_bw.jpg')
    with col2:
        st.caption('Sepia / Vintage')
        st.image('./images/sample/filter_sepia.jpg')
    with col3:
        st.caption('Vignette Effect')
        st.image('./images/sample/filter_vignette.jpg')
    with col4:
        st.caption('Pencil Sketch')
        st.image('./images/sample/filter_pencil_sketch.jpg')
