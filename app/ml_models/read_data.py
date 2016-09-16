'''
Reads data from sql data base and formats it appropriately before
returning it to main.py which then feeds it to the rest of the model
'''

import os
import re
import logging
from pprint import pprint
import numpy as np
from collections import defaultdict
import nltk.data

from app.database import db_session
from app.models import User, Story, n2nModel

# from app.ml_models.read_data import DataSet


class DataSet(object):
    def __init__(self, batch_size, idxs, xs, qs, ys, vocab_map, vocab_size, include_leftover=False, name=""):
        # assert len(xs) == len(qs) == len(ys), "X, Q, and Y sizes don't match."
        # print "batch size: ", batch_size
        assert batch_size <= len(xs), "batch size cannot be greater than data size."
        self.name = name or "dataset"
        self.idxs = idxs
        print("length of idxs: ",len(idxs))
        self.num_examples = len(idxs)
        self.xs = xs
        self.qs = qs
        self.ys = ys
        self.vocab_map = vocab_map
        self.vocab_size = vocab_size
        self.num_epochs_completed = 0
        self.idx_in_epoch = 0
        self.batch_size = batch_size
        self.include_leftover = include_leftover
        self.num_batches = int(self.num_examples / self.batch_size) + int(include_leftover)
        self.reset()

    def get_next_labeled_batch(self):
        assert self.has_next_batch(), "End of epoch. Call 'complete_epoch()' to reset."
        from_, to = self.idx_in_epoch, self.idx_in_epoch + self.batch_size
        if self.include_leftover and to > self.num_examples:
            to = self.num_examples
        cur_idxs = self.idxs[from_:to]
        xs, qs, ys = zip(*[[self.xs[i], self.qs[i], self.ys[i]] for i in cur_idxs])
        self.idx_in_epoch += self.batch_size
        return xs, qs, ys

    def has_next_batch(self):
        if self.include_leftover:
            return self.idx_in_epoch + 1 < self.num_examples
        return self.idx_in_epoch + self.batch_size <= self.num_examples

    def complete_epoch(self):
        self.reset()
        self.num_epochs_completed += 1

    def reset(self):
        self.idx_in_epoch = 0
        np.random.shuffle(self.idxs)

# TODO : split data into val

def _tokenize_faq(raw_list):
    processed_list = []

    for sent in raw_list:
        tokens = re.findall(r"[\w]+", sent) # finds every word
        normalized_tokens = [token.lower() for token in tokens]
        processed_list.append(normalized_tokens)
    return processed_list

'''
returns list of lists where each list is the tokenized version of a sentence
'''
def _tokenize_story(raw):

    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    story_sentences = sent_detector.tokenize(raw) # returns a list where each element of the list is a story_sentences

    processed_paragraph = []
    for sentence in story_sentences:
        tokens = re.findall(r"[\w]+", sentence) # finds every word
        normalized_tokens = [token.lower() for token in tokens]
        processed_paragraph.append(normalized_tokens)

    return processed_paragraph # list of lists where each list is the tokenized version of a sentence

# _s_re = re.compile("^F:")
# _q_re = re.compile("^Q:")
# _a_re = re.compile("^A:")

'''
called from read_train
defines the vocabulary, paragraphs (x input), questions and answers
'''
def process_input(story_text, faq_text):
    print("story text: ", story_text)

    # need to convert to utf-8 and get rid of new lines
    story_text.decode('utf-8')
    faq_text.decode('utf-8')

    # getting rid of new lines
    story_text = story_text.replace("\n", " ")
    faq_text = faq_text.replace("\n", " ")

    print("story text: ", story_text)
    print("faq_text: ", faq_text)

    vocab_set = set()
    paragraphs = []
    questions = []
    answers = []

    # NOTE will only have 1 paragraph to train on
    # TODO explore loading this model from a pre-trained version?

    # loading the sentences into the single paragraph representation --> paragraph is then re-used as X for every question/answer pair
    paragraph = _tokenize_story(story_text)
    print("paragraph: ", paragraph)
    # deal with FAQ
    # get lists of all the questions and answers (raw text)
    questions_raw = re.findall(r"(?<=Q:).*?(?=A:)", faq_text)
    answers_raw = re.findall(r"(?<=A:).*?(?=Q:|$)", faq_text)

    # tokenize the questions and answers
    questions = _tokenize_faq(questions_raw) # returns list of lists of tokenized questions

    # get list of answers
    for answer in answers_raw:
        vocab_set.add(answer)
        answers.append(answer)

    # build the vocabulary
    for sentence in paragraph:
        for word in sentence:
            vocab_set.add(word)

    for question in questions:
        for word in question:
            vocab_set.add(word)

    print("Loaded %d examples" % (len(questions)))

    return vocab_set, paragraph, questions, answers


def read_train(batch_size, story_text, faq_text):
    # calls read_babi_files
    vocab_set, paragraph, questions, answers = process_input(story_text, faq_text)
    # w2v_dict = w2v_dict[0]

    # need to construct a dictionary of {word: index} and a list of the word vectors as they appear
    vocab_map = {}
    # w2v_vectors = []
    idx_to_word = {}
    for idx, word in enumerate(sorted(vocab_set)):
        vocab_map[word] = idx
        # w2v_vectors.append(w2v_dict[word])
        idx_to_word[idx] = word

    ''' get the index of the word, return index for <UNK> token if word is not in the vocabulary '''
    #TODO add the word vector look ups right here...return the vector instead of the index
    def _get(vm, w): # w = word, vm = vocabulary_map
        if w in vm:
            return vm[w]
        return 0

    ''' this is basically the final step in making the data sets '''
    # TODO word2vec or glove vectors here instead of just indices
    ## Makes the inputs to the networks
    xs_list = [[[[_get(vocab_map, word) for word in sentence] for sentence in paragraph] for i in range(len(questions))]]
    qs_list = [[[_get(vocab_map, word) for word in question] for question in questions]]
    ys_list = [[_get(vocab_map, answer) for answer in answers]]

    print("xs_list: ", xs_list)

    # data sets are now a list of word vectors for the sentences instead of list
    # of indices

    data_sets = [DataSet(batch_size, list(range(len(xs))), xs, qs, ys, vocab_map, len(vocab_map))
                 for xs, qs, ys in zip(xs_list, qs_list, ys_list)]
    print "datasets: ",len(data_sets)
    # just for debugging
    for data_set in data_sets:
        print("adding vocab stuff to the datasets")
        data_set.vocab_map = vocab_map
        data_set.vocab_size = len(vocab_map)

    return data_sets, idx_to_word


'''
called from read_train
defines the vocabulary, paragraphs (x input), questions and answers
'''
def process_input_text(story_text, faq_text, vocab_map, idx_to_word):

    # need to convert to utf-8 and get rid of new lines
    story_text.decode('utf-8')
    faq_text.decode('utf-8')

    # getting rid of new lines
    story_text = story_text.replace("\n", " ")
    faq_text = faq_text.replace("\n", " ")

    paragraphs = []
    questions = []

    # NOTE will only have 1 paragraph to train on
    # TODO explore loading this model from a pre-trained version?

    # loading the sentences into the single paragraph representation --> paragraph is then re-used as X for every question/answer pair
    paragraph = _tokenize_story(story_text)
    print("paragraph: ", paragraph)
    # deal with FAQ
    # get lists of all the questions and answers (raw text)
    questions_raw = re.findall(r"(?<=Q:).*?(?=A:)", faq_text)
    # answers_raw = re.findall(r"(?<=A:).*?(?=Q:|$)", faq_text)

    # tokenize the questions and answers
    questions = _tokenize_faq(questions_raw) # returns list of lists of tokenized questions

    # get list of answers
    # for answer in answers_raw:
    #     answers.append(answer)

    print("Loaded %d examples" % (len(questions)))

    return paragraph, questions


def read_test(batch_size, story_text, faq_text, vocab_map, idx_to_word):
        # calls read_babi_files
        vocab_set, paragraph, questions, answers = process_input_test(story_text, faq_text, vocab_map, idx_to_word)
        # w2v_dict = w2v_dict[0]

        ''' get the index of the word, return index for <UNK> token if word is not in the vocabulary '''
        #TODO add the word vector look ups right here...return the vector instead of the index
        def _get(vm, w): # w = word, vm = vocabulary_map
            if w in vm:
                return vm[w]
            return 0

        ''' this is basically the final step in making the data sets '''
        # TODO word2vec or glove vectors here instead of just indices
        ## Makes the inputs to the networks
        xs_list = [[[[_get(vocab_map, word) for word in sentence] for sentence in paragraph] for i in range(len(questions))]]
        qs_list = [[[_get(vocab_map, word) for word in question] for question in questions]]
        ys_list = [[_get(vocab_map, answer) for answer in answers]]

        # data sets are now a list of word vectors for the sentences instead of list
        # of indices

        data_sets = [DataSet(batch_size, list(range(len(xs))), xs, qs, ys, vocab_map, len(vocab_map))
                     for xs, qs, ys in zip(xs_list, qs_list, ys_list)]
        print "datasets: ",len(data_sets)
        # just for debugging
        for data_set in data_sets:
            print("adding vocab stuff to the datasets")
            data_set.vocab_map = vocab_map
            data_set.vocab_size = len(vocab_map)

        return data_sets, idx_to_word


def split_val(data_set, ratio):
    end_idx = int(data_set.num_examples * (1-ratio))
    left = DataSet(data_set.batch_size, list(range(end_idx)), data_set.xs[:end_idx], data_set.qs[:end_idx], data_set.ys[:end_idx], data_set.vocab_map, data_set.vocab_size)
    right = DataSet(data_set.batch_size, list(range(len(data_set.xs) - end_idx)), data_set.xs[end_idx:], data_set.qs[end_idx:], data_set.ys[end_idx:],data_set.vocab_map, data_set.vocab_size)
    return left, right


def get_max_sizes(*data_sets):
    max_sent_size = max(len(s) for ds in data_sets for idx in ds.idxs for s in ds.xs[idx])
    max_ques_size = max(len(ds.qs[idx]) for ds in data_sets for idx in ds.idxs)
    return max_sent_size, max_ques_size


if __name__ == "__main__":
    train, test = read_babi(1, "data/tasks_1-20_v1-2/en", 1)
    # print train.vocab_size, train.max_m_len, train.max_s_len, train.max_q_len
    # print test.vocab_size, test.max_m_len, test.max_s_len, test.max_q_len
    x_batch, q_batch, y_batch = train.get_next_labeled_batch()
    max_sent_size, max_ques_size = get_max_sizes(train, test)
    print(max_sent_size, max_ques_size)
# print x_batch
