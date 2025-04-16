import os

def rename_files_in_folder(folder_path):
    try:
        # Get a list of all files in the folder
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        files.sort()  # Sort files alphabetically

        # Rename files starting with 01
        for index, file_name in enumerate(files, start=1):
            file_extension = os.path.splitext(file_name)[1]  # Get the file extension
            new_name = f"{index:03}{file_extension}"  # Format index with leading zero
            old_path = os.path.join(folder_path, file_name)
            new_path = os.path.join(folder_path, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed: {file_name} -> {new_name}")

        print("All files have been renamed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the folder path
folder_path = r"C:\Users\igor_\OneDrive\Área de Trabalho\coding\desafio_gatinho\renomeador\ColoqueOsArquivosAqui"  # Replace with your folder path
rename_files_in_folder(folder_path)