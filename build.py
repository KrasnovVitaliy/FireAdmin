import __init__
from tempfile import mkstemp
from os import remove
from shutil import move
import tarfile

ini_file_path = "./__init__.py"


def get_new_version_str():
    current_version_str = __init__.version
    current_version = current_version_str.split(".")
    new_minor_version = int(current_version[-1]) + 1
    return "{}.{}.{}".format(current_version[0], current_version[1], new_minor_version)


def update_ini_file_version(new_version_str):
    fh, abs_path = mkstemp()
    with open(fh, 'w') as new_file:
        with open(ini_file_path) as old_file:
            for line in old_file.readlines():
                if "version = " in line:
                    new_file.write("version = \"{}\"".format(new_version_str))
                else:
                    new_file.write(line)
    remove(ini_file_path)
    # Move new file
    move(abs_path, ini_file_path)


def update_template_file_version(new_version_str):
    with open("app/templates/lib/version.html", 'w') as out_file:
        out_file.write(new_version_str)


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def main():
    new_version_str = get_new_version_str()
    update_ini_file_version(new_version_str)
    update_template_file_version(new_version_str)


if __name__ == "__main__":
    main()
