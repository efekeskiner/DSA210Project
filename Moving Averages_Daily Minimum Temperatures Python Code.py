import pandas as pd
import json
import glob
import matplotlib.pyplot as plt
from datetime import datetime

# Function to load and combine JSON files
def load_spotify_data(file_paths):
    all_data = []
    for file in file_paths:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_data.extend(data)
    return pd.DataFrame(all_data)

file_paths = [
    '/Users/efekeskiner2/Downloads/Spotify Extended Streaming History/Streaming_History_Audio_2015-2019_0.json',
    '/Users/efekeskiner2/Downloads/Spotify Extended Streaming History/Streaming_History_Audio_2019-2021_1.json',
    '/Users/efekeskiner2/Downloads/Spotify Extended Streaming History/Streaming_History_Audio_2021-2022_2.json',
    '/Users/efekeskiner2/Downloads/Spotify Extended Streaming History/Streaming_History_Audio_2022-2023_3.json',
    '/Users/efekeskiner2/Downloads/Spotify Extended Streaming History/Streaming_History_Audio_2024_5.json'
]

data = load_spotify_data(file_paths)

# Convert timestamp to datetime
data['ts'] = pd.to_datetime(data['ts'])
data['date'] = data['ts'].dt.date

# Exam period (example dates, adjust according to MySU schedule)
exam_periods = [
    ('2024-10-01', '2024-10-30'),
    ('2024-06-01', '2024-06-15'),
    ('2024-04-01', '2024-04-30'),
    ('2024-01-05', '2024-01-15'),
    ('2023-10-02', '2023-10-30'),
    ('2023-06-03', '2023-06-15'),
    ('2023-04-02', '2023-04-30'),
    ('2023-01-05', '2023-01-20'),
    ('2022-10-05', '2022-10-30')
]

# Helper function to determine if a date is in exam periods
def is_exam_period(date, periods):
    date = pd.Timestamp(date)  # Ensure date is in pd.Timestamp format
    for start, end in periods:
        if pd.Timestamp(start) <= date <= pd.Timestamp(end):
            return True
    return False


data['is_exam'] = data['date'].apply(lambda x: is_exam_period(x, exam_periods))

# Analyze listening trends during exam vs. non-exam periods
exam_data = data[data['is_exam'] == True]
non_exam_data = data[data['is_exam'] == False]

# Top genres/artists during exam periods
exam_top_artists = exam_data['master_metadata_album_artist_name'].value_counts().head(10)
non_exam_top_artists = non_exam_data['master_metadata_album_artist_name'].value_counts().head(10)

# Visualization
plt.figure(figsize=(10, 5))
exam_top_artists.plot(kind='bar', title='Top Artists During Exam Periods')
plt.xlabel('Artist')
plt.ylabel('Play Count')
plt.show()

plt.figure(figsize=(10, 5))
non_exam_top_artists.plot(kind='bar', title='Top Artists During Non-Exam Periods')
plt.xlabel('Artist')
plt.ylabel('Play Count')
plt.show()

# Compare play counts during exam and non-exam periods
exam_play_count = exam_data['ms_played'].sum()
non_exam_play_count = non_exam_data['ms_played'].sum()

exam_avg_play_count = exam_data['ms_played'].mean()
non_exam_avg_play_count = non_exam_data['ms_played'].mean()

print(f"Total play time during exam periods: {exam_play_count / (1000 * 60):.2f} minutes")
print(f"Total play time during non-exam periods: {non_exam_play_count / (1000 * 60):.2f} minutes")
print(f"Average play time per track during exam periods: {exam_avg_play_count / 1000:.2f} seconds")
print(f"Average play time per track during non-exam periods: {non_exam_avg_play_count / 1000:.2f} seconds")

# Visualization of play counts
labels = ['Exam Periods', 'Non-Exam Periods']
play_counts = [exam_play_count, non_exam_play_count]

plt.figure(figsize=(8, 6))
plt.bar(labels, play_counts, color=['blue', 'green'])
plt.title('Total Play Time Comparison (Exam vs. Non-Exam Periods)')
plt.ylabel('Total Play Time (ms)')
plt.show()

# Optional: Plot average play time
avg_play_counts = [exam_avg_play_count, non_exam_avg_play_count]

plt.figure(figsize=(8, 6))
plt.bar(labels, avg_play_counts, color=['orange', 'purple'])
plt.title('Average Play Time Comparison (Exam vs. Non-Exam Periods)')
plt.ylabel('Average Play Time (ms)')
plt.show()

# Identify most listened-to group during exam and non-exam periods
exam_top_group = exam_data['master_metadata_album_artist_name'].value_counts().idxmax()
non_exam_top_group = non_exam_data['master_metadata_album_artist_name'].value_counts().idxmax()

exam_group_playcounts = exam_data[exam_data['master_metadata_album_artist_name'] == exam_top_group]['ms_played']
non_exam_group_playcounts = non_exam_data[non_exam_data['master_metadata_album_artist_name'] == non_exam_top_group]['ms_played']


# Convert play time from milliseconds to minutes
exam_group_playcounts = exam_group_playcounts / (1000 * 60)
non_exam_group_playcounts = non_exam_group_playcounts / (1000 * 60)

plt.figure(figsize=(10, 6))
plt.hist(exam_group_playcounts, bins=20, alpha=0.5, label=f'{exam_top_group} (Exam Periods)', color='blue')
plt.hist(non_exam_group_playcounts, bins=20, alpha=0.5, label=f'{non_exam_top_group} (Non-Exam Periods)', color='green')
plt.title('Play Count Comparison for Top Groups (Exam vs. Non-Exam Periods)')
plt.xlabel('Play Time (Minutes)')
plt.ylabel('Frequency')
plt.legend()
plt.show()

# Save processed data to a CSV file
data.to_csv('/Users/efekeskiner2/Downloads/processed_spotify_data.csv', index=False)


print("Analysis complete. Processed data saved as 'processed_spotify_data.csv'.")
