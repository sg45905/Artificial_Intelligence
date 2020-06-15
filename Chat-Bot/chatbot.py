import re
import sqlite3
from collections import Counter
from string import punctuation
from math import sqrt

# create connection to the database
connection = sqlite3.connect('chatbot.sqlite')
cursor = connection.cursor()

# create tables
create_table_request_list = [
    'CREATE TABLE words(word TEXT UNIQUE)',
    'CREATE TABLE sentences(sentence TEXT UNIQUE,used INT NOT NULL DEFAULT 0)',
    'CREATE TABLE associations(word_id INT NOT NULL,sentence_id INT NOT NULL,weight REAL NOT NULL)',
]

for create_table_request in create_table_request_list:
    try:
        cursor.execute(create_table_request)
    except:
        pass

# Retrieve entity - word or sentence
def get_id(entityName, text):
    tableName = entityName + 's'
    columnName = entityName
    cursor.execute('SELECT rowid FROM ' + tableName + ' WHERE ' + columnName + ' = ?', (text,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        cursor.execute('INSERT INTO ' + tableName + ' (' + columnName + ') VALUES (?)', (text,))
        return cursor.lastrowid

# Retrieve word - in tuple form - (word,count(word))
def get_words(text):
    wordsRegexpString = '(?:\w+|[' + re.escape(punctuation) + ']+)'
    wordsRegexp = re.compile(wordsRegexpString)
    wordsList = wordsRegexp.findall(text.lower())
    return Counter(wordsList).items()

# run until user quits - it uses NLP to reply to the users' questions

'''
This program uses the occurance frequency of the words in a sentence 
(or say, reply from the user), to analyse and interpret the answer that
should be given to the user
'''

bot = 'Hello!'
while True:
    print('Bot: ' + bot)
    usr = input('Usr: ').strip()
    if usr == '':
        print('Bot: it was noce talking to you, goodbye!!')
        break
    words = get_words(bot)
    words_length = sum([n * len(word) for word, n in words])
    sentence_id = get_id('sentence',usr)
    for word,n in words:
        word_id = get_id('word',word)
        weight = sqrt(n/float(words_length))
        cursor.execute('INSERT INTO associations VALUES (?,?,?)',(word_id,sentence_id,weight))
    connection.commit()
    cursor.execute('CREATE TEMPORARY TABLE results(sentence_id INT, sentence TEXT, weight REAL)')
    words = get_words(usr)
    words_length = sum([n * len(word) for word, n in words])
    for word,n in words:
        weight = sqrt(n / float(words_length))
        cursor.execute('INSERT INTO results SELECT associations.sentence_id,sentences.sentence,?*associations.weight/(4+sentences.used) FROM words INNER JOIN associations ON associations.word_id=words.rowid INNER JOIN sentences ON sentences.rowid=associations.sentence_id WHERE words.word=?',(weight, word,))
    cursor.execute('SELECT sentence_id,sentence,SUM(weight) AS sum_weight FROM results GROUP BY sentence_id ORDER BY sum_weight DESC LIMIT 1')
    row = cursor.fetchone()
    cursor.execute('DROP TABLE results')
    if row is None:
        cursor.execute('SELECT rowid,sentence FROM sentences WHERE used=(SELECT MIN(used) FROM sentences) ORDER BY RANDOM() LIMIT 1')
        row = cursor.fetchone()
    bot = row[1]
    cursor.execute('UPDATE sentences SET used=used+1 WHERE rowid=?',(row[0],))
