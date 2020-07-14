import threading
import time
import sys
import signal
import os, shutil


def delete_folder_content(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


def file_create_copy(file_path):
    content = []
    with open(file_path,"r") as f:
        for line in f:
            content.append(line)

    copy_path = file_path + "_original"
    with open(copy_path,"w") as f:
        for i in range(len(content)):
            f.write(content[i])

def file_append(file_path, string_to_append):
    content = []
    try:
        with open(file_path,"r") as f:
            for line in f:
                content.append(line)
    except FileNotFoundError:
        print("file not found - '", file_path, "' created")
        content=""


    with open(file_path,"w", errors="ignore") as f:
        for i in range(len(content)):
            f.write(content[i])
        f.write(string_to_append)


def print_after_terminal_stop():
    def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C')
    forever = threading.Event()
    forever.wait()
