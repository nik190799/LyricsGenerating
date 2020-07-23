import os
import re
from graph import Graph, Vertex
import string
import random


def get_words_from_text(text_path):
    with open(text_path, 'r') as file:
        text = file.read()
        # remove [verse 1: artist]
        text = re.sub(r'\[(.+)\]', ' ', text)
        text = ' '.join(text.split())
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))

    words = text.split()

    return words


def make_graph(words):
    g = Graph()
    prev_word = None
    # for each word
    for word in words:
        # check that word is in graph, and if not then add it
        word_vertex = g.get_vertex(word)

        # if there was a previous word, then add an edge if does not exist
        
        if prev_word:  # prev word should be a Vertex

            prev_word.increment_edge(word_vertex)

        prev_word = word_vertex

    return g


def compose(g, words, length=50):
    composition = []
    word = g.get_vertex(random.choice(words))
    for _ in range(length):
        composition.append(word.value)
        word = random.choice(word.probability_map)

    return composition


def main(artist):
    words = []
    for song in os.listdir('songs/{}'.format(artist)):
        if song == '.DS_Store':
            continue
        words.extend(get_words_from_text('songs/{artist}/{song}'.format(artist=artist, song=song)))

    g = make_graph(words)
    g.generate_probability_mappings()
    composition = compose(g, words, 100)
    print(' '.join(composition))


if __name__ == '__main__':
    main('roddy_ricch')
