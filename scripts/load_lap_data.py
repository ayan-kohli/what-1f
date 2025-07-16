from matplotlib import pyplot as plt 
import seaborn as sns 
import fastf1 
import fastf1.plotting 
import pandas as pd

fastf1.Cache.enable_cache('cache')

fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme="fastf1")

race = fastf1.get_session(2023, "Monza", "R")
race.load()

laps = race.laps.pick_drivers("VER").reset_index()
laps["LapTimeSeconds"] = laps["LapTime"].dt.total_seconds()
laps["StintStartLap"] = laps.groupby("Stint")["LapNumber"].transform("min")
laps['TireAge'] = laps['LapNumber'] - laps['StintStartLap']

df = laps[['LapNumber', 'Compound', 'Stint', 'TireAge', 'LapTimeSeconds', 'PitInTime', 'PitOutTime']].copy()

pit_laps = df[df['PitInTime'].notna()]['LapNumber'].tolist()

plt.figure(figsize=(12, 6))
ax = plt.gca()

plt.figure(figsize=(12, 6))
sns.scatterplot(
    data=laps,
    x="LapNumber",
    y="LapTime",
    hue="Compound",
    palette=fastf1.plotting.get_compound_mapping(session=race),
    s=80,
    linewidth=0,
    legend='auto',
    ax=ax
)

for lap in pit_laps:
    ax.axvline(x=lap, color='red', linestyle='--', alpha=0.7, label='Pit Stop' if lap == pit_laps[0] else "")

ax.set_title("Lap Times Colored by Tire Compound – Max Verstappen (Monza 2023)")
ax.set_xlabel("Lap Number")
ax.set_ylabel("Lap Time (seconds)")
ax.grid(True)
ax.invert_yaxis()
plt.tight_layout()
plt.show()