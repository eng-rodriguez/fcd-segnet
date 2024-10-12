import os
import imageio
import numpy as np
import scienceplots
import matplotlib.pyplot as plt

# Adding LATeX to the PATH
os.environ["PATH"] += os.pathsep + '/Library/TeX/texbin'

# Reduce DPI size when using 'ieee' for SciencePlot
plt.rcParams.update({'figure.dpi': '100'})

# Set the default style for matplotlib
plt.style.use(['science', 'notebook'])

def plot_brain_scans(brain_scan, lesion_mask, slice_index=50, axis=2):
    """
    Plot the T1w, FLAIR, and Lesion Mask images in a single figure for a specific slice.
    """
    if axis == 0:
        brain_slice = brain_scan[slice_index, :, :]
        lesion_slice = lesion_mask[slice_index, :, :]
    elif axis == 1:
        brain_slice = brain_scan[:, slice_index, :]
        lesion_slice = lesion_mask[:, slice_index, :]
    else:
        brain_slice = brain_scan[:, :, slice_index]
        lesion_slice = lesion_mask[:, :, slice_index]

    fig, axes = plt.subplots(1, 2, figsize=(8, 8))
    axes[0].imshow(brain_slice.T, cmap='gray', origin='lower')
    axes[0].set_title('MRI Scan')
    
    axes[1].imshow(brain_slice.T, cmap='gray', origin='lower')
    axes[1].imshow(lesion_slice.T, cmap='hot', alpha=0.5, origin='lower')
    axes[1].set_title('MRI Scan w/ Lesion Mask')

    for ax in axes:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def plot_brain_scans_gif(brain_scan, lesion_mask, axis=2, fps=10):

    num_slices = brain_scan.shape[axis]

    frames = []

    for i in range(num_slices):
        # Slice the brain and lesion mask along the chosen axis
        if axis == 0:
            brain_slice = brain_scan[i, :, :]
            lesion_slice = lesion_mask[i, :, :]
        elif axis == 1:
            brain_slice = brain_scan[:, i, :]
            lesion_slice = lesion_mask[:, i, :]
        else:
            brain_slice = brain_scan[:, :, i]
            lesion_slice = lesion_mask[:, :, i]

        # Show the brain slice in grayscale and overlay the lesion mask in red
        fig, ax = plt.subplots()
        ax.imshow(brain_slice.T, cmap='gray', origin='lower')
        ax.imshow(lesion_slice.T, cmap='Reds', alpha=0.5, origin='lower')
        ax.axis('off')
        fig.canvas.draw()

        # Convert the figure to a numpy array
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        frames.append(image)
        plt.close(fig)

    # Save the frames as a GIF
    output_files = '../outputs/gifs/brain_scan.gif'
    imageio.mimsave(output_files, frames, fps=fps)
    print(f'Animation saved as {output_files}')