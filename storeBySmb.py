from smb.SMBConnection import SMBConnection
import os


def storeFile(smb_connection, file, path, service_name):
    with open(file, "rb") as f:
        print("send " + file + " to " + path)
        smb_connection.storeFile(service_name, path + "/" + file, f,
                                 timeout=60 * 60,
                                 show_progress=True)


def store(files_location: str, service_name: str, path_to_store, filters: list[str], delete=False):
    if filters is None:
        filters = []
    for basedir, dirs, files in os.walk(files_location):
        conn = SMBConnection('LabRead',
                             'KlavirReadLab20@#',
                             '132.74.242.29',
                             'WORKGROUP',
                             use_ntlm_v2=True)
        assert conn.connect('132.74.242.29', port=445)
        for result_file in files:
            with open(os.path.join(basedir, result_file), "rb") as f:
                if filters is not None and len(filters) > 0:
                    for fil in filters:
                        if fil in result_file:
                            storeFile(conn, os.path.join(basedir, result_file), path_to_store, service_name)
                            break
                else:
                    storeFile(conn, os.path.join(basedir, result_file), path_to_store, service_name)
            if delete:
                os.remove(os.path.join(basedir, result_file))