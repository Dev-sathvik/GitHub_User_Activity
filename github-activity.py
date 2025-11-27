import sys
import requests

BASEURL = "https://api.github.com"

def fetch_results(endpoint, headers, params):
   try:
        r = requests.get(endpoint, headers=headers, params=params)
        r.raise_for_status()
   except ConnectionError:
        sys.exit("Network Problem")
   except requests.exceptions.HTTPError:
        sys.exit("Http Error")
   except TimeoutError:
        sys.exit("Timeout")
   except requests.exceptions.RequestException:
        sys.exit("Some exception")
   return r.json()

def main():
    if len(sys.argv) != 2:
        sys.exit("Wrong arguments")
    
    username = sys.argv[1].strip()
    ENDPOINT = f"{BASEURL}/users/{username}/events"

    headers = {'accept': 'application/vnd.github+json'}
    page_count = 1
    params = {'per_page': 10, 'page': f"{page_count}"}
    
    json_data = fetch_results(ENDPOINT, headers, params)

    if (len(json_data) == 0):
        sys.exit("Wrong username or no events")

    while (len(json_data) != 0):
        list_activity(json_data)
        while True:
            res = input("Show more: y/n: ").lower()
            if res == 'y':
                break
            elif res == 'n':
                sys.exit()
        page_count = page_count + 1
        params = {'per_page': 10, 'page': f"{page_count}"}
        json_data = fetch_results(ENDPOINT, headers, params)
    print("---END---")

def list_activity(json_data):
    for event in json_data:
        match event["type"]:
            case "CommitCommentEvent":
                print(f"A new commit comment was created in {event['repo']['name']}")

            case "CreateEvent":
                print(f"A {event['payload']['ref_type']} was created in {event['repo']['name']}")

            case "DeleteEvent":
                print(f"A {event['payload']['ref_type']} was deleted in {event['repo']['name']}")

            case "DiscussionEvent":
                print(f"A discussion was created in {event['repo']['name']}")

            case "ForkEvent":
                print(f"{event['repo']['name']} was forked.")

            case "GollumEvent":
                pages = event["payload"]["pages"]
                for page in pages:
                    action = page["action"]
                    title = page["title"]
                    print(f"Wiki page '{title}' was {action} in {event['repo']['name']}")

            case "IssueCommentEvent":
                print(f"A comment was added to an issue or pull request in {event['repo']['name']}")

            case "IssuesEvent":
                action = event["payload"]["action"]
                issue = event["payload"]["issue"]
                print(f"Issue #{issue['number']} was {action} in {event['repo']['name']}")

            case "MemberEvent":
                member = event["payload"]["member"]["login"]
                print(f"User '{member}' was added as a collaborator in {event['repo']['name']}")

            case "PublicEvent":
                print(f"The repository {event['repo']['name']} was made public.")

            case "PullRequestEvent":
                action = event["payload"]["action"]
                number = event["payload"]["number"]
                print(f"Pull request #{number} was {action} in {event['repo']['name']}")

            case "PullRequestReviewEvent":
                action = event["payload"]["action"]
                print(f"A pull request review was {action} in {event['repo']['name']}")

            case "PullRequestReviewCommentEvent":
                print(f"A review comment was added to a pull request in {event['repo']['name']}")

            case "PushEvent":
                ref = event["payload"]["ref"]
                print(f"A push occurred on {ref} in {event['repo']['name']}")

            case "ReleaseEvent":
                action = event["payload"]["action"]
                print(f"A release was {action} in {event['repo']['name']}")

            case "WatchEvent":
                print(f"{event['repo']['name']} was starred.")

            case _:
                print(f"Unknown event type: {event['type']}")

if __name__ == "__main__":
    main()

    
    
