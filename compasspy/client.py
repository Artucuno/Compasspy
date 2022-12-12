# Created by Artucuno
# https://artucuno.dev

import sys, os
import json
import requests
from .models import *
import logging
from datetime import date
from datetime import datetime
# StandardClass:1,Event:2,Meeting:3,Assembly:4,GenericActivity:5,CalendarItem:7,GenericGroup:8,ProfessionalDevelopment:9,LearningTask:10,Exam:11,OnCall:12,MinutesMeeting:13
API_ENDPOINT = 'https://compassapi.xyz/api/v1/'

class Compass:
    def __init__(self, userId: int, cookie: str):
        self.userId = userId
        self.cookie = cookie
        self.dt = {'userId': userId, 'cookie': cookie}
        self.user = None
    # GetMyUpcoming

    def GetTaskCategories(self, page: int = 1, start: int = 0, limit: int = 50):
        d = self.dt
        d['page'] = page
        d['start'] = start
        d['limit'] = limit
        x = requests.post(API_ENDPOINT+'GetAllTaskCategories', data=d).json()
        #print(x)
        a = []
        for f in x['d']:
            a += [TaskCategory.parse_obj(f)]
        return a

    def getUpcoming(self) -> list:
        """Get Upcoming Events"""
        x = requests.post(API_ENDPOINT+'GetMyUpcoming', data=self.dt).json()
        a = []
        for f in x['d']:
            a += [AlertItem.parse_obj(f)]
        return a

    def getLocations(self, page: int = 1, start: int = 0, limit: int = 50) -> list:
        """Get all buildings in school"""
        d = self.dt
        d['page'] = page
        d['start'] = start
        d['limit'] = limit
        x = requests.post(API_ENDPOINT+'GetAllLocations', data=d).json()
        a = []
        for f in x['d']:
            a += [Location.parse_obj(f)]
        return a

    def getInfo(self) -> UserDetailsBlob:
        """Get Current User Info"""
        x = requests.post(API_ENDPOINT+'GetInfo', data=self.dt).json()
        return UserDetailsBlob.parse_obj(x['d'])

    def getTimetable(self, dt: str = None) -> GenericMobileResponse:
        """Get your timetable"""
        if dt == None:
            da = date.today().strftime(f"%d/%m/%Y")
        else:
            da = dt
        d = self.dt
        d['date'] = str(da)
        x = requests.post(API_ENDPOINT+'GetTimetable', data=d).json()
        #print(x)
        return GenericMobileResponse.parse_obj(x['d'])

    def getStaff(self, page: int = 1, start: int = 0, limit: int = 50) -> list:
        """Get all staff"""
        d = self.dt
        d['page'] = page
        d['start'] = start
        d['limit'] = limit
        x = requests.post(API_ENDPOINT+'GetAllStaff', data=d).json()
        #print(x)
        a = []
        for f in x['d']:
            a += [User.parse_obj(f)]
        return a
        #return UserDetailsBlob.parse_obj(x['d'])

    def login(self) -> bool:
        """Function for logging in"""
        if not self.user:
            x = requests.post(API_ENDPOINT+'GetInfo', data=self.dt).json()
            #print(x)
            self.user = UserDetailsBlob.parse_obj(x['d'])
            logging.info('Compass - Logged in', self.user)
            return True
        else:
            logging.warning('Compass - Already logged in')
            return True
