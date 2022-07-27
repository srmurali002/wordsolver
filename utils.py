import numpy as np
import nltk

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag

def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'

    if tag.startswith('V'):
        return 'v'

    if tag.startswith('J'):
        return 'a'

    if tag.startswith('R'):
        return 'r'

    return None

def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None

    try:
        return wordnet.synsets(word, wn_tag)[0]
    except:
        return None

def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))

    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]

    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]

    score, count = 0.0, 0

    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        best_score = max([synset.path_similarity(ss) for ss in synsets2])

        # Check that the similarity could have been computed
        if best_score is not None:
            score += best_score
            count += 1

    # Average the values
    score /= count
    return score


def searcher(masked, meaning, sim_thr = 0.8):

    wlist = [ n for n in wordnet.all_lemma_names() if (len(n) == len(masked))]

    words = [n for n in wlist if len(n) == len(masked)]

    def ord_list(word): return [ord(c) for c in list(word)]

    diffs = []

    no_chars = sum([int(c.isalpha()) for c in masked])

    for word in words:
        diffs.append([i-j for i,j in zip(ord_list(masked),ord_list(word))])

    diffs = np.array(diffs)
    ids = np.argwhere(np.count_nonzero(diffs==0, axis=1) == no_chars).ravel()

    search_result = [words[i] for i in ids]

    max_prob = []
    for item in search_result:
      word = item
      syns = wordnet.synsets(word)
      syn_wor_list = np.array([syn.name().split(".")[0].replace('_',' ') for syn in syns])
      ids = np.argwhere(syn_wor_list == word).ravel()
      for i in ids:
        defin = syns[i].definition()
        if defin:
          if sentence_similarity(defin,meaning) >= sim_thr:
            max_prob.append(item)

    return list(set(max_prob))
