import matplotlib.pyplot as plt
import seaborn as sns

# Clean the data
dataset = dataset.dropna()

# Find the volume column dynamically
volume_col = [col for col in dataset.columns if col not in ['department', 'order_hour_of_day']][0]

# Sort the data so the lines draw perfectly from left to right (Hours 0 to 23)
dataset = dataset.sort_values(by=['department', 'order_hour_of_day'])

# Set a clean theme
sns.set_theme(style="whitegrid")

# INCREASED FIGURE SIZE: Gives the bigger fonts room to breathe
plt.figure(figsize=(12, 7)) 

# Grab all the unique departments in your visual
departments = dataset['department'].unique()

# Generate a beautiful color palette with enough colors for every department
colors = sns.color_palette("crest", n_colors=len(departments))

# THE TRICK: Loop through each department one by one, draw its exact line, and fill it!
for idx, dept in enumerate(departments):
    # Filter the data for just this one department
    dept_data = dataset[dataset['department'] == dept]
    
    # 1. Draw the hard line
    plt.plot(
        dept_data['order_hour_of_day'], 
        dept_data[volume_col], 
        color=colors[idx], 
        linewidth=3,  # THICKER LINES to match the bold text
        label=dept
    )
    
    # 2. Fill the "mountain" underneath the line
    plt.fill_between(
        dept_data['order_hour_of_day'], 
        dept_data[volume_col], 
        color=colors[idx], 
        alpha=0.3 # 30% transparency so you can see the mountains overlapping
    )

# --- FORMATTING: BIGGER & BOLDER ---

# Title
plt.title('Purchasing Rhythm: Exact Hourly Volume by Department', 
          fontsize=18, fontweight='bold', pad=20)

# X & Y Axis Labels
plt.xlabel('Hour of Day (0-23)', fontsize=14, fontweight='bold', labelpad=10)
plt.ylabel('Total Orders', fontsize=14, fontweight='bold', labelpad=10)

# Tick Marks (The actual numbers on the axes)
plt.xticks(range(0, 24), fontsize=12, fontweight='bold')
plt.yticks(fontsize=12, fontweight='bold')

# Axis Limits
plt.xlim(0, 23)
plt.ylim(0, dataset[volume_col].max() * 1.1) # Add 10% breathing room at the top

# Legend (Made the text bold, bigger, and styled the legend title)
legend = plt.legend(
    bbox_to_anchor=(1.05, 1), 
    loc='upper left', 
    prop={'size': 12, 'weight': 'bold'} # Makes the department names bold
)
plt.setp(legend.get_title(), fontsize='14', fontweight='bold', text='Department') # Makes the title bold

# Tightly pack the layout so nothing gets cut off
plt.tight_layout()
plt.show()