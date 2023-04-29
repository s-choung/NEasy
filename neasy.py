import os
import time
from ase.io import write, read, Trajectory
from ase.io.vasp import read_vasp
from scipy.spatial import distance
import numpy as np
from ase.neb import NEB
import sys
from image_maker import save_images, interpolate, idpp

class NEasy:
    def __init__(self):
        self.print_ascii_art()

    def print_ascii_art(self):
        neasy_interface = '''
    888b    888 8888888888
    8888b   888 888
    88888b  888 888
    888Y88b 888 8888888     8888b.  .d8888b  888  888
    888 Y88b888 888            "88b 88K      888  888
    888  Y88888 888        .d888888 "Y8888b. 888  888
    888   Y8888 888        888  888      X88 Y88b 888
    888    Y888 8888888888 "Y888888  88888P'  "Y88888
                                                  888
                                             Y8b d88P
    NEasy Ver 1.0.0 (21 Apr. 2023)            "Y88P"
    Developer: Seokhyun Choung
    NEasy saved you time? Buy him a cup of coffee :)
    '''
        print(neasy_interface)
        options_menu ='''
    ============= NEasy Options =====================
     1)  Image Maker
     2)  Pre-calculator
     3)  Calculator
     4)  Image Generator
     5)  Advanced Image Generator
     6)  Image Distance Calculator
     0)  Quit
    =================================================
     '''
        print(options_menu)

    def ask_for_structure(self):
        initial_structure = input("Enter initial structure: ")
        ini = read_vasp(initial_structure) 
        final_structure = input("Enter final structure: ")
        fin = read_vasp(final_structure)
        is_pos = ini.get_positions().flatten()
        fs_pos = fin.get_positions().flatten()
        self.distance_ini_fin = np.abs(distance.euclidean(is_pos, fs_pos))
        self.recom_images = int(self.distance_ini_fin / 1.5) 
        print('distance between initial final is ', round(self.distance_ini_fin, 2), 'Å', 'and recommended images is more than', self.recom_images)
        return ini, fin

    def image_maker(self):
        while True:
            print("""
    =======Image Maker Options:=====
    1) Interpolate
    2) IDPP (Image Dependent Pair Potential)
    0) Go back to main menu
    =================================
            """)
            choice = input("Enter the number corresponding to your choice: ")

            if choice == "1":
                initial_structure, final_structure = self.ask_for_structure()
                self.interpolate_neb = nterpolate_generator(initial_structure, final_structure, self.distance_ini_fin)
            elif choice == "2":
                initial_structure, final_structure = self.ask_for_structure()
                self.idpp_neb = idpp(initial_structure, final_structure, self.distance_ini_fin)
            elif choice == "0":
                break
            else:
                print("Invalid input. Please try again.")


    def print_progress_bar(self, current, total):
        progress = round(current / total * 100, 2)
        status_bar = self.status(progress)
        print(f"\r{status_bar} {progress}% done", end='')

    def status(self, progress):
        num = int(progress / 5)
        return '?윪' * num + '燧쒙툘' * (20 - num)
    def main(self):
        while True:
            user_choice = input("Enter the number corresponding to your choice: ")

            if user_choice == "1":
                self.image_maker()
            elif user_choice == "2":
                # Call pre_calculator here
                pass
            elif user_choice == "3":
                # Call calculator here
                pass
            elif user_choice == "4":
                # Call image_generator here
                pass
            elif user_choice == "5":
                # Call advanced_image_generator here
                pass
            elif user_choice == "0":
                print("Goodbye!")
                break
            else:
                print("Choose from 0 to 5. Plz try again.")

if __name__ == "__main__":
    neasy = NEasy()
    neasy.main()
