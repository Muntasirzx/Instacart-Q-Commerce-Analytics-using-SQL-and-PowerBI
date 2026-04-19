import matplotlib.pyplot as plt
import seaborn as sns

# Clean the data
dataset = dataset.dropna()

# Dynamically find the right columns
cat_cols = dataset.select_dtypes(include=['object', 'category']).columns
num_cols = dataset.select_dtypes(include=['float64', 'int64']).columns

segment_col = [col for col in cat_cols if 'segment' in col.lower() or 'customer' in col.lower()][0]
days_col = [col for col in num_cols if 'days' in col.lower() or 'avg' in col.lower()][0]

# Order the segments logically
order = ['VIP Customer', 'Loyal Customer', 'Regular Customer', 'Occasional Customer']

# Set the background style
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

# Create the Violin Plot
sns.violinplot(
    x=days_col, 
    y=segment_col, 
    data=dataset, 
    order=order,
    palette="magma",
    inner="quartile" 
)

plt.title('The Habit Engine: Purchasing Frequency by Segment', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Average Days Between Orders', fontsize=12, fontweight='bold')
plt.ylabel('', fontsize=12)
plt.xticks(fontsize=11, fontweight='bold')
plt.yticks(fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()