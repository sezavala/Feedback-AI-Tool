import json

text = """About the Project
Sonarr is a "Personal Video Recorder" for Usenet and BitTorrent users. It's an app that scours the internet or monitors multiple RSS feeds for links to download your desired media. It can scan your media files and check if you're missing any episodes of a particular season of TV shows or Anime, rename them according to an accepted standard or even be configured to automatically download and replace them with a higher desired quality.
The app grabs media information from popular database sites like Tvdb and Imdb and uses that information to organize it. This can help users stay up to date on their favorite shows and make it easier to organize them. If set up correctly by the user, it's almost a hands-off maintenance of your media files. And it’s not just for personal use, if you host a large media server that many people have access to, or you provide a service to, this should provide the host with less headaches. A quality-of-life app for these users with a large media library that they would want to manage.
Example usage:
1.) Homepage: localhost:8989 (since I’m using this as a personal use app)

2.) Media page.

3.) Searching for results. If searching for a season, it can take a while as it’s searching for each episode as well as the season packs.

4.) Search results. Or just one result for this series. Here, it took me about 5 minutes to produce the results.


5.) Click the button on the right to start the download. Provided that you set up Sonarr correctly, the app will initialize the download with your favorite torrent app.
The Issue
Anime Standard Format Search (allow search by seasons) #5616. For some indexers, with the option of “Anime Standard Format Search” on, season packs for anime will not show up. For indexers that are reasonably competent or specialized in the Anime category, this is not a problem, season packs do show up. The issue arises for indexers that are more general in content (but still have some anime), season packs will not show up for anime search queries.
This is a quality-of-life issue, and QOL patches are always welcomed, never scorned. Our patch can make Sonarr easier and more user-friendly for Anime fans. This is just an overall improvement on the user experience with this app, increasing the user base.
Where to start:
Here is the issue we’re trying to fix. Let us search for the Anime, One Punch Man, season 1. These are the results before our changes.

To peek into the future, before explaining the final solution, these are the results after our changes. We’re able to get 4 additional results that are valid.

Through the search feature of the IDE, we were able to find some functions related to the “anime” query in several files. Then we found an object called AnimeEpisodeSearchCriteria. Then we used the search function again for said object. A couple of functions stood out to us.

The function shown above was found in the file, ReleaseSearchService.cs. While exploring the file, just a bit below the function SearchAnime, there was SearchAnimeSeason.

Codebase Overview
Tech Stacks:

System diagram:

Flow of Control:
1.) We’ll start with the homepage shown here.

2.) Let’s look at One Punch Man’s media page.

3.) When that button is clicked, an app call is made by the front-end. That call is then received by the back-end, which analyzes the request. Eventually, it reaches here, the function SearchAnimeSeason(), called in the ReleaseSearchService.cs file.

Judging from its code, it just searches for every episode in the season, no specific season pack search.
4.) With the function above, it will identify what indexer Sonarr is using, and eventually reach this function, GetSearchRequests().

From the SearchAnimeSeason function, the GetSearchRequests function is called for each episode.
5.) After the functions have finished running, we’ll get our search results for One Punch Man here.

Challenges
One of the technical challenges we faced was finding a good way to test our code changes. Previously, when we were just confirming the, at the time, the current behavior of the app, we found no difference when the “Anime Standard Format Search” option was on or off.
Since the issue was not getting season packs for anime, we assumed that when searching for individual episodes, the desired behavior was for season packs to show up as well that contained that individual episode. Another possible solution that we thought of was when a full season search is performed, on the first episode, look for season packs as well. Lastly, we had the idea to add another episode to search for that episode object that would have all the same parameters as the first episode, but instead only search for the season packs, ignoring any mention of the first “episode”.
I made inquiries with the project maintainer about it, and it turns out that none of those was the desired solution. Referring to our first assumption, the indexer that we were using to test search results was too capable of an Anime indexer. He suggested using Prowlarr, another project from the same developers of Sonarr, to add generic, general content indexers. As for our second assumption, the project maintainer wanted a separate search done, not pairing it with the first episode search. That leads to our third assumption. While we were able to do a separate search, we were still using the “AnimeEpisodeSearchCriteria” object, but the project maintainer wanted a separate object to conduct the season search called “AnimeSeasonSearchCriteria” instead. After all those inquiries about the desired solution, we finally came to our final solution.
First attempt:
We made only one code change here, and that was to search for season packs on every episode.

Here’s the console of what’s going on for our first attempt. First, let’s look at the original behavior in the console before we started working on the issue.

Now here, we saw our changes working, only, it’s working too much.

Second attempt, trying to search only once:
To make it so that we only search for season packs only once, we needed to add a flag in the existing object, “AnimeEpisodeSearchCriteria”.

Then we use that flag to detect the first episode.


With that flag, we made it so that when the searchCriteria object is on its first episode, run a season search.

Here’s the console for our second attempt.

Third attempt:
We kept the flags, we added a new fake episode, and on that episode, GetSearchRequest() will only do a season pack search.

Of course, to make it only search for seasons on that first “fake” episode, it took some finagling.

Finally, here’s our console for our “failed” results. We got the desired results, it’s just not the best practice.

Solution
As I have shown above, the previous solutions were all just quick fixes that weren't readable at first glance. More of a bandaid than a cure. With some communication from the project maintainer, it was more important to introduce a new object called “AnimeSeasonSearchCriteria”. This increases code reusability, scalability, and readability. These are just some of the important aspects to have in any project.
Due to the journey of our challenges, we were at least familiar with what we needed to do. There’s already the object “AnimeEpisodeSearchCriteria” that exists. Following the same pattern, we made the object “AnimeSeasonSearchCriteria”, a sibling class. Compared to the episode variant, our new object only has one crucial data container, the season number. The episode variant had more data stored, like episode number, which is unnecessary for our goal.
To do that, we needed to add a file for it in this folder:

In the folder, /Core/IndexerSearch/Definitions/, we added the file, AnimeSeasonSearchCriteria.cs, which contains our new object.

The “AnimeEpisodeSearchCriteria” for reference.

So here is our new object class.

Even though this new object only holds one piece of data, making a new object like this improves scalability if the project may want to improve or add more features to the season search.
With our new object created, we’re ready to implement it throughout the codebase. Wherever there’s an object of “AnimeEpisodeSearchCriteria” being used, we’ll make another function below it using our new object, “AnimeSeasonSearchCriteria”, taking cues of patterns from the episode search function into making a new function. We had to edit 21 files, so I’ll only just give 2 examples below.
Example 1:
Here, in a file that handles a specific indexer’s search API, NyaaRequestGenerator.cs, this is one use of the “AnimeEpisodeSearchCriteria” object.

Luckily, since C# is written similarly to C++, it’s easy to know the different parts of the function using the object. So writing a function for our new object proved to be not that difficult. Compared to the function above, here we just copied the same pattern for our new function, it’s the same code but all instances of anything related to “episode” are removed.

Example 2:
Another indexer called “FileListRequestGenerator.cs".

Then for our new object, here’s our new function right below it.

We just removed all instances of “episode”.
Overall, for our new object, “AnimeSeasonSearchCriteria”, we would just take the same logic used for “AnimeEpisodeSearchCriteria” objects, and implement it in a new function right below in the same file.
Here’s the console that shows off the new object.

Now that the first search for season packs is appropriately labeled.
The result of our work, and the results of a search query:
With this option off in the indexer settings.

We get these results.

Then with this option on.

We get these results after changes.

We’ve successfully made a positive change and got 4 more relevant results. After some testing, and writing some new tests, our work was approved and merged with the main project.
Link(s):
Our pull request, merged."""

new_item = {
    "id": 2,
    "blog": text,
    "rubric_labels": {
            "section1_project_about": 1,
            "section1_why_important": 1,
            "section1_typical_user": 1,
            "section2_issue_description": 1,
            "section2_issue_importance": 1,
            "section3_tech_stack_description": 1,
            "section3_system_diagram_included": 1,
            "section3_workflow_description": 1,
            "section4_challenges_identified": 1,
            "section4_problem_solving_attempts": 1,
            "section5_solution_explained": 1,
            "section5_solution_testing_proof": 1
    }
}

JSON_FILE_PATH = "data.json"

try:
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    data = []
except json.JSONDecodeError:
    data = []

if not isinstance(data, list):
    raise ValueError(f"Expected a JSON list in {JSON_FILE_PATH}, but got {type(data)}")

data.append(new_item)

# 5) Write the updated array back to the same JSON file
with open(JSON_FILE_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
    print("dumped")

print(f"Appended new item to {JSON_FILE_PATH} successfully!")