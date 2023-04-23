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

    # Combine the 2 dataframes for both pipelines and machines
    whole_pipelines = pd.concat([df_pipelines_worse, df_pipelines_better], ignore_index=True)
    whole_machines = pd.concat([df_machines_worse, df_machines_better], ignore_index=True)

    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    sns.barplot(data=df_pipelines_better)
    sns.barplot(data=df_pipelines_worse)

    # Plot the pipelines
    sns.barplot(data=whole_pipelines)
    plt.xlabel("Pipelines")
    plt.ylabel("Execution time (s)")
    plt.title("Comparison Worse vs Better")
    plt.show()

    # Plot the machines
    sns.barplot(data=whole_machines)
    plt.xlabel("Machines")
    plt.ylabel("Idle time (s)")
    plt.title("Comparison Worse vs Better")
    plt.show()

    df = sns.load_dataset("penguins")
    print(df)


show_individual_results("results_RR_worse.csv", "Results execute_RR")
show_individual_results("results_RR2.csv", "Results execute_RR_better")
# show_combined_results()
