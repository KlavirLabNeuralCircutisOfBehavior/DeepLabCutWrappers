import argparse

from smb.SMBConnection import SMBConnection


def getFiles(service_name, files_path_smb, filters, files_download_location):
    conn = SMBConnection('LabRead',
                         'KlavirReadLab20@#',
                         '132.74.242.29',
                         'WORKGROUP',
                         use_ntlm_v2=True)
    assert conn.connect('132.74.242.29', port=445)
    # list the files on each share
    files = conn.listPath(service_name, files_path_smb, timeout=30)
    for file in files:
        if "." != file.filename and ".." != file.filename:
            isFiltered = False
            for fil in filters:
                if fil in file.filename:
                    isFiltered = True
                    break
            if isFiltered:
                with open(files_download_location + "/" + file.filename, 'wb') as video_file:
                    conn.retrieveFile(service_name, files_path_smb + "/" + file.filename, video_file,
                                      timeout=60 * 60,
                                      show_progress=True)
                print("done downloading" + file.filename)
            else:
                print("skip downloading" + file.filename)
    conn.close()


if __name__ == "__main__":
    CLI = argparse.ArgumentParser()
    CLI.add_argument(
        "--filters",  # name on the CLI - drop the `--` for positional/required parameters
        nargs="*",  # 0 or more values expected => creates a list
        type=str,
        default=[".csv", ".h5", ".mp4"],  # default if nothing is provided
    )
    CLI.add_argument("--files_download_location", type=str, default='.')
    CLI.add_argument("--service_name", type=str, default='deeplabcutfiles')
    CLI.add_argument("--files_path_smb", type=str, default='/')
    args = CLI.parse_args()
    getFiles(args.service_name, args.files_path_smb, args.filters, args.files_download_location)
