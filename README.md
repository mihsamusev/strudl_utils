# STRUDL tools

List of convenience tools to work with [STRUDL](https://github.com/ahrnbom/strudl).

# Functionality

- `draw_transparent_mask.py` - generating transparent mask on top of a video frame with interactive Paint-like UI
- `generate_logfile.py` - generating frame to time mapping log files for each video
- `post_strudl_dataset.py` - posting a dataset with STRUDL API using one config file
- more coming

# Procedure
## Preparing your dataset
At this point the disk with datasets is in remote PC from which the posting will happen

1) python init_project_folder.py -f ./datasets/thermal_20191204_17/
2) create mask and put it into the project folder
3) python cashe_video_names.py -d "D:\Kolding\Termisk\20191204_17" -o ./datasets/thermal_20191204_17/

## Posting the dataset to STRUDL

At this point the disk with datasets is plugged into STRUDL server

1) python post_strudl_dataset.py

## Saving the server state
