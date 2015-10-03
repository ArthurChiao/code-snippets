import math
import pprint

from Database import *

def similarity_distance(ratings, user1, user2):
    '''
    @param ratings - rating matrix
    @param user1 - name of user1
    @param user2 - name of user2
    @return normalized similarity distance
    '''
    movies = set(map(lambda l: l[1], ratings.keys())) # extract movie names
    conjunct_movies = list(filter(lambda l:
            (user1, l) in ratings and ratings[(user1, l)] != "" and
            (user2, l) in ratings and ratings[(user2, l)] != "", movies))

    if len(conjunct_movies) == 0:
        return 0

    distances = [pow(float(ratings[(user1, m)]) - float(ratings[(user2, m)]), 2) for m in conjunct_movies]
    return 1 / (1 + math.sqrt(sum(distances)))

if __name__ == '__main__':
    ratings = load_file()
    sim = similarity_distance(ratings, 'User1', 'User2')
    print(sim)
