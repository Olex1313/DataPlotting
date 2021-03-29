from classes import User
from config import USERNAME, REALNAME

MainUser = User(USERNAME, REALNAME)
MainUser.UpdateAllData()
fig = MainUser.MakePlot()
