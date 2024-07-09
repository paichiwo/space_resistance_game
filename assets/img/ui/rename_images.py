import os


def rename(input_path):
    for filename in os.listdir(input_path):
        if filename.endswith('.png'):
            new_filename = filename.split('_')[-1] if len(filename.split('_')) > 1 else None
            old_file = os.path.join(input_path, filename)
            new_file = os.path.join(input_path, new_filename)
            os.rename(old_file, new_file)



rename('rotating_planet_small/')
