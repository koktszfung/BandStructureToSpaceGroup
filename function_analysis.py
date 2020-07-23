import os
import json
import numpy as np
import matplotlib.pyplot as plt


def total_count(group_numbers, list_dir, list_format):
    # counts = np.zeros(len(group_numbers)).astype(int)
    # for i, index in enumerate(group_numbers):
    #     counts[i] = len(open(list_dir + list_format.format(index)).readlines())
    # return counts
    return np.array([len(open(list_dir + list_format.format(gnum)).readlines()) for gnum in group_numbers])


def correct_count(group_numbers, guess_list_dir, actual_list_dir, list_format):
    counts = np.zeros(len(group_numbers)).astype(int)
    for i, index in enumerate(group_numbers):
        with open(guess_list_dir + list_format.format(index), "r") as list_file:
            guesses = set([line.split("/")[-1] for line in list_file.readlines()])
        with open(actual_list_dir + list_format.format(index), "r") as list_file:
            actuals = set([line.split("/")[-1] for line in list_file.readlines()])
        counts[i] = len(set.intersection(guesses, actuals))  # compare two set
    return counts


def print_result(group_numbers, guess_list_dir, actual_list_dir, list_format, validate_size):
    guess_total = total_count(group_numbers, guess_list_dir, list_format)
    actual_total = np.floor(total_count(group_numbers, actual_list_dir, list_format)*validate_size)
    guess_correct = correct_count(group_numbers, guess_list_dir, actual_list_dir, list_format)
    print("guess count:", guess_total, guess_total.sum())
    print("actual count:", actual_total, actual_total.sum())
    print("guess correct:", guess_correct, guess_correct.sum())
    print("correct percentage in guess:", (1 - (guess_total - guess_correct).sum()/guess_total.sum())*100)
    print("TP:", guess_correct)
    print("TN:", np.full(len(group_numbers), actual_total.sum()) - guess_total - actual_total + guess_correct)
    print("FP:", guess_total - guess_correct)
    print("FN:", actual_total - guess_correct)


def get_confusion(guess_list_paths, json2label):
    num_group = len(guess_list_paths)
    confusion = np.zeros((num_group, num_group)).astype(int)
    for i, guess_list_path in enumerate(guess_list_paths):
        if os.stat(guess_list_path).st_size == 0:
            continue
        file_names = np.loadtxt(guess_list_path, "U90", ndmin=1)
        for file_name in file_names:
            with open(file_name, "r") as file:
                data_json = json.load(file)
            confusion[i, json2label(data_json)] += 1  # (guess, actual)
        print(f"\r\tload: {i}/{num_group}", end="")
    print(f"\rload: {num_group}")
    confusion = confusion/np.maximum(1, confusion.sum(0))[None, :]
    return confusion


def plot_confusion(json2label, guess_list_paths, group_names=None, show_text: bool = True):
    confusion = get_confusion(guess_list_paths, json2label)
    plt.matshow(confusion, fignum=False, cmap="cividis")
    num_group = len(guess_list_paths)
    if show_text:
        for i in range(num_group):
            for j in range(num_group):
                c = confusion[i, j]
                plt.gca().text(j, i, f"{c:.2f}", va='center', ha='center', color="grey", fontsize=10)
    if group_names is not None:
        plt.xticks(range(num_group), group_names, fontsize=8)
        plt.yticks(range(num_group), group_names, fontsize=8)
    plt.gca().set_ylabel("Guess")
    plt.gca().set_xlabel("Actual")


def show_confusion(json2label, guess_list_paths, group_names=None, show_text: bool = True):
    plot_confusion(json2label, guess_list_paths, group_names, show_text)
    plt.show()
