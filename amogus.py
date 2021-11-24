from PIL import Image, ImageEnhance, ImageDraw
from color_changer import color_to_alpha
import glob, os, copy, argparse

# handle arguments from the command line
parser = argparse.ArgumentParser("image_to_amogus")
parser.add_argument("path", help="Path to target image, where the /target/ folder is the current directory.", type=str)
parser.add_argument("-size", help="Integer representing the size length of square images, and the length of the shortest side in rectangular images (16 by default).", type=int, required=False, default=16)
args = parser.parse_args()

# size of each amogus character (50x50)
amogus_size = 50

os.chdir("./target/")
infile = args.path
file, ext = os.path.splitext(infile)
orig_name = file
target_im = width = height = None

# get target image
with Image.open(infile) as im: 
    orig_w, orig_h = im.size
    min_side = min(orig_w, orig_h)
    scale = args.size / min_side # calc constant to scale by to make min side length equal to given argument
    width, height = orig_w * scale, orig_h * scale
    target_im = im.resize((int(width), int(height)), resample=Image.BILINEAR)

bkg = Image.new("RGB", (int(width * amogus_size), int(height * amogus_size)), (0, 0, 0))
bkg_draw = ImageDraw.Draw(bkg)

# generate background
for i in range(int(width)): 
    for j in range(int(height)):
        color = target_im.getpixel((i, j))
        bkg_draw.rectangle([(i * amogus_size, j * amogus_size), (i * amogus_size + amogus_size, j * amogus_size + amogus_size)], fill=color)

os.chdir("../source/")
infile = sorted(glob.glob("*.jpg"))
frames = []

# get amogus frames
for i in range(6):
    file, ext = os.path.splitext(infile[i])
    with Image.open(infile[i]) as im: 
        amogus = im.resize((amogus_size, amogus_size)).convert("RGB")
        frames.append(amogus)

# compile each frame
output_frames = []
over_x = (width * amogus_size) % amogus_size
over_y = (height * amogus_size) % amogus_size
for i in range(6): 
    converted = color_to_alpha(ImageEnhance.Contrast(frames[i]).enhance(2.0), (255, 255, 0, 255)) # make body of each frame transparent
    output_frame = copy.deepcopy(bkg)
    for j in range(int(width)): 
        for k in range(int(height)): 
            output_frame.paste(converted.convert("RGB"), (j * amogus_size, k * amogus_size), mask=converted) # overlay amogus onto previously colored background
    output_frame = output_frame.crop((0, 0, width * amogus_size - over_x, height * amogus_size - over_y)) # crop extraneous pixels
    output_frames.append(output_frame)

# save frame to output folder
output_frames[0].save("../output/" + orig_name + "_amogus.gif", save_all=True, append_images=output_frames[1:], optimize=False, duration=40, loop=0)
print(orig_name + "_amogus.gif saved in ../output/ folder. So sussy! ඞ")
