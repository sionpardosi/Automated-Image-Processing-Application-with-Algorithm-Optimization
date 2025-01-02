from PIL import Image

def divide_and_conquer_resize(img, new_width, new_height):
    original_width, original_height = img.size
    sections = []
    part_width = original_width // 2
    part_height = original_height // 2

    # Split the image into 4 sections
    for i in range(2):
        for j in range(2):
            left = i * part_width
            upper = j * part_height
            right = (i + 1) * part_width
            lower = (j + 1) * part_height
            section = img.crop((left, upper, right, lower))
            sections.append(section)

    # Resize each section
    resized_sections = [s.resize((new_width // 2, new_height // 2)) for s in sections]

    # Combine the sections back into one image
    new_img = Image.new('RGB', (new_width, new_height))
    new_img.paste(resized_sections[0], (0, 0))
    new_img.paste(resized_sections[1], (new_width // 2, 0))
    new_img.paste(resized_sections[2], (0, new_height // 2))
    new_img.paste(resized_sections[3], (new_width // 2, new_height // 2))

    return new_img
