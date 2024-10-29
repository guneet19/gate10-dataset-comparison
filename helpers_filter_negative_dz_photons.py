import uproot
import pandas as pd
import os

# Path variables
simulation_root_file_folder = "/Users/data_machine/Work/pyGate/opengate/opengate/tests/output"
simulation_root_file_name = "test075_optigan_create_dataset_carlotta_simu_entering_phase_space.root"
filtered_dz_root_file_name = "test075_optigan_create_dataset_carlotta_simu_entering_phase_space_filtered_positive_dz.root"

# Open the ROOT file and extract the desired tree
with uproot.open(os.path.join(simulation_root_file_folder, simulation_root_file_name)) as file:
    tree = file["Phase"]

# Convert the tree to a Pandas DataFrame
df = tree.arrays(library="pd")

# Filter DataFrame for rows where dZ is positive
filtered_df = df[df['Direction_Z'] > 0]

# Save the DataFrame to a root file
with uproot.recreate(os.path.join(simulation_root_file_folder, filtered_dz_root_file_name)) as file:
    file["Phase"] = filtered_df

# Print required info
print(f"The length of the dataframe is {len(df)}")
print(f"The length of the filtered dataframe is {len(filtered_df)}")
print(file.classnames())
