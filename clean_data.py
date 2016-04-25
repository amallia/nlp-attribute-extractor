import os
import helper


class Review(object):

    def __init__(self, title):
        self.title = title
        self.samples = []

    def __str__(self):
        return '\n' + str(self.title) + '\n' + str(self.samples) + '\n'


def process_file(f):

    reviews = []
    review = None

    for line in open(f, 'r'):

        line = line.replace('\r\n', '').strip()

        # print(line)

        if (line is None) or (len(line) == 0):
            continue

        if line[0] == '*':
            continue

        # Read title
        if line.startswith('[t]'):

            if review is not None:
                reviews.append(review)

            title = line.replace('[t]', '').strip()
            review = Review(title)

            continue

        parts = line.split('##')

        pos_features = []
        neg_features = []

        # Read features
        if len(parts) > 1 and len(parts[0]) > 0:
            features = parts[0]

            # Read into single features, build dictionary
            for feature in [x.strip() for x in features.split(',')]:

                # Split with []

                feature_splits = feature.split('[')

                feature_name = feature_splits[0]

                feature_score = feature_splits[1].split(']')[0]

                if int(feature_score) > 0:
                    pos_features.append(feature_name)
                else:
                    neg_features.append(feature_name)

        if review is not None:

            review_line = parts[-1].strip()
            if review_line[-1] not in ['.', '!', '?']:
                review_line = review_line[:-1] + '.'

            review.samples.append((pos_features, neg_features, review_line))

    return reviews


def generate_data(f, reviews):

    count = 1

    dir_name = helper.get_name_without_extension( os.path.basename(f) )
    helper.ensure_dir(dir_name)

    for review in reviews:

        # Without labels
        target_path = os.path.join(dir_name, 'no_label_' + str(count) + '.txt')
        helper.save_list_to_file(target_path, [x[2] for x in review.samples])

        # With labels
        target_path = os.path.join(dir_name, str(count) + '.txt')
        data = [','.join(x[0]) + ' | ' + ','.join(x[1]) + ' | ' + x[2] for x in review.samples]
        helper.save_list_to_file(target_path, data)

        count += 1




def main():

    files = helper.get_files('customer review data')

    for f in files:
        reviews = process_file(f)
        generate_data(f, reviews)
        break

    pass


if __name__ == '__main__':
    main()

