from sys import maxsize
import os


def hexEditorForGif(output_filename):
    maxSize=0
    output_filenameList = []
    with open(output_filename, "rb") as f:
        hex_data = f.read().hex()
        new_hex_data = hex_data[:-2] + '21'
    with open(output_filename, "wb") as f:
        f.write(bytes.fromhex(new_hex_data))




def checkFilesize(filename):
    stats = os.stat(filename)
    return float((stats.st_size/(1024**2)).__format__("0.2f"))