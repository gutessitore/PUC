import json
import string
import nltk
from TriesWithFrequencies.TriesWithFrequencies import *
from nltk.corpus import stopwords
from nltk.util import ngrams

# Baixando as stopwords
nltk.download('stopwords')

# Lista de stopwords em português
stopwords_pt = stopwords.words('portuguese')

text = open('blogdosvinhos.txt', encoding='utf-8').read()
text = text.lower()

# Remove pontuação
translator = str.maketrans('', '', string.punctuation)
text = text.translate(translator)

word_list = text.split()

# Remove stopwords
word_list = [word for word in word_list if word not in stopwords_pt]

# Escolha o valor de 'n' para os n-grams
n = 2

# Cria os n-grams
n_grams = list(ngrams(word_list, n))
n_grams = [' '.join(gram) for gram in n_grams]

# Agora, 'word_list' contém as palavras do texto, todas em minúsculas,
# sem pontuação e sem stopwords.


tr = trie_create(word_list, verify_input=False)
ptr = trie_node_probabilities(tr)
trie_form(trie_shrink(ptr))
# classified = trie_classify(ptr, list("u"), prop="Probabilities")
# print(json.dumps(classified, indent=4, ensure_ascii=False))
