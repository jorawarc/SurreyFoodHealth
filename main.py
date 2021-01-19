
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style='darkgrid')


def plot_inspections_over_time(data: pd.DataFrame):
    data = data.resample('2W', on='INSPECTIONDATE').sum().reset_index()
    groups = data[['INSPECTIONDATE', 'NUMNONCRITICAL', 'NUMCRITICAL']].groupby(by='INSPECTIONDATE').sum()
    sns.lineplot(data=groups[['NUMNONCRITICAL', 'NUMCRITICAL']], palette="muted", linewidth=2.5)
    plt.xlabel("Inspection Date")
    plt.ylabel("Number of Violations")
    plt.title("Health Violations over Time")
    plt.legend(['non-critical', 'critical'])
    plt.show()


def plot_critical_vs_non(data: pd.DataFrame):
    data = data[['NAME', 'NUMNONCRITICAL', 'NUMCRITICAL']].groupby(by='NAME').sum().reset_index().drop(columns=['NAME'])
    sns.jointplot(x="NUMNONCRITICAL", y="NUMCRITICAL",
                    palette="muted", kind='reg',
                    data=data)
    plt.show()


def worst_offenders(data: pd.DataFrame):
    data['violations'] = data['NUMCRITICAL'] + data['NUMNONCRITICAL']
    groups = data[['NAME', 'NUMCRITICAL', 'NUMNONCRITICAL', 'violations']].groupby(by='NAME').sum()
    print("Most Violations")
    print(groups.sort_values(by='violations', ascending=False).head(5))

    print('\n=== Data Stats ===')
    print(groups.describe())


def main(restaurant_path, inspection_path):
    restaurants_df = pd.read_csv(restaurant_path, usecols=['TRACKINGNUMBER', 'NAME', 'PHYSICALADDRESS'])
    inspections_df = pd.read_csv(inspection_path,
                                 usecols=['TRACKINGNUMBER', 'INSPECTIONDATE', 'INSPTYPE', 'NUMCRITICAL',
                                          'NUMNONCRITICAL', 'VIOLLUMP', 'HAZARDRATING'],
                                 parse_dates=['INSPECTIONDATE'])

    merged_df = restaurants_df.merge(inspections_df, on='TRACKINGNUMBER')
    merged_df = merged_df[(merged_df['NUMNONCRITICAL'] != 0) & (merged_df['NUMCRITICAL'] != 0) & (merged_df['HAZARDRATING'] != 'Low')]
    plot_inspections_over_time(merged_df)
    plot_critical_vs_non(merged_df)
    worst_offenders(merged_df)


if __name__ == '__main__':
    # Restaurant data, Inspection data
    main(sys.argv[1], sys.argv[2])
