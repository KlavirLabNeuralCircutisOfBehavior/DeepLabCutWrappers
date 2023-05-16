import sys
from smb.SMBConnection import SMBConnection
import os

tmp_video_path = ["../rikaTmpVideos"]
for basedir, dirs, files in os.walk(tmp_video_path[0]):
    conn = SMBConnection('LabRead',
                         'KlavirReadLab20@#',
                         '132.74.242.29',
                         'WORKGROUP',
                         use_ntlm_v2=True)
    assert conn.connect('132.74.242.29', port=445)
    for result_file in files:
        if ".csv" in result_file or ".h5" in result_file or "labeled.mp4" in result_file:
            with open(os.path.join(basedir, result_file), "rb") as f:
                print("send " + result_file + " to /rika/results1505/")
                conn.storeFile("deeplabcutfiles", "/rika/results1505/" + result_file, f,
                               timeout=60 * 60,
                               show_progress=True)