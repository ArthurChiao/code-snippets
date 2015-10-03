import pprint

def load_file():
    '''
    load csv (comma-seperated-value) format rating data

    @return a rating database which stores all the ratings for all movies from
    all users in system
    '''
    db = {} # rating database of all users
            # key: (user, movie); value: the user's rating on that movie

    f = open("train-data.csv")
    movies = [m.strip() for m in f.readline().split(",")] # movie names

    for line in f: # remaining lines, rating data
        ratings = [r.strip() for r in line.split(',')] # rating on each movie
        user = ratings[0]                              # user name
        for i in range(len(ratings))[1:]:
            db[(user, movies[i])] = ratings[i]

    #print(db)
    return db

def reorder_rating_key(rating_db):
    '''
    reorder rating matrix key
    '''
    rows = set(map(lambda l: l[0], rating_db.keys())) # users
    cols = set(map(lambda l: l[1], rating_db.keys())) # movies

    new_matrix = {}
    for r in rows:
        for c in cols:
            new_matrix[(c, r)] = rating_db[(r, c)]
    return new_matrix


if __name__ == '__main__':
    rating_db = load_file()
    print("original rating_db: ")
    pprint.pprint(rating_db)

    key = ('User1', 'Alvin and the Chipmunks')
    print(('User1', 'Alvin and the Chipmunks') in rating_db)
    print(key in rating_db)

    # new_matrix_matrix = reorder_rating_key(rating_db)
    # print("\nnew_matrix rating_db: ")
    # pprint.pprint(new_matrix_matrix)

