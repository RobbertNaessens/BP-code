import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns


def show_individual_results(file, title):
    result = pd.read_csv(file)
    df = pd.DataFrame(result)
    # df.iloc is used for integer indexing
    df_pipelines = df.iloc[:, list(range(4)) + [-1]]

    # df.loc is used for label indexing
    df_machines = df.loc[:, "Machine1-Idle":"Machine3-Idle"]

    # Plot the pipelines
    fig = sns.barplot(data=df_pipelines)
    plt.ylabel("Execution time (s)")
    plt.title(title)

    # Plot the same y-axis
    # plt.ylim(0, 360)
    plt.show()

    # Plot the machines
    fig2 = sns.barplot(data=df_machines)
    plt.xlabel("Machines")
    plt.ylabel("Idle time (s)")
    plt.title(title)

    # plt.ylim(0, 180)
    plt.show()


def transform_result(total_df, index_df, function, machine=False):
    temp = pd.DataFrame()
    if not machine:
        temp["Execution time"] = total_df[index_df]
        temp["Pipeline"] = index_df
    else:
        temp["Idle time"] = total_df[index_df]
        temp["Machine"] = index_df
    temp["Type"] = function
    return temp


def show_all_combined_results(files, types):
    df_all_pipelines = pd.DataFrame()
    df_all_machines = pd.DataFrame()
    for looper in range(len(files)):
        result = pd.read_csv(files[looper])
        df = pd.DataFrame(result)
        # Transform the dataframe a bit
        # Add a column to the dataframe to indicate the result type
        df["Type"] = types[looper]

        df_pipelines = df.iloc[:, list(range(4)) + [-2] + [-1]]
        df_machines = df.iloc[:, list(range(4, 7)) + [-1]]

        # Transform pipelines
        pipelines = pd.DataFrame()

        # Worse results
        for i in range(1, 5):
            df = transform_result(df_pipelines, f"Pipeline{i}", types[looper])
            pipelines = pd.concat([pipelines, df])

        total = transform_result(df_pipelines, "Total", types[looper])
        pipelines = pd.concat([pipelines, total])

        # Add the pipelines_df to the global one
        df_all_pipelines = pd.concat([df_all_pipelines, pipelines])

        # ----------------------------
        # Now do the same for the machines
        # ----------------------------

        # Transform pipelines
        machines = pd.DataFrame()

        # Worse results
        for i in range(1, 4):
            df = transform_result(df_machines, f"Machine{i}-Idle", types[looper], True)
            machines = pd.concat([machines, df])

        df_all_machines = pd.concat([df_all_machines, machines])

    # Show the plot
    sns.barplot(data=df_all_pipelines, y="Execution time", x="Pipeline", hue="Type")

    plt.xlabel("Pipelines")
    plt.ylabel("Execution time (s)")
    plt.title("Comparison of algorithms")

    # plt.ylim(0, 360)
    plt.legend(loc='upper left')
    plt.show()

    sns.barplot(data=df_all_machines, y="Idle time", x="Machine", hue="Type")

    plt.xlabel("Machines")
    plt.ylabel("Idle time (s)")
    plt.title("Comparison of algorithms")

    # plt.ylim(0, 180)
    plt.show()


file_RR_worse = "Results/results_RR_worse.csv"
file_RR = "Results/results_RR2.csv"
file_MFT = "Results/results_MFT.csv"
file_Dumb = "Results/results_Dumb.csv"

# Dom algoritme
show_individual_results(file_Dumb, "Results dumb algorithm")

# Round Robin algoritmen
show_individual_results(file_RR_worse, "Results execute_RR")
show_individual_results(file_RR, "Results execute_RR_better")
show_all_combined_results([file_RR_worse, file_RR], ["Round Robin Worse", "Round Robin Better"])

# MFT algoritme
show_individual_results(file_MFT, "Results MFT algorithm")

# Gecombineerde resultaten
show_all_combined_results([file_Dumb, file_RR, file_MFT], ["Dumb", "Round Robin", "Most Fit Task"])
show_all_combined_results([file_Dumb, file_RR_worse, file_RR, file_MFT],
                          ["Dumb", "Round Robin Worse", "Round Robin Better", "Most Fit Task"])
show_all_combined_results([file_RR, file_MFT], ["Round Robin", "Most Fit Task"])
