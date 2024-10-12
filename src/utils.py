import nibabel as nib

def load_nifti_image(filepath):
    """
    """
    img = nib.load(filepath)
    data = img.get_fdata()
    return img, data