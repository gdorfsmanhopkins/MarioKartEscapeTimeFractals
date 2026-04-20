import os
from PIL import Image

def create_gif(input_dir, output_gif, duration=50):
    # Get list of PNG files
    png_files = [f for f in os.listdir(input_dir) if f.endswith('.png')]
    png_files.sort()  # Sort to ensure order
    images = []
    for png in png_files:
        img = Image.open(os.path.join(input_dir, png))
        images.append(img)
    
    if images:
        images[0].save(output_gif, save_all=True, append_images=images[1:], duration=duration, loop=0)
        print(f"GIF created: {output_gif}")
    else:
        print("No PNG files found.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        input_dir = sys.argv[1]
        output_gif = sys.argv[2]
        create_gif(input_dir, output_gif)
    elif len(sys.argv) == 4:
        input_dir = sys.argv[1]
        output_gif = sys.argv[2]
        duration = sys.argv[3]
        create_gif(input_dir, output_gif, int(duration))
    else:
        print("Usage: python png_to_gif.py <input_dir> <output_gif> <duration (ms, optional)>")
        sys.exit(1)
