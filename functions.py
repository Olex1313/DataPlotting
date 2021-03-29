import json
from datetime import date, datetime
from config import DATA_PATH

def get_zulip_activity( email : str, data_path = DATA_PATH + "ZulipStats.json"):
    """
    data_path: str - path to file
    email: str - user email
    -> tuple(total_messages, total_mentions, stats)
    """
    with open(data_path, 'r', encoding="utf-8") as f:

        obj = json.loads(f.read())

        for user in obj:
            if user['email'] == email:

                total_messages = len(user["messages"])
                total_mentions = len(user["mentions"])

                messages = []
                counter = 0

                for message in user["messages"]:
                    counter += 1
                    date = datetime.fromisoformat(message["timestamp"].replace('Z', '+00:00'))
                    messages.append((date, counter))
                messages.sort()
                return (total_messages, total_mentions, messages)

def get_git_activity( email : str, data_path = DATA_PATH + "GitStats.json"):
    """
    data_path: str - path to file
    email: str - user email
    -> tuple(commit_count, project_count, commits)
    """
    with open(data_path, 'r', encoding="utf-8") as f:
        obj = json.loads(f.read())
        for user in obj:
            if user["email"] == email:

                true_name = user["name"]
                project_count = len(user["projects"])

                commit_count = 0
                commits = []

                for project in user["projects"]:
                    for commit in project["commits"]:
                        if commit["committer_name"] == true_name:
                            commit_count += 1
                            date = datetime.fromisoformat(commit["committed_date"].replace('Z', "+00:00"))
                            commits.append((date, commit_count))
                commits.sort()
                return (project_count, commit_count, commits)

def get_jitsi_activity(email : str, data_path = DATA_PATH + "JitsiSession.json"):
    """
    data_path: str - path to file
    email: str - user email
    -> tuple(commit_count, project_count, commits)
    """
    with open(data_path, 'r', encoding="utf-8") as f:
        obj = json.loads(f.read())
        seminar_count = 0
        poster_count = 0
        seminar = []
        poster = []
        for session in obj:
            if session["room"] == "312" and session["username"] == email:
                seminar_count += 1
                seminar.append(datetime.strptime(session["date"], "%Y-%m-%d"))
            if session["room"].startswith("project") and session["username"] == email:
                poster_count += 1
                poster.append(datetime.strptime(session["date"], "%Y-%m-%d"))
        poster.sort()
        seminar.sort()
        return (poster_count, seminar_count, poster, seminar)
