import uproot
import pandas as pd
import os

# Path variables
# Parent folder where all root sub-directories are present
simu_root_files_parent_folder = "/Users/data_machine/Work/pyGate/opengate/opengate/tests/output/gate10_dataset_comparison"

"""
Root file categories based on filtering:
- simu_unfiltered_root_files_folder: Path for storing unfiltered simulation root files.
- simu_filtered_root_files_folder: Path for storing filtered root files. Filters:
  +dZ/-dZ or position constraints (posZ < 20.02 and posZ > 20.11).
"""
simu_unfiltered_root_files_folder = os.path.join(simu_root_files_parent_folder, "non_filtered_root_files")
simu_filtered_root_files_folder = os.path.join(simu_root_files_parent_folder, "filtered_root_files")

"""
Inside simu_filtered_root_files_folder, root files are divided based on filter used.
- simu_positive_dZ_filtered_root_files_folder: Path to store root files with +dZ filter.
- simu_negative_dZ_filtered_root_files_folder: Path to store root files with -dZ filter. 
- simu_lt_threshold_pos_Z_root_files_folder: Path to store root files with posZ < 20.02.
- simu_gt_threshold_pos_Z_root_files_folder: Path to store root files with posZ > 20.11. 
"""
simu_positive_dZ_filtered_root_files_folder = os.path.join(simu_filtered_root_files_folder, "filtered_positive_dZ_files")
simu_positive_dZ_filtered_root_files_folder = os.path.join(simu_filtered_root_files_folder, "filtered_negative_dZ_files")
simu_lt_threshold_pos_Z_root_files_folder = os.path.join(simu_filtered_root_files_folder, "filtered_pos_Z_lt_threshold_files")
simu_gt_threshold_pos_Z_root_files_folder = os.path.join(simu_filtered_root_files_folder, "filtered_pos_Z_gt_threshold_files")

# Change this to use with your own root file
# simu_unfiltered_root_file_name = "test075_optigan_create_dataset_carlotta_simu_entering_phase_space.root" 
# filtered_dz_root_file_name = "test075_optigan_create_dataset_carlotta_simu_entering_phase_space_filtered_positive_dz.root"

# Loop through the root files in simu_unfiltered_root_files_folder
for simu_unfiltered_root_file_name in os.listdir(simu_unfiltered_root_files_folder):
    if simu_unfiltered_root_file_name.endswith(".root"):
        print(simu_unfiltered_root_file_name)

        # Open root file and store the root tree
        with uproot.open(os.path.join(simu_unfiltered_root_files_folder, simu_unfiltered_root_file_name)) as simu_root_file:
            tree = simu_root_file["Phase"]
        
        # Convert the tree to a Pandas DataFrame
        df = tree.arrays(library="pd")

        # Filter DataFrame where pos_Z is <20.02 or >20.11 
        lt_threshold_filtered_pos_Z_df = df[df['Position_Z'] < 20.02]
        gt_threshold_filtered_pos_Z_df = df[df['Position_Z'] > 20.11]

        # Filter DataFrame based on +dZ and -dZ
        positive_dZ_filtered_df = df[df['Direction_Z'] > 0]
        negative_dZ_filtered_df = df[df['Direction_Z'] < 0]

        # Debug statements
        print(f"The length of unfiltered df is {len(df)}")
        print(f"The length of lt_threshold_filtered_pos_Z_df is {len(lt_threshold_filtered_pos_Z_df)}")
        print(f"The length of gt_threshold_filtered_pos_Z_df is {len(gt_threshold_filtered_pos_Z_df)}")
        print(f"The length of positive_dZ_filtered_df is {len(positive_dZ_filtered_df)}")
        print(f"The length of negative_dZ_filtered_df is {len(negative_dZ_filtered_df)}")



# # Save the DataFrame to a root file
# with uproot.recreate(os.path.join(simu_root_files_folder, filtered_dz_root_file_name)) as file:
#     file["Phase"] = filtered_df

# # Print required info
# print(f"The length of the dataframe is {len(df)}")
# print(f"The length of the filtered dataframe is {len(filtered_df)}")
# print(file.classnames())