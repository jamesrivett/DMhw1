# CS4412 : Data Mining
# Summer 2022
# Kennesaw State University
# Homework 1

# module for reading csv files
import csv

def read_csv_file(filename):
    """this function reads a .CSV file, and returns the dataset as a list"""
    with open(filename,'r') as f:
        reader = csv.reader(f,delimiter=',', quotechar='"')
        dataset = [ line for line in reader ]
    return dataset

# read the datasets from file
movie_data = read_csv_file("data/movies.csv")
rating_data = read_csv_file("data/ratings.csv")

# skip the headers in the datasets
movie_data = movie_data[1:]
rating_data = rating_data[1:]

# produce a map from movie_id to the movie's title
movie_titles = dict()
for movie in movie_data:
    # each line in the dataset has an ID, title, and list of genre's
    movie_id,title,genres = movie
    movie_titles[movie_id] = title

# produce a map from movie_id to the movie's genres
movie_genres = dict()
for movie in movie_data:
    movie_id,title,genres = movie
    # the list of genre is seperated by a | character
    genres = genres.split('|')
    movie_genres[movie_id] = genres

# next, we compute the average rating for each movie
# first, initialize counts and sums
counts = dict()  # number of ratings
sums = dict()    # sum of all ratings
for rating in rating_data:
    # each line in the dataset has a user-ID, movie-ID, score, and timestamp
    user_id,movie_id,score,timestamp = rating
    counts[movie_id] = 0
    sums[movie_id] = 0

# count and sum the ratings for each movie
for rating in rating_data:
    user_id,movie_id,score,timestamp = rating
    # in the dataset, all fields are strings, so convert the score to
    # a floating-point number first when we compute the average rating
    score = float(score)
    counts[movie_id] += 1
    sums[movie_id] += score

# compute the averages from the counts and sums
stats = dict()
min_ratings = 100
genre = "Comedy"
for movie_id in counts:
    if counts[movie_id] < min_ratings: continue
    if genre not in movie_genres[movie_id]: continue
    average = sums[movie_id]/counts[movie_id]
    # each stat entry has the movie id, the average rating, and #-of-ratings
    stats[movie_id] = (movie_id,average,counts[movie_id])

# sort the list of ratings
key_function = lambda x: x[1] # given x, return x[1]
ranking = list(stats.values())
ranking.sort(key=key_function,reverse=True)

# print the top-10 movies
print("============================================")
print("== Top 10 %s movies with at least %d ratings" % (genre,min_ratings))
print("============================================")
for line in ranking[:10]:
    # each stat entry has the movie id, the average rating, and #-of-ratings
    movie_id,average,count = line
    movie_title = movie_titles[movie_id]
    print('%40s: %.2f (%d ratings)' % (movie_title[:40],average,count))
