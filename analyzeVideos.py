import os

import deeplabcut
from smb.SMBConnection import SMBConnection
import sys
from storeBySmb import store


def analyze(config_path, video_paths_smb, video_tmp_save_path, results_paths_smb, service_name_video_path,
            service_name_result_path):
    if ".yaml" not in config_path:
        config_path += "/config.yaml"
    conn = SMBConnection('LabRead',
                         'KlavirReadLab20@#',
                         '132.74.242.29',
                         'WORKGROUP',
                         use_ntlm_v2=True)
    assert conn.connect('132.74.242.29', port=445)
    # list the files on each share
    files = conn.listPath(service_name_video_path, video_paths_smb, timeout=30)
    for file in files:
        if "." != file.filename and ".." != file.filename:
            conn = SMBConnection('LabRead',
                                 'KlavirReadLab20@#',
                                 '132.74.242.29',
                                 'WORKGROUP',
                                 use_ntlm_v2=True)
            assert conn.connect('132.74.242.29', port=445)
            tmp_video_folder_path = os.path.join(video_tmp_save_path, os.path.basename(file.filename))
            if not os.path.exists(tmp_video_folder_path):
                os.mkdir(tmp_video_folder_path)
            tmp_video_path = [os.path.join(tmp_video_folder_path, file.filename)]
            with open(tmp_video_path[0], 'wb') as video_file:
                conn.retrieveFile(service_name_video_path, video_paths_smb + "/" + file.filename, video_file,
                                  timeout=60 * 60,
                                  show_progress=True)
            print("done downloading {}".format(file.filename))
            conn.close()
            deeplabcut.analyze_videos(
                config_path,
                tmp_video_path,
                allow_growth=True,
                dynamic=(True, 5, 50),
                auto_track=True,
                calibrate=True,
                save_as_csv=True
            )
            print("Done analyze")

            deeplabcut.create_labeled_video(
                config_path,
                tmp_video_path,
                keypoints_only=False
            )
            print("sending {} results to smb server".format(os.path.basename(file.filename)))
            store(tmp_video_folder_path, service_name_result_path, results_paths_smb, [".csv", ".h5", "labeled"],
                  True)

    # store(video_tmp_save_path, service_name_result_path, results_paths_smb, [".csv", ".h5", "labeled.mp4"], True)
    print("done!")


if __name__ == "__main__":
    analyze(*sys.argv[1:])
