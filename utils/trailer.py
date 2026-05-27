def watch_trailer(movie_name):

    query = movie_name.replace(" ", "+")

    url = f"https://www.youtube.com/results?search_query={query}+trailer"

    return url