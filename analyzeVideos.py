import os

import deeplabcut
from smb.SMBConnection import SMBConnection
import sys

config_path = sys.argv[1]
video_paths_smb = sys.argv[2]
video_tmp_save_path = sys.argv[3]
results_paths_smb = sys.argv[4]
service_name_video_path = sys.argv[5]
service_name_result_path = sys.argv[6]
conn = SMBConnection('LabRead',
                     'KlavirReadLab20@#',
                     '132.74.242.29',
                     'WORKGROUP',
                     use_ntlm_v2=True)
assert conn.connect('132.74.242.29', port=445)
# list the files on each share
files = conn.listPath('deepLabCutFiles', video_paths_smb, timeout=30)
for file in files:
    if "." != file.filename and ".." != file.filename:
        conn = SMBConnection('LabRead',
                             'KlavirReadLab20@#',
                             '132.74.242.29',
                             'WORKGROUP',
                             use_ntlm_v2=True)
        assert conn.connect('132.74.242.29', port=445)
        tmp_video_path = [os.path.join(video_tmp_save_path, file.filename)]
        with open(tmp_video_path[0], 'wb') as video_file:
            conn.retrieveFile(service_name_video_path, video_paths_smb + "/" + file.filename, video_file,
                              timeout=60 * 60,
                              show_progress=True)
        print("done downloading" + file.filename)
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
            keypoints_only=False,
        )
        os.remove(tmp_video_path[0])
        basedir, dirs, files = os.walk(video_tmp_save_path)
        conn = SMBConnection('LabRead',
                             'KlavirReadLab20@#',
                             '132.74.242.29',
                             'WORKGROUP',
                             use_ntlm_v2=True)
        assert conn.connect('132.74.242.29', port=445)
        for result_file in files:
            with open(os.path.join(basedir, result_file)) as f:
                print("send " + result_file + " to " + results_paths_smb)
                conn.storeFile(service_name_result_path, results_paths_smb, f, timeout=60 * 60, show_progress=True)
            os.remove(os.path.join(basedir, result_file))
print("done!")
