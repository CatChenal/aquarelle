"""
Module: aquarelle.process
Main function: `image_to_edges` to extract the edges from an image.
"""
from pathlib import Path
import warnings
from PIL import Image, ImageFilter, ImageEnhance


def warning_one_line(message, category, filename, lineno,
                        file=None, line=None):
    return f"\t{filename}: {lineno}: {category.__name__}: {message}"

warnings.formatwarning = warning_one_line

SAMPLE_FILE = Path(__file__).parent.joinpath("sample.jpg")
DEFAULT_SAVE_SUFFIX = "_lines"

def image_to_edges(pic_filename,
                   reduction_factor=5, 
                   rotate_angle=None,
                   sharpen_image=True,
                   save_file=False,
                   output_filename="default"):
    """
    Extract the edges from an image.
    
    :param pic_filename (string or pathlib.Path): the original image.
    :param reduction_factor (int, 10): reduce dimensions by this number
           if w or h is > 1024. Set to 1 to keep original dimensions.
    :param rotate_angle (int (0, 360), None): angle of counter-clockwise
           rotation.
    :param save_file (bool, False): save the processed file.
    :param output_filename (str or pathlib.Path, "default"): output_filename
           is used to save the processed file if different from "default".
           If "default", the file is saved in the same folder as the
           original and has a contructed name as follows:
           pic_filename.stem + _lines_ + reduction_factor + .png
    """
    # Input checks:
    VALID_FORMATS = ["png","jpeg","jpg"]
    
    f = Path(pic_filename)
    if (f == SAMPLE_FILE 
        and output_filename =="default"
        and save_file):
        msg = "You must provide a non-default output filename"
        msg = "".join((msg, " for saving the processed sample file."))
        raise ValueError(msg)
    
    if not f.exists():
        raise FileNotFoundError(f"File not found: {f}")
        
    if f.suffix[1:] not in VALID_FORMATS:
        raise ValueError(f"Invalid format. Supported: {VALID_FORMATS}")

    
    reduction_factor = int(reduction_factor)
    if reduction_factor == 0 or reduction_factor == 1:
        reduction_factor = None
    
    if rotate_angle is not None:
        if not (rotate_angle>0 and rotate_angle<360):
            warnings.warn(f"Invalid angle (ignored):{rotate_angle}. Must be in (0, 360).")
            rotate_angle = None
              
    pic = Image.open(f)
    
    if sharpen_image:
        pic = ImageEnhance.Sharpness(pic).enhance(2.)

    if reduction_factor is not None:
        x, y = pic.size
        if x > 1024 or y > 1024:
            pic = pic.resize((x//reduction_factor, y//reduction_factor))
            warnings.warn(f"Reduced by a factor of {reduction_factor}.")
                
    # Get the sharpest band from the edges
    bands = pic.filter(ImageFilter.FIND_EDGES).split()[0]
    # Convert white edges to black 255:
    outline = bands.point(lambda x: 255 if x < 100 else 0)
    
    if rotate_angle is not None:
        outline = outline.rotate(rotate_angle,expand=True) 
    
    out = None
    if save_file:
        if output_filename == "default":
            fout = f"{f.stem}{DEFAULT_SAVE_SUFFIX}"
            if reduction_factor is not None:
                fout = "".join((fout, f"_{reduction_factor}.png"))
            else:
                fout = "".join((fout, ".png"))
            out = f.parent.joinpath(fout)
        else:
            out = Path(output_filename)
            if out.suffix != ".png":
                out = out.parent.joinpath(out.stem + ".png")
                msg = "The output type must be 'png'; `output_filename`"
                msg = "".join((msg,f" was modified accordingly:\n{out}"))
                warnings.warn(msg)
        outline.save(str(out), format="png")
        
    return outline, out


def load_sample():
    return Image.open(SAMPLE_FILE)
