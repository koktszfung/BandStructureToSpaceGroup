import numpy


def total_count(group_numbers, list_dir, list_format):
    counts = numpy.zeros(len(group_numbers)).astype(int)
    for i, index in enumerate(group_numbers):
        counts[i] = len(open(list_dir + list_format.format(index)).readlines())
    return counts


def correct_count(group_numbers, guess_list_dir, actual_list_dir, list_format):
    counts = numpy.zeros(len(group_numbers)).astype(int)
    for i, index in enumerate(group_numbers):
        with open(guess_list_dir + list_format.format(index), "r") as list_file:
            guesses = set([line.split("/")[-1] for line in list_file.readlines()])
        with open(actual_list_dir + list_format.format(index), "r") as list_file:
            actuals = set([line.split("/")[-1] for line in list_file.readlines()])
        counts[i] = len(set.intersection(guesses, actuals))
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
    print("TN:", numpy.full(len(group_numbers), actual_total.sum()) - guess_total - actual_total + guess_correct
          if len(group_numbers) > 1 else None)
    print("FP:", guess_total - guess_correct)
    print("FN:", actual_total - guess_correct)
