# import the Chat class from nltk
from nltk.chat.util import Chat

# reflections to reply as 1st person
ref = {
        "i am": "you are",
        "i was": "you were",
        "i": "you",
        "i'm": "you are",
        "i'd": "you would",
        "i've": "you have",
        "i'll": "you will",
        "my": "your",
        "you are": "I am",
        "you were": "I was",
        "you've": "I have",
        "you'll": "I will",
        "your": "my",
        "yours": "mine",
        "you": "me",
        "me": "you",
      }

# some pre difned question answer pairs
pairs = [
            [
                r"my name is (.*)",
                ["Hello %1, How u doing today..."]
            ],
            [
                r"(.*) your name",
                ["My name's Sam","You can call me Sam","Well, my friends address me as Sam"]
            ],
            [
                r"(.*) my name",
                ["I'm so sorry, i just forgot your name :(","So sorryyyy, would you please tell me your name again"]
            ],
            [
                r"(.*) doing",
                ["I'm doing absolutely fine","I am not doing so good","Ya, you can say, I an fine"]
            ],
            [
                r"(.*) happened (.*)",
                ["Nothing much, just a bit off..."]
            ],
            [
                r"sorry (.*)",
                ["Its alright","Its OK, never mind"]
            ],
            [
                r"hi|hey|hello",
                ["Hello", "Hey there"]
            ],
            [
                r"(.*) age",
                ["Seriously dude, I'm just a software","Oh my Gosh, r u seriously asking me this"]
            ],
            [
                r"(.*) (want|wants)",
                ["Make me an offer I can't refuse"]
            ],
            [
                r"(.*) (created u|creator)",
                ["Sarthak is the man who created me","I was created by Sarthak Gupta"]
            ],
            [
                r"(.*) (live|location)",
                ["Come on dude, It's a computer program","Oh man, I am a software situated in your computer memory...","Damn it man, r u seriously asking me this"]
            ],
            [
                r"(.*) yes (.*)",
                ["Then, I'm extremely sorry, I cannot answer that!!!","You look so high buddy, get to your home and have tight sleep","Hey bro, please drink less next time"]
            ],
            [
                r"(.*) weather (in|at) (.*)",
                ["Weather in %2 is awesome like always","Too hot man here in %2","Too cold man here in %2","Never even heard about %2"]
            ],
            [
                r"i work (in|at) (.*)",
                ["I haven't heard about that firm before...","Well, you know %1 is the best firm right now...","%1 is a good firm, but I personally suggest you to switch on your job..."]
            ],
            [
                r"(.*)raining in (.*)",
                ["No rain since last week here in %2","Damn its raining too much here in %2"]
            ],
            [
                r"how (.*) health(.*)",
                ["I'm a computer program, so I'm always healthy "]
            ],
            [
                r"(.*) (sports|game) ?",
                ["I'm a very big fan of Football"]
            ],
            [
                r"who (.*) sportsperson ?",
                ["Messy","Ronaldo","Roony"]
            ],
            [
                r"who (.*) (moviestar|actor)?",
                ["Brad Pitt"]
            ],
            [
                r"quit",
                ["BBye take care. See you soon :) ","It was nice talking to you. See you soon :)"]
            ]
        ]

# function chatty to converse with the user
def chatty():
    # some starting lines
    print("Hi, I'm Chatty and I chat alot ;)\nPlease type lowercase English language to start a conversation. Type quit to leave ")
    
    # create object for the Chat class
    chat = Chat(pairs, ref)

    # use the pre-defined converse function to chat
    chat.converse()

# main function
if __name__ == "__main__":
    # call the chatty function here
    chatty()
