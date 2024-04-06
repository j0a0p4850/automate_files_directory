import logging
import os.path
import shutil
import time
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move

import logging

source_directory = r"\Users\Acer\Downloads"
img_directory = r"\Users\Acer\Downloads\Images"
documents_directory = r"\Users\Acer\Downloads\Documents"

#Takes and set the file path
def makeFileUnique(path):
    file_name, extension = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = file_name + " (" + str(counter) + ")" + extension
        counter += 1
    return path

def move(dest, entry, name):
    file_exist = os.path.exists(dest + "/" + name)
    if file_exist:
        unique_name = makeFileUnique(name)
        os.rename(entry, unique_name)
    shutil.move(entry, dest + "/" + name)

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(source_directory) as entries:
            for entry in entries:
                name = entry.name
                dest = source_directory

                if name.endswith(".doc") or name.endswith(".docx") or name.endswith(".pdf") or name.endswith(".pptx"):
                    dest = documents_directory
                    move(dest, entry, name)
                elif name.endswith(".jpeg") or name.endswith(".png") or name.endswith(".jpg") or name.endswith(".webp"):
                    dest = img_directory
                    move(dest, entry, name)

#Did change, from the library site.
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_directory
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()





