from functions import get_git_activity, get_zulip_activity, get_jitsi_activity
from datetime import datetime
import plotly
import plotly.graph_objs as go
import plotly.offline
from config import OUTPUT

class ZulipData:

    def __init__(self, total_messeges, total_mentions, history):
        self.total_mentions_count = total_mentions
        self.total_messeges_count = total_messeges
        self.history = history
    
    def Exists(self):
        return self.total_messeges_count > 0 or self.total_mentions_count > 0

    def GetMessages(self):
        return self.total_messeges_count
    
    def GetMentions(self):
        return self.total_mentions_count

    def GetHistory(self):
        return self.history

class GitData:

    def __init__(self, project_count, commit_count, commit_history):
        self.commit_count = commit_count
        self.project_count = project_count
        self.history = commit_history
    
    def Exists(self):
        return self.commit_count > 0 or self.project_count > 0

    def GetCommitCount(self):
        return self.commit_count

    def GetHistory(self):
        return self.history

class JitsiData:
    def __init__(self, poster, seminar, poster_history, project_history):
        self.poster_count = poster
        self.project_seminar_count = seminar
        self.poster_history = poster_history
        self.project_history = project_history

    def GetPosterCount(self):
        return self.poster_count

    def GetSeminarCount(self):
        return self.project_seminar_count

    def GetPosterHistory(self):
        return self.poster_history

    def GetProjectHistory(self):
        return self.project_history

class User:

    def __init__(self, username, realname):
        self.username = username
        self.git_data = None
        self.zulip_data = None
        self.jitsi_data = None
        self.realname = realname

    def UpdateGit(self):
        self.git_data = GitData(*get_git_activity(self.username))

    def UpdateZulip(self):
        self.zulip_data = ZulipData(*get_zulip_activity(self.username))

    def UpdateJitsi(self):
        self.jitsi_data = JitsiData(*get_jitsi_activity(self.username))

    def UpdateAllData(self):
        self.UpdateGit()
        self.UpdateJitsi()
        self.UpdateZulip()

    def CountGrade(self):
        grade = float(int(self.git_data.Exists())
            + int(self.git_data.GetCommitCount() > 0)
            + int(self.zulip_data.Exists())
            + int(self.zulip_data.Exists())
            + (0.5*self.jitsi_data.GetSeminarCount())
            + (0.5*self.jitsi_data.GetPosterCount()))
        return min(10, round(grade))



    def MakePlot(self):
        data = []
        zulip_data = [x[0] for x in self.zulip_data.GetHistory()]
        dates = zulip_data + [datetime.now()]
        values = list(range(1, len(dates)))
        if values:
            values.append(values[-1])
        else:
            values = [0]
        data.append(go.Scatter(x=dates, y=values, name="Сообщения в Zulip"))
        git_data = [x[0] for x in self.git_data.GetHistory()]
        dates = git_data + [datetime.now()]
        values = list(range(1, len(dates)))
        if values:
            values.append(values[-1])
        else:
            values = [0]
        data.append(go.Scatter(x=dates, y=values, name="Коммиты в GitLab"))

    
        jitsi_data = self.jitsi_data.GetProjectHistory()
        dates = jitsi_data + [datetime.now()]
        values = list(range(1, len(dates)))
        if values:
            values.append(values[-1])
        else:
            values = [0]
        data.append(go.Scatter(x=dates, y=values, name="Посещение проектных семинаров в Jitsi"))


        jitsi_data = self.jitsi_data.GetPosterHistory()
        dates = jitsi_data + [datetime.now()]
        values = list(range(1, len(dates)))
        if values:
            values.append(values[-1])
        else:
            values = [0]
        data.append(go.Scatter(x=dates, y=values, name="Посещение постерной сессии в Jitsi"))

        fig = go.Figure(data)
        fig.update_layout(

                title= f"Cтудент - {self.realname}, Итоговая оценка  = {self.CountGrade()}",
                xaxis_title="Время",
                yaxis_title="Активность",
                legend_title="Элементы активности",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="Black"
                )
            )


        fig.write_html(OUTPUT, auto_open = False)
        return plotly.offline.plot(fig, include_plotlyjs=False, output_type="div")
