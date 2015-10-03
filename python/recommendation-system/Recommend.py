import pprint as pp

from Database import *
from Similarity import *

def calc_similarities(ratings, user, similarity=similarity_distance):
    '''
    calculate the specified user's similarity with all the other users

    @param ratings - rating matrix: USER (vertical) x MOVIE (horizontal)
    @param user    - specified user
    @param similarity - similarity distance function
    @return (similarity_value, with_which_user) list
    '''
    users = set(map(lambda l: l[0], ratings.keys()))

    sims = [(similarity(ratings, user, u), u) for u in users if u != user]
    sims.sort()    # smallest first
    sims.reverse() # biggest first

    print("SIMILARITY list for " + user + ": ")
    pp.pprint(sims)
    return sims

def get_recommendations(ratings, user, similarity=similarity_distance):
    '''
    predict the given user's likeness on each movie by his/her similarity with
    other users and the ratings rated by other users

    @param ratings - rating matrix: USER (vertical) x MOVIE (horizontal)
    @param user    - specified user
    @param similarity - similarity distance function
    @return (score, movie) list which represents the user's likeness on each
    moview, note that the score is normalized to [0.0, 1.0]
    '''
    users  = set(map(lambda l: l[0], ratings.keys()))
    movies = set(map(lambda l: l[1], ratings.keys()))

    # similarity and normalized score on each movie
    # sum over all the other users in our system
    sim_on_movie = {}
    score_on_movie = {}
    for u in users:
        if u == user:
            continue

        sim = similarity_distance(ratings, user, u)
        if sim <= 0:
            continue

        for m in movies:
            if ratings[(u, m)] == "":
                continue

            sim_on_movie.setdefault(m, 0)
            sim_on_movie[m] += sim
            score_on_movie.setdefault(m, 0)
            score_on_movie[m] += float(ratings[u, m]) * sim

    # final weighted likeness on each movie
    likeness = [(sim_on_movie[m] / score_on_movie[m], m) for m in movies]
    likeness.sort()
    likeness.reverse()

    print("predicted LIKENESS list for " + user + ": ")
    pp.pprint(likeness)
    return likeness

if __name__ == '__main__':
    ratings = load_file()

    # calculate the similarity with the other users
    calc_similarities(ratings, 'User1', similarity_distance)

    # predict the likeness on each movie by using other users' ratings
    likeness = get_recommendations(ratings, 'User1', similarity_distance)
