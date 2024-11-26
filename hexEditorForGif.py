def hexEditorForGif(output_filename):
    with open(output_filename, "rb") as f:
        hex_data = f.read().hex()
        new_hex_data = hex_data[:-2] + '21'
    with open(output_filename, "wb") as f:
        f.write(bytes.fromhex(new_hex_data))




