import pickle, os, argparse

parser = argparse.ArgumentParser(description='BiLSTM-CRF for Chinese NER task')
parser.add_argument('--corpus_path', type=str, default='data_path')
parser.add_argument('--vocab_path', type=str, default='data_path')
parser.add_argument('--min_count', type=int, default=0)
args = parser.parse_args()

corpus_path = os.path.join('.', args.corpus_path, 'corpus_data')
vocab_path = os.path.join('.', args.vocab_path,  'word2id.pkl')
min_count = args.min_count

def read_corpus(corpus_path):
    """
    read corpus and return the list of samples
    :param corpus_path:
    :return: data
    """
    data = []
    with open(corpus_path, encoding='utf-8') as fr:
        lines = fr.readlines()
    sent_ = []
    for line in lines:
        for word in line.strip().split(' '):
            if word != '\n':
                sent_.append(word)
                data.append(sent_)
            else:
                data.append(sent_)
                sent_= []
    # print(sent_)
    return data


def vocab_build(vocab_path, corpus_path, min_count):
    """

    :param vocab_path:
    :param corpus_path:
    :param min_count:
    :return:
    """
    data = read_corpus(corpus_path) 
    word2id = {}
    for sent_ in data:
        #print(sent_)
        for word in sent_:
            if word.isdigit():
                word = '<NUM>'
            elif ('\u0041' <= word <='\u005a') or ('\u0061' <= word <='\u007a'):
                word = '<ENG>'
            if word not in word2id:
                word2id[word] = [len(word2id)+1, 1]
            else:
                word2id[word][1] += 1
    low_freq_words = []
    for word, [word_id, word_freq] in word2id.items():
        if word_freq < min_count and word != '<NUM>' and word != '<ENG>':
            low_freq_words.append(word)
    for word in low_freq_words:
        del word2id[word]

    new_id = 1
    for word in word2id.keys():
        word2id[word] = new_id
        new_id += 1
    word2id['<UNK>'] = new_id
    word2id['<PAD>'] = 0

    print(word2id)
    with open(vocab_path, 'wb') as fw:
        pickle.dump(word2id, fw)

vocab_build(vocab_path, corpus_path, min_count)