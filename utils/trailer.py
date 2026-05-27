import webbrowser

def open_trailer(movie_name):
    query = movie_name.replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={query}+official+trailer"
    webbrowser.open(url)