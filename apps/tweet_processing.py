import spacy
from spacy.matcher import Matcher
from operator import methodcaller
import re

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)


def find_hash_tags(text):
    """
    :return:
    """

    doc = nlp(text)
    hashtag = [{'ORTH': '#'}, {'IS_ASCII': True}]
    matcher.add("HashTags", None, hashtag)
    matches = matcher(doc)
    hastag_collector = []
    for match_id, start, end in matches:
        hashtag_info = {}
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]
        # The matched span
        hashtag_info['index'] = [start, end]
        hashtag_info['text'] = span.text
        hastag_collector.append(span.text)
        print(match_id, string_id, start, end, span.text)
    return ",".join(hastag_collector)


def remove_stop_words(text):
    """
    :param str:
    :return:
    """
    doc = nlp(text)
    tokens = [token.text for token in doc if not token.is_stop]
    return " ".join(tokens)


def clean_text(text):
    """
    :param text:
    :return: string
    """
    # hashtag_re = re.compile("(?:^|\s)[＃#]{1}(\w+)", re.UNICODE)
    # mention_re = re.compile("(?:^|\s)[＠ @]{1}([^\s#<>[\]|{}]+)", re.UNICODE)
    # remove special charcters
    pattern = r"[-()\"#/@;:<>{}`+=~|.!?,]"
    new_ = re.sub(pattern, '', text)
    # replace unicode charcters
    new_ = re.sub(r'[^\x00-\x7F]+', '', new_)
    # remove link elements
    new_ = re.sub(r'http\S+', '', new_)
    return new_


def tweet_extractor(text):
    """
    labels : WORK_OF_ART,ORG,GPE,LOC,PRODUCT,EVENT
    :param
    """
    doc = nlp(text)
    label_list = {
        "WORK_OF_ART": {"label": "WORK_OF_ART", "emoji": "🎭"},
        "ORG": {"label": "ORG", "emoji": "🏢"},
        "GPE": {"label": "GPE", "emoji": "🗺️"},
        "LOC": {"label": "LOC", "emoji": "🌄"},
        "PRODUCT": {"label": "PRODUCT", "emoji": "🎁"},
        "EVENT": {"label": "EVENT", "emoji": "🙌"},
        "PERSON": {"label": "PERSON", "emoji": "👫"}
    }

    inline_ = [{"tag": label_list.get(each.label_).get('label'),
                "text": each.text,
                "emoji": label_list.get(each.label_).get('emoji')
                } for each in doc.ents if each.label_ in label_list.keys()]

    tags = ["dobj", "pobj", "iobj", "nsubj", "ROOT", "compound"]

    phrases = [each.text for each in doc if
               each.dep_ in tags and (each.head.pos_ in ['VERB', 'NOUN'] and each.pos_ not in ['PRON'])]

    # return {
    #     "entities": inline_,
    #     "words": phrases
    # }

    #return (' ').join(phrases)
    return {
        "entities": inline_,
        "words": phrases,
        "text":text
    }

if __name__ == '__main__':
    text = "First lady Melania #Trump visits infant opioid #treatment center in Huntington, West Virginia.  We love your grace and style @ FLOTUS! ❤️❤️ https://t.co/hLAKPSOro6"
    list_ = [text]
    a = clean_text(text)

    tweet_extractor(a)
    print(a)

