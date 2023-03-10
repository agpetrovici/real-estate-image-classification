from PIL import Image

# Custom functions
def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))
def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

def process_img(file, resolution=(512,512)):
    """
    Prepare image for training.
    Converts image to square grayscale image
    """
    im = Image.open(file).convert('L')
    im2 = crop_max_square(im)
    im3 = im2.resize(resolution, Image.Resampling.LANCZOS)
    return im3