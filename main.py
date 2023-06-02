import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Any

class Plotter:
    def __init__(self, plot_dir: str) -> None:
        self.plot_folder = plot_dir
        # Create the plot directory if it doesn't exist
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)

    def draw_barplot(self, df: pd.DataFrame, ax: Any, x_column: str, y_column: str, x_label: str, title: str) -> None:
        sns.barplot(ax=ax, x=x_column, y=y_column, data=df)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_column)
        ax.set_title(title)

    def draw_plots(self, json_file: str) -> List[str]:
        # Read the JSON file into a pandas DataFrame
        df = pd.read_json(json_file)
        # Initialize an empty list to store plot paths
        paths: List[str] = []

        # Iterate through the columns of the DataFrame
        for column in df.columns:
            # Skip the 'name' column
            if column == 'name':
                continue

            # Create a 1x2 subplot with shared x-axis and a specified figure size
            fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, figsize=(12,5))

            # Set the title for the entire figure
            fig.suptitle('Comparing gt_corners and rb_corners')
            
            # Create a bar plot for Ground Truth Corners on the left subplot (ax1)
            self.draw_barplot(df, ax1, 'gt_corners', column, 'Ground Truth Corners', f'Ground Truth Corners and {column}')
            
            # Create a bar plot for Model Corners on the right subplot (ax2)
            self.draw_barplot(df, ax2, 'rb_corners', column, 'Number of Corners found by the model', 
                              f'Number of Corners found by the model and {column}')

            # Save the plot to a file and append the path to the list of paths
            plot_path = os.path.join(self.plot_folder, f'{column}_plot.png')
            plt.savefig(plot_path)
            paths.append(plot_path)
            
            # Close the current plot to free up memory
            plt.close()

        # Return the list of plot paths
        return paths

if __name__ == '__main__':
    plotter = Plotter("plots")
    plotter.draw_plots("deviation.json")
