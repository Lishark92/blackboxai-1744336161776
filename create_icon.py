from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create a new image with a white background
    size = (256, 256)
    image = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw a blue circle
    circle_bbox = (20, 20, 236, 236)
    draw.ellipse(circle_bbox, fill='#007bff')
    
    # Draw a camera icon in white
    camera_bbox = (58, 88, 198, 168)
    draw.rectangle(camera_bbox, fill='white')
    lens_center = (128, 128)
    lens_radius = 30
    draw.ellipse((lens_center[0]-lens_radius, lens_center[1]-lens_radius,
                  lens_center[0]+lens_radius, lens_center[1]+lens_radius),
                 fill='#007bff')
    
    # Save as both PNG and ICO
    image.save('icon.png')
    image.save('icon.ico', format='ICO')
    print("Icon files created: icon.png and icon.ico")

if __name__ == '__main__':
    create_icon()
