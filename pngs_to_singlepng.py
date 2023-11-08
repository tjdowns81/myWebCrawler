from PIL import Image
import os

def combine_images_to_png(image_files, output_filename):
    images = [Image.open(image_file) for image_file in image_files]
    
    # Calculate the total height of the combined image
    total_height = sum(image.height for image in images)
    max_width = max(image.width for image in images)
    
    # Create a new image with the appropriate height and width
    combined_image = Image.new('RGB', (max_width, total_height))
    
    # Paste the images into the combined image
    y_offset = 0
    for image in images:
        combined_image.paste(image, (0, y_offset))
        y_offset += image.height
    
    # Save the combined image
    combined_image.save(output_filename)

# Main script
if __name__ == "__main__":
    # Get all PNG files in the current directory
    png_files = [f for f in os.listdir('./output') if f.endswith('.png')]
    png_files.sort()  # Sort the files by name
    
    # Output filename
    output_filename = 'combined_image.png'
    
    # Combine images
    combine_images_to_png(png_files, output_filename)
    print(f"Combined image created as '{output_filename}'.")
