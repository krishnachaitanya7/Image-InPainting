from image_masking import ImageMasker
import argparse
import os
import shutil
import random
import imageio
import pathlib

test_data_percentage = 10


def get_random_mask():
    """
    This will generate a random mask from the global variable mask_dataset
    I know it's bad, but it was the best optimal way
    Sorry!
    :return:
    """
    return random.choice(mask_dataset)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process file paths to generate dataset')
    parser.add_argument('--images_path', type=str, help='Full path to images dataset like CelebHQ etc'
                        )
    parser.add_argument('--mask_dataset_path', type=str, help='Full path to masking dataset like qd_imd',
                        )
    parser.add_argument('--dataset_save_directory', type=str, help='The full path to the directory where the'
                                                                   'dataset will be saved. '
                                                                   'Beware if directory exists '
                                                                   'it will be deleted')
    all_arguments = parser.parse_args()
    if os.path.exists(all_arguments.dataset_save_directory):
        # Delete the folder if already exists
        shutil.rmtree(all_arguments.dataset_save_directory)
    train_data_folder = all_arguments.dataset_save_directory + '/train'
    test_data_folder = all_arguments.dataset_save_directory + '/test'
    pathlib.Path(train_data_folder).mkdir(parents=True, exist_ok=True)
    pathlib.Path(test_data_folder).mkdir(parents=True, exist_ok=True)
    list_of_files = [all_arguments.images_path + '/' + f for f in os.listdir(all_arguments.images_path) if
                     os.path.isfile(os.path.join(all_arguments.images_path, f))]
    mask_dataset = [all_arguments.mask_dataset_path + '/' + f for f in os.listdir(all_arguments.mask_dataset_path) if
                    os.path.isfile(os.path.join(all_arguments.mask_dataset_path, f))]
    random.shuffle(list_of_files)
    num_files = len(list_of_files)
    train_data_percentage = 100 - test_data_percentage
    num_of_training_data = int(num_files * (train_data_percentage / 100))
    train_files = list_of_files[:num_of_training_data]
    test_files = list_of_files[num_of_training_data:]
    for each_file in train_files:
        file_name = os.path.basename(each_file)
        file_name_without_extension = file_name.split('.')[0]
        file_extension = file_name.split('.')[1]
        img_masker = ImageMasker(each_file, get_random_mask())
        masked_image = img_masker.get_masked_image()
        imageio.imwrite(train_data_folder+f"/{file_name_without_extension}_masked.{file_extension}", masked_image)
        shutil.copyfile(each_file, train_data_folder+f"/{file_name_without_extension}_original.{file_extension}")

    for each_file in test_files:
        file_name = os.path.basename(each_file)
        file_name_without_extension = file_name.split('.')[0]
        file_extension = file_name.split('.')[1]
        img_masker = ImageMasker(each_file, get_random_mask())
        masked_image = img_masker.get_masked_image()
        imageio.imwrite(test_data_folder+f"/{file_name_without_extension}_masked.{file_extension}", masked_image)
        shutil.copyfile(each_file, test_data_folder+f"/{file_name_without_extension}_original.{file_extension}")



