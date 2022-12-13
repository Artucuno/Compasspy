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
    def __init__(self, schoolSubdomain: str, cookie: str):
        self.schoolSubdomain = schoolSubdomain
        self.userId = None
        self.cookie = cookie
        self.dt = {'userId': None, 'cookie': cookie, 'subdomain': schoolSubdomain}
        self.user = None

    def getAccount(self) -> Account:
        d = self.dt
        x = requests.post(API_ENDPOINT+'GetAccount', data=d).json()
        return Account.parse_obj(x['d'])

    def saveTask(self, task: str) -> int:
        d = self.dt.copy()
        d['task'] = task
        x = requests.post(API_ENDPOINT+'SaveTaskItem', data=d).json()['d']
        return x

    def getTasks(self, page: int = 1, start: int = 0, limit: int = 50) -> list:
        d = self.dt.copy()
        d['page'] = page
        d['start'] = start
        d['limit'] = limit
        x = requests.post(API_ENDPOINT+'GetTaskItems', data=d).json()
        a = []
        for f in x['d']:
            a += [Task.parse_obj(f)]
        return a

    def GetTaskCategories(self, page: int = 1, start: int = 0, limit: int = 50) -> list:
        d = self.dt.copy()
        d['page'] = page
        d['start'] = start
        d['limit'] = limit
        x = requests.post(API_ENDPOINT+'GetAllTaskCategories', data=d).json()
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
        d = self.dt.copy()
        d['page'] = page
        d['start'] = start
        d['limit'] = limit
        x = requests.post(API_ENDPOINT+'GetAllLocations', data=d).json()
        a = []
        for f in x['d']:
            a += [Location.parse_obj(f)]
        return a

    def getInfo(self, targetUserId: int = None) -> UserDetailsBlob:
        """Get Current User Info"""
        d = self.dt.copy()
        if targetUserId == None:
            d['targetUserId'] = self.dt['userId']
        else:
            d['targetUserId'] = targetUserId
        x = requests.post(API_ENDPOINT+'GetInfo', data=d).json()
        return UserDetailsBlob.parse_obj(x['d'])

    def getNamesById(self, ids: list, page: int = 1, start: int = 0, limit: int = 25):
        d = self.dt.copy()
        d['page'] = page
        d['start'] = start
        d['limit'] = limit
        d['useridlist'] = ','.join(ids)
        x = requests.post(API_ENDPOINT+'GetNamesById', data=d).json()
        print(x)
        # Unfinished

    def getTimetable(self, dt: str = None) -> GenericMobileResponse:
        """Get your timetable"""
        if dt == None:
            da = date.today().strftime(f"%d/%m/%Y")
        else:
            da = dt
        d = self.dt.copy()
        d['date'] = str(da)
        x = requests.post(API_ENDPOINT+'GetTimetable', data=d).json()
        return GenericMobileResponse.parse_obj(x['d'])

    def getStaff(self, page: int = 1, start: int = 0, limit: int = 50) -> list:
        """Get all staff"""
        d = self.dt.copy()
        d['page'] = page
        d['start'] = start
        d['limit'] = limit
        x = requests.post(API_ENDPOINT+'GetAllStaff', data=d).json()
        a = []
        for f in x['d']:
            a += [User.parse_obj(f)]
        return a

    def login(self) -> bool:
        """Function for logging in"""
        if not self.user:
            d = self.dt.copy()
            x = requests.post(API_ENDPOINT+'GetAccount', data=d).json()
            self.user = Account.parse_obj(x['d'])
            self.dt = {'userId': self.user.userId, 'cookie': self.cookie, 'subdomain': self.schoolSubdomain}
            logging.info('Compass - Logged in', self.user)
            return True
        else:
            logging.warning('Compass - Already logged in')
            return True
