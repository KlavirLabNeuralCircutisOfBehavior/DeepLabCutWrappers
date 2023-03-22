import os

import deeplabcut
from smb.SMBConnection import SMBConnection
import sys

config_path = sys.argv[1]
video_paths_smb = sys.argv[2]
conn = SMBConnection('LabRead',
                     'KlavirReadLab20@#',
                     '132.74.242.29',
                     'WORKGROUP',
                     use_ntlm_v2=True)
assert conn.connect('132.74.242.29', port=445)
# list the files on each share
files = conn.listPath('Public', video_paths_smb, timeout=30)
for file in files:
    if "." != file.filename and ".." != file.filename:
        conn = SMBConnection('LabRead',
                             'KlavirReadLab20@#',
                             '132.74.242.29',
                             'WORKGROUP',
                             use_ntlm_v2=True)
        assert conn.connect('132.74.242.29', port=445)
        tmp_video_path = [file.filename]
        with open(tmp_video_path[0], 'wb') as video_file:
            conn.retrieveFile("Public", video_paths_smb + "/" + file.filename, video_file, timeout=60 * 60,
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
print("done!")
