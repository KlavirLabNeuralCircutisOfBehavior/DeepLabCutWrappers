import sys

import deeplabcut

video_path = sys.argv[1]
superanimal_name = 'superanimal_topviewmouse'
scale_list = [200, 300, 400]  # image height pixel size range and increment

deeplabcut.video_inference_superanimal([video_path], superanimal_name,scale_list=scale_list)