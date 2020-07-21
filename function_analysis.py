import os
import json
import numpy as np
import matplotlib.pyplot as plt


def total_count(group_numbers, list_dir, list_format):
    counts = np.zeros(len(group_numbers)).astype(int)
    for i, index in enumerate(group_numbers):
        counts[i] = len(open(list_dir + list_format.format(index)).readlines())
    return counts


def correct_count(group_numbers, guess_list_dir, actual_list_dir, list_format):
    counts = np.zeros(len(group_numbers)).astype(int)
    for i, index in enumerate(group_numbers):
        with open(guess_list_dir + list_format.format(index), "r") as list_file:
            guesses = set([line.split("/")[-1] for line in list_file.readlines()])
        with open(actual_list_dir + list_format.format(index), "r") as list_file:
            actuals = set([line.split("/")[-1] for line in list_file.readlines()])
        counts[i] = len(set.intersection(guesses, actuals))  # compare two set
    return counts


def print_result(group_numbers, guess_list_dir, actual_list_dir, list_format):
    guess_total = total_count(group_numbers, guess_list_dir, list_format)
    actual_total = total_count(group_numbers, actual_list_dir, list_format)
    guess_correct = correct_count(group_numbers, guess_list_dir, actual_list_dir, list_format)
    print("guess count:", guess_total, guess_total.sum())
    print("actual count:", actual_total, actual_total.sum())
    print("guess correct:", guess_correct, guess_correct.sum())

    print("correct percentage in guess:", (1 - (guess_total - guess_correct).sum()/guess_total.sum())*100)

    print("TP:", guess_correct)
    print("TN:", np.full(len(group_numbers), actual_total.sum()) - guess_total - actual_total + guess_correct
          if len(group_numbers) > 1 else None)
    print("FP:", guess_total - guess_correct)
    print("FN:", actual_total - guess_correct)


def get_confusion(group_names, guess_list_path_format, json2label):
    num_group = len(group_names)
    confusion = np.zeros((num_group, num_group)).astype(int)
    for i in range(num_group):
        if os.stat(guess_list_path_format.format(i+1)).st_size == 0:
            continue
        file_names = np.loadtxt(guess_list_path_format.format(i+1), "U90", ndmin=1)
        for file_name in file_names:
            with open(file_name, "r") as file:
                data_json = json.load(file)
            confusion[i, json2label(data_json)] += 1  # (guess, actual)
        print(f"\r\t{i}/{num_group}", end="")
    print(f"\r{num_group}")
    confusion = confusion/np.maximum(1, confusion.sum(0))[None, :]
    plt.figure(figsize=(4, 4))
    plt.gca().matshow(confusion, cmap="cividis")
    if num_group < 50:
        for i in range(num_group):
            for j in range(num_group):
                c = confusion[i, j]
                plt.gca().text(j, i, f"{c:.2f}", va='center', ha='center', color="grey", fontsize=12)
    plt.gca().set_ylabel("Guess")
    plt.gca().xaxis.set_label_position('top')
    plt.gca().set_xlabel("Actual")
    plt.xticks(range(num_group), group_names)
    plt.yticks(range(num_group), group_names)
    plt.show()
    return confusion
