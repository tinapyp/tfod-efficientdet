import shutil
import os


def move_files(file_list, src_folder, dst_folder):
    for file in file_list:
        # Move the image file
        src_img = os.path.join(src_folder, file)
        dst_img = os.path.join(dst_folder, file)
        shutil.copy(src_img, dst_img)

        # Move the corresponding XML file
        xml_file = file.replace(".jpg", ".xml")
        src_xml = os.path.join(src_folder, xml_file)
        dst_xml = os.path.join(dst_folder, xml_file)
        shutil.copy(src_xml, dst_xml)
