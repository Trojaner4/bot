import os
import threading

SPLIT_PREFIX = 'split_'
FILES_DIRECTORY = 'files'
NAMES_FILE = 'original_file_names.txt'

if not os.path.exists(FILES_DIRECTORY):
    os.makedirs(FILES_DIRECTORY)

def get_user_input(prompt, result):
    result.append(input(prompt))

def split_and_upload():
    result = []
    os.system("ls")
    threading.Thread(target=get_user_input, args=("Geben Sie den Dateinamen ein, den Sie hochladen möchten: ", result)).start()
    while not result:
        pass
    file_name = result[0].strip()
    if not os.path.exists(file_name):
        print("Die angegebene Datei existiert nicht.")
        return

    file_size = os.path.getsize(file_name)
    chunk_size = 25 * 1024 * 1024  # 25 MB

    with open(file_name, 'rb') as f:
        chunk_num = 1
        while True:
            chunk_data = f.read(chunk_size)
            if not chunk_data:
                break

            chunk_file_name = f"{SPLIT_PREFIX}{os.path.basename(file_name)}_part{chunk_num}"
            with open(os.path.join(FILES_DIRECTORY, chunk_file_name), 'wb') as chunk_file:
                chunk_file.write(chunk_data)

            print(f"Teil {chunk_num} von {os.path.basename(file_name)} erfolgreich gespeichert.")
            chunk_num += 1

    print("Datei erfolgreich in 25 MB große Teile zerlegt und gespeichert.")

    # Speichere den Namen der ursprünglichen Datei in einer Textdatei
    with open(NAMES_FILE, 'a') as names_file:
        names_file.write(os.path.basename(file_name) + '\n')
    os.system("python3 upload.py")

def main():
    split_and_upload()

if __name__ == "__main__":
    main()
