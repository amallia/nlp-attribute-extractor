import helper
import os


def merge_multi_word_features(features):

    for key, value in features.items():

        if (len(key) > 0) and (' ' in key):
            del features[key]
            features[key.split()[-1]] = None

    return features


def get_labels(empirical, true):

    y = []
    y_hat = []

    # Read true labels
    f = open(true, 'r')

    for line in f:

        splits = line.split('|')

        positives = merge_multi_word_features({x.strip(): None for x in splits[0].split(',')})
        negatives = merge_multi_word_features({x.strip(): None for x in splits[1].split(',')})

        y.append((positives, negatives))

    f.close()

    # Read empirical labels
    f = open(empirical, 'r')

    for line in f:

        splits = line.split('|')

        positives = merge_multi_word_features({x.strip(): None for x in splits[0].split(',')})
        negatives = merge_multi_word_features({x.strip(): None for x in splits[1].split(',')})

        y_hat.append((positives, negatives))

    f.close()

    return y_hat, y


def score_file(empirical, true):

    y_hat, y = get_labels(empirical, true)

    # Compare true and empirical labels
    if len(y) != len(y_hat):
        print('MISMATCH IN FILE SIZE')
        return None, None, None, None

    true_positives = 0
    false_positives = 0
    false_negatives = 0

    total_correct = 0
    total_wrong = 0

    for i in range(len(y)):

        # What was predicted -- TP / FP
        for label in y_hat[i][0]:
            if label in y[i][0]:
                true_positives += 1
                total_correct += 1

            else:
                false_positives += 1

        for label in y_hat[i][1]:
            if label in y[i][1]:
                true_positives += 1
                total_correct += 1
            else:
                false_positives += 1

        # What was not predicted -- FN
        for label in y[i][0]:
            if label not in y_hat[i][0]:
                false_negatives += 1
                total_wrong += 1

        for label in y[i][1]:
            if label not in y_hat[i][1]:
                false_negatives += 1
                total_wrong += 1

        # Check correct positives

    # Precision
    if (false_positives == 0) and (true_positives == 0):
        precision = 0
    else:
        precision = (1.0 * true_positives) / (true_positives + false_positives)

    # Recall
    if (false_negatives == 0) and (true_positives == 0):
        recall = 0.0
    else:
        recall = (1.0 * true_positives) / (true_positives + false_negatives)

    # F-1 score
    if (false_negatives == 0) and (false_positives == 0) and (true_positives == 0):
        f_1_score = 0
    else:
        f_1_score = (2.0 * true_positives) / (2.0 * true_positives + 2.0 * false_positives + 2.0 * false_negatives)

    # Accuracy
    accuracy = (1.0 * total_correct) / (total_wrong + total_correct)

    return precision, recall, f_1_score, accuracy


def main():

    base_dir = 'Apex AD2600 Progressive-scan DVD player'
    output_dir = 'Apex AD2600 Progressive-scan DVD player_output'

    files = helper.get_files(base_dir)

    total_precision = 0
    total_recall = 0
    total_f1_score = 0
    count = 0
    total_accuracy = 0

    for f in files:

        if 'no_label_' not in f:
            continue

        true = f.replace('no_label_', '')
        empirical = os.path.join(output_dir, os.path.basename(f))

        precision, recall, f1, accuracy = score_file(empirical, true)

        if precision is not None:
            count += 1
            total_precision += precision
            total_recall += recall
            total_f1_score += f1
            total_accuracy += accuracy

            print(f, 'Precision: ', precision, 'Recall: ', recall, 'F1', f1, 'accuracy', accuracy)

    pre = total_precision / count
    rec = total_recall / count
    f1s = total_f1_score / count
    acc = total_accuracy / count

    print('\n\nSummary:\n\n')
    print('Precision: ', pre, 'Recall: ', rec, 'F1:', f1s, 'Accuracy: ', acc)

if __name__ == '__main__':
    main()