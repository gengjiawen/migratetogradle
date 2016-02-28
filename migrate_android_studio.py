import fnmatch
import os
import shutil

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


def get_immdiate_dir(folder):
    file_list = [os.path.join(folder, i) for i in next(os.walk(folder))[1]]
    return file_list

def start_migrate(eclipse_project_path, output_path):
    """
    Call this method to migrate your eclipse project
    :param eclipse_project_path: The Original eclipse path
    :param output_path: The generate folder of your Anroid Studio Project
    :return:
    """
    print("eclipse path {}, output path: {}".format(eclipse_project_path, output_path))
    dir_prefix = "android_studio_templete/"
    dirs = [(dir_prefix + i) for i in ["libs", "src/main/java", "src/main/res", "src/main/assets"]]
    for i in dirs:
        os.makedirs(i, exist_ok=True)
    if os.path.exists(output_path):
        print("remove existing")
        shutil.rmtree(output_path, onerror=onerror)
    shutil.copytree(dir_prefix, output_path)

    print("handling libs...")
    copytree(eclipse_project_path + "/libs", output_path + "/libs")
    soLibs =  get_immdiate_dir(output_path + "/libs")
    if soLibs:
        print("handling so...")
        studio_so_path = os.path.join(output_path, r"src/main/jniLibs")
        os.makedirs(studio_so_path)
        for i in soLibs:
            print(i)
            shutil.move(i, studio_so_path)

    print("handling res...")
    copytree(os.path.join(eclipse_project_path, "res"), os.path.join(output_path, r"src/main/res"))
    print("handling sourcecode...")
    copytree(os.path.join(eclipse_project_path, "src"), os.path.join(output_path, r"src/main/java"))
    print("handling assets...")
    eclipse_asset_dir = os.path.join(eclipse_project_path, "assets")
    if os.path.exists(eclipse_asset_dir) and os.listdir(eclipse_asset_dir) != []:
        asset_dir = os.path.join(output_path, r"src/main/assets")
        print(eclipse_project_path, asset_dir)
        copytree(eclipse_project_path + "/assets", asset_dir)
    else:
        print("no assets folder were found or it is empty")
    print("handling aidl...")
    aidl_files = list()
    for top, dirs, filenames in os.walk(output_path + "/src/main/java"):
        for f in fnmatch.filter(filenames, "*.aidl"):
            tf = os.path.abspath(os.path.join(top, f))
            aidl_files.append(tf)
    if aidl_files:
        print("project has aidl")
        source_root = os.path.join(output_path, "src", "main")
        for i in aidl_files:
            aa = os.path.dirname(i).replace(os.path.join(output_path, "src", "main", "java", ""), "")
            i_aidl_path = os.path.join(source_root, "aidl", aa)
            print(i_aidl_path)
            os.makedirs(i_aidl_path, exist_ok=True)
            shutil.move(i, i_aidl_path)
    print("handling manifest.xml and proguard-rules")
    shutil.copy2(eclipse_project_path + "/AndroidManifest.xml", output_path + "/src/main")
    proguard_file = eclipse_project_path + "/proguard-project.txt"
    if os.path.exists(proguard_file):
        shutil.copy2(proguard_file, output_path)
        shutil.move(output_path + "/proguard-project.txt", output_path + "/proguard-rules.pro")
    print("finished")

