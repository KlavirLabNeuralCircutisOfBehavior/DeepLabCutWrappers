#!/bin/bash
mkdir "${HOME}/logs"
cd ~
config_file_name=$1
config_path=$2
service_name_config=$3
video_paths_smb=$4
results_paths_smb=$5
service_name_video_path=$6
service_name_result_path=$7
current_date=$(date +"%A%B%d%Y%H%M%S")
containerName="/users/klavir/shared/dlcContainer${current_date}.sqsh"
userName="${USER}"
git clone https://github.com/KlavirLabNeuralCircutisOfBehavior/DeepLabCutWrappers.git
cd DeepLabCutWrappers
git pull
cd ~
cp /users/klavir/shared/pytorch:21.04-py3.sqsh "${containerName}"
IFS=. read -r file_name zip <<< "${config_file_name}"
mkdir "video_tmp_save_path${current_date}"
sbatch /users/klavir/shared/runTrainAndAnalyzingSbatch.sh config_file_name config_path service_name_config video_paths_smb results_paths_smb service_name_video_path service_name_result_path file_name current_date containerName userName

# how to run: sbatch ../shared/TrainAndAnalyze.sh groomingL2-roni-2023-05-15.zip /roni/ homes /shahaf/pain_and_grooming_batch2/Videos/post_surgery/glass/L2/ /tzuk/test/ PUBLIC deeplabcutfiles