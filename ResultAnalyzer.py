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
    plt.ylim(0, 360)
    plt.show()

    # Plot the machines
    fig2 = sns.barplot(data=df_machines)
    plt.xlabel("Machines")
    plt.ylabel("Idle time (s)")
    plt.title(title)

    plt.ylim(0, 180)
    plt.show()


def show_combined_results():
    result_worse = pd.read_csv("results_RR_worse.csv")
    df = pd.DataFrame(result_worse)
    # Transform the dataframe a bit
    # Add a column to the dataframe to indicate the result type
    df["Type"] = "Worse"

    df_pipelines_worse = df.iloc[:, list(range(4)) + [-2] + [-1]]
    df_machines_worse = df.iloc[:, list(range(4, 7)) + [-1]]

    # Repeat the same steps for the other file
    result_better = pd.read_csv("results_RR2.csv")
    df2 = pd.DataFrame(result_better)
    # Transform the dataframe a bit
    # Add a column to the dataframe to indicate the result type
    df2["Type"] = "Better"

    df_pipelines_better = df2.iloc[:, list(range(4)) + [-2] + [-1]]
    df_machines_better = df2.iloc[:, list(range(4, 7)) + [-1]]

    # Transform pipelines
    pipelines = pd.DataFrame()

    # Worse results
    for i in range(1, 5):
        df = transform_result(df_pipelines_worse, f"Pipeline{i}", "Execute_RR")
        pipelines = pd.concat([pipelines, df])

    total = transform_result(df_pipelines_worse, "Total", "Execute_RR")
    pipelines = pd.concat([pipelines, total])

    # Better results
    for i in range(1, 5):
        df = transform_result(df_pipelines_better, f"Pipeline{i}", "Execute_RR_better")
        pipelines = pd.concat([pipelines, df])

    total = transform_result(df_pipelines_better, "Total", "Execute_RR_better")
    pipelines = pd.concat([pipelines, total])

    # Show the plot
    sns.barplot(data=pipelines, y="Execution time", x="Pipeline", hue="Type")

    plt.xlabel("Pipelines")
    plt.ylabel("Execution time (s)")
    plt.title("Comparison of function results execute_RR and execute_RR_better")

    plt.ylim(0, 360)
    plt.legend(loc='upper left')
    plt.show()

    # ----------------------------
    # Now do the same for the machines
    # ----------------------------

    # Transform pipelines
    machines = pd.DataFrame()

    # Worse results
    for i in range(1, 4):
        df = transform_result(df_machines_worse, f"Machine{i}-Idle", "Execute_RR", True)
        machines = pd.concat([machines, df])

    # Better results
    for i in range(1, 4):
        df = transform_result(df_machines_better, f"Machine{i}-Idle", "Execute_RR_better", True)
        machines = pd.concat([machines, df])

    sns.barplot(data=machines, y="Idle time", x="Machine", hue="Type")

    plt.xlabel("Machines")
    plt.ylabel("Idle time (s)")
    plt.title("Comparison of function results execute_RR and execute_RR_better")

    plt.ylim(0, 180)
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


# show_individual_results("results_RR_worse.csv", "Results execute_RR")
# show_individual_results("results_RR2.csv", "Results execute_RR_better")
show_combined_results()
