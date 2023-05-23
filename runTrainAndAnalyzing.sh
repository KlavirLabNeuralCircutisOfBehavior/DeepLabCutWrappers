#!/bin/bash
mkdir "${HOME}/logs"
#SBATCH -J dlc-benchmark
#SBATCH -o "${HOME}/logs/%x.%j.out"
#SBATCH -e "${HOME}/logs/%x.%j.err"
#SBATCH -D $HOME
#SBATCH --time=7-00:00:00
#SBATCH --get-user-env
#SBATCH --nodes 1
#SBATCH --ntasks=1
#SBACTH -G 1
cd ~
config_file_name=$1
config_path=$2
service_name_config=$3
video_paths_smb=$4
results_paths_smb=$5
service_name_video_path=$6
service_name_result_path=$7
current_date=$(date +"%A%B%d%Y%H:%M:%S")
containerName="/users/klavir/shared/dlcContainer${current_date}.sqsh"
userName="${USER}"
git clone https://github.com/KlavirLabNeuralCircutisOfBehavior/DeepLabCutWrappers.git
cp /users/klavir/shared/pytorch:21.04-py3.sqsh "${containerName}"
IFS=. read -r file_name zip <<< "${config_file_name}"
srun --container-image="${containerName}" --container-mounts="${HOME}:/${userName}" python3 "/${userName}/DeepLabCutWrappers/trainDeepLabCut.py" "${config_path}" "${service_name_result_path}" "${config_file_name}" "/${userName}"
mkdir "video_tmp_save_path${current_date}"
srun --gpus=1 --container-image="${containerName}" --container-mounts="${HOME}:/${userName}" python3 "/${userName}/DeepLabCutWrappers/analyzeVideos.py" "/${userName}/${file_name}/config.yaml" "${video_paths_smb}" "/$USER/video_tmp_save_path${current_date}" "${results_paths_smb}" "${service_name_video_path}" "${service_name_result_path}"
rm "${containerName}"

# how to run: sbatch ../shared/TrainAndAnalyze.sh groomingL2-roni-2023-05-15.zip /roni/ homes /shahaf/pain_and_grooming_batch2/Videos/post_surgery/glass/L2/ /tzuk/test/ PUBLIC deeplabcutfiles