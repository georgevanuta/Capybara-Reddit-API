import sys

import praw
from prawcore.exceptions import NotFound

import configure

reddit = praw.Reddit(
    user_agent=configure.user_agent,
    client_id=configure.client_id,
    client_secret=configure.client_secret,
    username="",  # not needed
    password=""   # not needed
)

MAX_DIST = 4
REFERENCE = "capybara"

capybara_count = 0


# check for almost capybara words
def hamming_distance(str1, str2):
    length = min(len(str1), len(str2))
    dist = abs(len(str1) - len(str2))

    for i in range(0, length):
        if str1[i] != str2[i]:
            dist += 1

    return dist


# check for any capybara instance in sentence
def any_valid_word(ref, sentence):
    def valid_word(wrd):
        return hamming_distance(ref, wrd) < MAX_DIST

    acc = False

    [acc := acc or valid_word(word) for word in sentence.split()]

    return acc


# check all posts and comments for capybaras
def check_posts(ref, username):
    global capybara_count

    posts = list(reddit.redditor(username).submissions.new())
    comments = list(reddit.redditor(username).comments.new())

    for post in posts:
        if any_valid_word(ref, post.title) or any_valid_word(ref, post.selftext):
            capybara_count += 1

    for comment in comments:
        if any_valid_word(ref, comment.body):
            capybara_count += 1


# error handling for user input
def user_exists(name):
    try:
        reddit.redditor(name).id
    except NotFound:
        return False
    return True


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Please provide a Reddit username.")
        exit(1)

    user = str(sys.argv[1])

    if not user_exists(user):
        print("Please provide a valid Reddit username.")
        exit(1)

    print("Scrapping the posts of the user.....")

    check_posts(REFERENCE, user)

    if capybara_count == 1:
        print("User " + user + " has talked about capybaras " + capybara_count.__str__() + " time!")
    else:
        print("User " + user + " has talked about capybaras " + capybara_count.__str__() + " times!")

