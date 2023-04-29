
import numpy as np
from scipy.spatial import distance
from ase.neb import NEB, idpp_interpolate, interpolate
import os
from ase.io.vasp import write_vasp

def save_images(interpolate, method_name):
    output_directory = get_output_directory()
    for i, image in enumerate(interpolate, start=1):
        directory = os.path.join(output_directory, f"0{i}")
        os.makedirs(directory, exist_ok=True)
        filename = os.path.join(directory, "POSCAR")
        write_vasp(filename, image, direct=True)
    abs_output_directory = os.path.abspath(output_directory)
    print(f"Successfully generated images using {method_name}! Output directory: {abs_output_directory}")

def get_output_directory():
    while True:
        output_directory = input("Enter the desired output directory: ")
        if os.path.exists(output_directory) and os.path.isdir(output_directory):
            overwrite = input(f"Directory '{output_directory}' already exists. Do you want to overwrite it? (y/n): ")
            if overwrite.lower() == 'y':
                break
        elif os.path.exists(output_directory) and not os.path.isdir(output_directory):
            print(f"'{output_directory}' exists but is not a directory. Please choose another name.")
        else:
            break
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    return output_directory

def interpolate_generator(initial_structure, final_structure, distance_ini_fin):
    ini = initial_structure
    fin = final_structure
    images_num = int(input("Enter number of NEB images: "))
    inter_images = [ini.copy() for i in range(images_num - 1)] + [fin.copy()]
    neb = NEB(inter_images, k=0.05, parallel=True, climb=True, allow_shared_calculator=False)
    neb.interpolate()
    distance_between_images = distance_ini_fin / images_num
    print("Distance between images:", round(distance_between_images, 2), "Å")
    save_images(inter_images, 'interpolation')
    return neb
def idpp(initial_structure, final_structure, distance_ini_fin):
    ini = initial_structure
    fin = final_structure
    images_num = int(input("Enter number of NEB images: "))
    idpp_images = [ini.copy() for i in range(images_num - 1)] + [fin.copy()]

    # Create an NEB object
    neb_idpp = NEB(idpp_images, k=0.05, parallel=True, climb=True, allow_shared_calculator=False)

    # Perform the IDPP interpolation
    neb_idpp.interpolate(method='idpp')

    save_images(idpp_images, 'IDPP')
    distances = []
    for i in range(len(idpp_images) - 1):
        image_a = idpp_images[i].get_positions().flatten()
        image_b = idpp_images[i + 1].get_positions().flatten()
        distance_between_images = np.abs(distance.euclidean(image_a, image_b))
        distances.append(distance_between_images)
        print(f"Distance between 0{i+1} and 0{i+2}: {round(distance_between_images, 2)} Å")

