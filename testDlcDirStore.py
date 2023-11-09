from smb.SMBConnection import SMBConnection

import storeBySmb

save_path =  "/yaron/ret/"

conn = SMBConnection('LabRead',
                         'KlavirReadLab20@#',
                         '132.74.242.29',
                         'WORKGROUP',
                         use_ntlm_v2=True)
assert conn.connect('132.74.242.29', port=445)
try:
    print("sending to: {}".format(save_path))
    conn.createDirectory("deeplabcutfiles", save_path)
    storeBySmb.storeDirectory("C:\\Users\\rsolomon\\simbaProjects\\yaron_analysis",
                              save_path,"deeplabcutfiles")
except Exception as e:
    print("we got error when sending dlc folder to {}, error:{}".format(save_path, e))