import requests
import json
import os

# Get TMDb API key from environment variable

# To set API key in terminal session: 
# export TMDB_API_KEY="your_tmdb_api_key"

# To make permanent: 
# echo 'export TMDB_API_KEY="your_tmdb_api_key"' >> ~/.bashrc
# source ~/.bashrc

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY environment variable not set")

def get_top_titles(platform, media_type="movie", min_rating=8.0, max_results=10):
    url = f"https://api.themoviedb.org/3/discover/{media_type}"
    params = {
        "api_key": TMDB_API_KEY,
        "with_watch_providers": platform,
        "watch_region": "US",
        "sort_by": "vote_average.desc",
        "vote_count.gte": 100,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("results", [])
        return [
            {"title": item.get("title") or item.get("name"), "rating": item["vote_average"]}
            for item in results if item["vote_average"] >= min_rating
        ][:max_results]
    else:
        print(f"Error fetching data for platform {platform}: {response.status_code}")
        return []

def filter_watched_titles(titles, watched):
    return [title for title in titles if title["title"] not in watched]

def save_watched_titles(watched_titles, filename="watched_titles.json"):
    with open(filename, "w") as file:
        json.dump(list(watched_titles), file)

def load_watched_titles(filename="watched_titles.json"):
    try:
        with open(filename, "r") as file:
            return set(json.load(file))
    except FileNotFoundError:
        return set()

def main():
    # Load watched titles from JSON file
    watched_titles = load_watched_titles()

    platforms = {
        "8": "Netflix",
        "384": "HBO Max",
        "337": "Disney+"
    }

    netflix_movies = []
    hbo_movies = []
    disney_movies = []

    netflix_shows = []
    hbo_shows = []
    disney_shows = []

    #Checking if user wants to see top movies
    want_to_see_movies = input("Do you want to see top movies? (y/n): ")

    if want_to_see_movies == 'y':
        which_service = input("Which service do you want to see top movies from? (Netflix, HBO, Disney, All): ")
        if 'Netflix' in which_service:
            print(f"Fetching Top Movies from: Netflix...")
            netflix_movies = get_top_titles("8", media_type="movie")

            #Filtering netflix movies from already watched movies
            filtered_netflix_movies = filter_watched_titles(netflix_movies, watched_titles)

            print("\nTop Movies on Netflix (Filtered):")
            for title in filtered_netflix_movies:
                print(f"{title['title']} - Rating: {title['rating']}")

        elif 'HBO' in which_service:
            print(f"Fetching Top Movies from: HBO Max...")
            hbo_movies = get_top_titles("384", media_type="movie")

            #Filtering hbo movies from already watched movies
            filtered_hbo_movies = filter_watched_titles(hbo_movies, watched_titles)

            print("\nTop Movies on HBO Max (Filtered):")
            for title in filtered_hbo_movies:
                print(f"{title['title']} - Rating: {title['rating']}")

        elif 'Disney' in which_service:
            print(f"Fetching Top Movies from: Disney+...")
            disney_movies = get_top_titles("337", media_type="movie")

            #Filtering disney movies from already watched movies
            filtered_disney_movies = filter_watched_titles(disney_movies, watched_titles)

            print("\nTop Movies on Disney+ (Filtered):")
            for title in filtered_disney_movies:
                print(f"{title['title']} - Rating: {title['rating']}")

        elif which_service == 'All':
            print(f"Fetching Top Movies from all services...")
            netflix_movies = get_top_titles("8", media_type="movie")
            hbo_movies = get_top_titles("384", media_type="movie")
            disney_movies = get_top_titles("337", media_type="movie")
            filtered_netflix_movies = filter_watched_titles(netflix_movies, watched_titles)
            filtered_hbo_movies = filter_watched_titles(hbo_movies, watched_titles)
            filtered_disney_movies = filter_watched_titles(disney_movies, watched_titles)
        else:
            if 'All' in which_service and which_service != 'All':
                print("Cannot include 'All' in service name, if including other services. Must be 'All' or a list of specific services.")
            else:
                print("Invalid input. Please try again.")

    want_to_see_shows = input("Do you want to see top TV shows too? (y/n): ")
    if want_to_see_shows == 'y':
        which_service = input("Which service do you want to see top TV shows from? (Netflix, HBO Max, Disney+): ")
        if 'Netflix' in which_service:
            print(f"Fetching Top TV Shows from: Netflix...")
            netflix_shows = get_top_titles("8", media_type="tv")
            filtered_netflix_shows = filter_watched_titles(netflix_shows, watched_titles)
        elif 'HBO Max' in which_service:
            print(f"Fetching Top TV Shows from: HBO Max...")
            hbo_shows = get_top_titles("384", media_type="tv")
            filtered_hbo_shows = filter_watched_titles(hbo_shows, watched_titles)
        elif 'Disney+' in which_service:
            print(f"Fetching Top TV Shows from: Disney+...")
            disney_shows = get_top_titles("337", media_type="tv")
            filtered_disney_shows = filter_watched_titles(disney_shows, watched_titles)
        elif which_service == 'All':
            print(f"Fetching Top TV Shows from all services...")
            netflix_shows = get_top_titles("8", media_type="tv")
            hbo_shows = get_top_titles("384", media_type="tv")
            disney_shows = get_top_titles("337", media_type="tv")
            filtered_netflix_shows = filter_watched_titles(netflix_shows, watched_titles)
        else:
            if 'All' in which_service and which_service != 'All':
                print("Cannot include 'All' in service name, if including other services. Must be 'All' or a list of specific services.")
            else:
                print("Invalid input. Please try again.")

        

    # want_to_see_shows = input("Do you want to see top TV shows too? (y/n): ")
    # if want_to_see_shows == 'y':
    #     for platform_id, platform_name in platforms.items():
    #         print(f"Top TV Shows from: {platform_name}...")
    #         shows = get_top_titles(platform_id, media_type="tv")
    #         show_titles.extend(shows)

    
    # Display results
    print("\nTop Movies and TV Shows (Filtered):")
    for title in filtered_titles:
        print(f"{title['title']} - Rating: {title['rating']}")

    # Allow user to mark titles as watched
    newly_watched = []
    print("\nWould you like to mark any of these as watched? (Type the title to mark it, or press Enter to skip)")
    for title in filtered_titles:
        user_input = input(f"Mark '{title['title']}' as watched? (y/n): ").strip().lower()
        if user_input == 'y':
            newly_watched.append(title["title"])

    # Update and save watched titles
    watched_titles.update(newly_watched)
    save_watched_titles(watched_titles)

    print("\nUpdated watched titles saved.")

if __name__ == "__main__":
    main()
