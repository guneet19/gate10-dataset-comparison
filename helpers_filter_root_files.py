import uproot
import pandas as pd
import os

import matplotlib.pyplot as plt
import seaborn as sns

#FIX_ME - Need to refactor into a class.  

# Path variables
# Parent folder where all root sub-directories are present.
simu_root_files_parent_folder = "/Users/data_machine/Work/pyGate/opengate/opengate/tests/output/gate10_dataset_comparison"

"""
Root file categories based on filtering:
- simu_unfiltered_root_files_folder: Path for storing unfiltered simulation root files.
- simu_filtered_root_files_folder: Path for storing filtered root files. Filters:
  +dZ/-dZ or position constraints (posZ < 20.02 and posZ > 20.11).
"""
simu_unfiltered_root_files_folder = os.path.join(simu_root_files_parent_folder, "non_filtered_root_files")
simu_filtered_global_root_files_folder = os.path.join(simu_root_files_parent_folder, "filtered_root_files")

# DELETE - These path variables are now redundant.
"""
Inside simu_filtered_root_files_folder, root files are divided based on filter used.
- simu_positive_dZ_filtered_root_files_folder: Path to store root files with +dZ filter.
- simu_negative_dZ_filtered_root_files_folder: Path to store root files with -dZ filter. 
- simu_lt_threshold_pos_Z_root_files_folder: Path to store root files with posZ < 20.02.
- simu_gt_threshold_pos_Z_root_files_folder: Path to store root files with posZ > 20.11. 
"""
simu_positive_dZ_filtered_root_files_folder = os.path.join(simu_filtered_global_root_files_folder, "filtered_positive_dZ_files")
simu_positive_dZ_filtered_root_files_folder = os.path.join(simu_filtered_global_root_files_folder, "filtered_negative_dZ_files")
simu_lt_threshold_pos_Z_root_files_folder = os.path.join(simu_filtered_global_root_files_folder, "filtered_pos_Z_lt_threshold_files")
simu_gt_threshold_pos_Z_root_files_folder = os.path.join(simu_filtered_global_root_files_folder, "filtered_pos_Z_gt_threshold_files")

# Change this to use with your own root file
# simu_unfiltered_root_file_name = "test075_optigan_create_dataset_carlotta_simu_entering_phase_space.root" 
# filtered_dz_root_file_name = "test075_optigan_create_dataset_carlotta_simu_entering_phase_space_filtered_positive_dz.root"

# Function to save a DataFrame to a ROOT file.
def save_to_root(dataframe, filename):
    with uproot.recreate(filename) as file:
        file["tree"] = dataframe
        return file["tree"]

# Loop through the root files in simu_unfiltered_root_files_folder.
for simu_unfiltered_root_file_name in os.listdir(simu_unfiltered_root_files_folder):
    if simu_unfiltered_root_file_name.endswith(".root"):
        print(simu_unfiltered_root_file_name)

        # Open root file and store the root tree.
        with uproot.open(os.path.join(simu_unfiltered_root_files_folder, simu_unfiltered_root_file_name)) as simu_root_file:
            tree = simu_root_file["Phase"]
        
        # Convert the tree to a Pandas DataFrame.
        df = tree.arrays(library="pd")

        # Filter DataFrame where pos_Z is <20.02 or >20.11.
        lt_threshold_filtered_pos_Z_df = df[df['Position_Z'] < 20.02]
        gt_threshold_filtered_pos_Z_df = df[df['Position_Z'] > 20.11]

        # Filter DataFrame based on +dZ and -dZ.
        positive_dZ_filtered_df = df[df['Direction_Z'] > 0]
        negative_dZ_filtered_df = df[df['Direction_Z'] < 0]

        # Create an individual folder for every root file to store filtered output.
        simu_filtered_individual_root_file_folder = os.path.join(simu_filtered_global_root_files_folder, simu_unfiltered_root_file_name.replace(".root", ""))
        os.makedirs(simu_filtered_individual_root_file_folder, exist_ok="True")

        # Dictionary mapping file name with data stored in it. 
        file_names = {
            "lt_20.02_filter.root": lt_threshold_filtered_pos_Z_df,
            "gt_20.11_filter.root": gt_threshold_filtered_pos_Z_df,
            "positive_dZ_filter.root": positive_dZ_filtered_df,
            "negative_dZ_filter.root": negative_dZ_filtered_df
        }

        """
        Create root files from data filtered from simulation root files. 
        - root_file_filter_folder: Folder in which final filtered root files are created.
        - final_filtered_root_file_save_path: Path of the filtered root file. 
        """
        for file_name, data in file_names.items():
            filtered_tree = None

            root_file_filter_folder = os.path.join(simu_filtered_individual_root_file_folder, file_name.replace(".root", ""))
            os.makedirs(root_file_filter_folder, exist_ok=True)

            final_filtered_root_file_save_path = os.path.join(root_file_filter_folder, file_name)
            exists = os.path.exists(final_filtered_root_file_save_path)
            
            if not exists:
            # Create root file. 
                print("I am inside if statement")
                filtered_tree = save_to_root(data, final_filtered_root_file_save_path)
                print(f"The information of the tree is {tree}")

            print(filtered_tree)

            """
            Create histogram graphs for each filter. 
            """
            # Filtered root file graphs folder
            root_file_histograms_graphs_folder = os.path.join(root_file_filter_folder, "distribution_graphs")
            os.makedirs(root_file_histograms_graphs_folder, exist_ok=True)

            if filtered_tree == None:
                with uproot.open(final_filtered_root_file_save_path) as simu_root_file:
                    filtered_tree = simu_root_file["tree"]

            for branch_name, branch in filtered_tree.iteritems():
                data = branch.array()

                # Plot and save histogram for this branch
                plt.figure(figsize=(10,6))
                plt.ticklabel_format(axis='x', style='plain')
                sns.histplot(data, bins=50, kde=False, color="teal")
                plt.title(f"Histograms of {branch_name}", fontsize=16, fontweight='bold')
                plt.xlabel(branch_name, fontsize=14)
                plt.ylabel("Frequency", fontsize=14)

                # Improve layout
                plt.tight_layout()

                simu_root_distribution_graph_output_path = os.path.join(root_file_histograms_graphs_folder, f"{branch_name}_histogram.png")
                plt.savefig(simu_root_distribution_graph_output_path, dpi=300)
                plt.close()

        # DELETE after testing.
        # Debug statements.
        print(f"The length of unfiltered df is {len(df)}")
        print(f"The length of lt_threshold_filtered_pos_Z_df is {len(lt_threshold_filtered_pos_Z_df)}")
        print(f"The length of gt_threshold_filtered_pos_Z_df is {len(gt_threshold_filtered_pos_Z_df)}")
        print(f"The length of positive_dZ_filtered_df is {len(positive_dZ_filtered_df)}")
        print(f"The length of negative_dZ_filtered_df is {len(negative_dZ_filtered_df)}")