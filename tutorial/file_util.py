import os

def create_dir(path):
    try:
        if os.path.exists(path):
            rmdir_recursive(path)
            os.makedirs(path, 0775)
    except Exception as e:
        print("[Error] create_dir ... ... %s" % path)
        print(e)

def save_pic(base_path, file_name, is_title, content):
    picture_dir = base_path
    if is_title:
        picture_dir = os.path.join(picture_dir, "title")
    absolute_filename = os.path.join(picture_dir, file_name)
    try:
        if not os.path.exists(picture_dir):
            os.makedirs(picture_dir, 0775)
        with open(absolute_filename, 'wb') as f:
            f.write(content)
    except Exception as e:
        print("[Error] saving picture ... ... %s" % absolute_filename)
        print(e)

def rmdir_recursive(top):
    try:
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    except Exception as e:
        print("[Error] rmdir_recursive ... ... %s" % top)
        print(e)
