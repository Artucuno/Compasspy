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

class Compass:
    def __init__(self, schoolSubdomain: str, cookie: str):
        # API Endpoint Stuffs
        self.API_ENDPOINT = f'https://{schoolSubdomain}.compass.education/Services/'
        self.headers = {"Accept": "*/*", "Content-Type": "application/json", "Accept-Encoding": "gzip, deflate", "User-Agent": "iOS/14_6_0 type/iPhone CompassEducation/6.3.0", "Accept-Language": "en-au", "Connection": "close"}
        self.cookies = {"ASP.NET_SessionId": cookie}

        self.schoolSubdomain = schoolSubdomain
        self.userId = None
        self.cookie = cookie
        self.dt = {'userId': None, 'cookie': cookie, 'subdomain': schoolSubdomain}
        self.user = None

    def getAccount(self) -> Account:
        """Get current user account"""
        d = self.dt
        #x = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies).json()
        x = requests.post(self.API_ENDPOINT+'Accounts.svc/GetAccount', headers=self.headers, cookies=self.cookies)
        try:
            x = x.json()
        except Exception as e:
            raise APIError(x.text)
        return Account.parse_obj(x['d'])

    def saveTask(self, task: str) -> int:
        """Save a task to the 'My Tasks' section"""
        data = {"sessionstate": "readonly", "userId": int(self.dt['userId']), "task": {"id": 0, "taskName": task, "status": False}}
        x = requests.post(self.API_ENDPOINT+'TaskService.svc/SaveTaskItem', headers=self.headers, cookies=self.cookies, json=data).json()['d']
        return x

    def getTasks(self, page: int = 1, start: int = 0, limit: int = 50) -> list:
        """Get tasks from the 'My Tasks' section"""
        data = {"sessionstate": "readonly", "userId": int(self.dt['userId']), "page": page, "start": start, "limit": limit}
        x = requests.post(self.API_ENDPOINT+'TaskService.svc/GetTaskItems', headers=self.headers, cookies=self.cookies, json=data).json()
        a = []
        for f in x['d']:
            a += [Task.parse_obj(f)]
        return a

    def GetTaskCategories(self, page: int = 1, start: int = 0, limit: int = 50) -> list:
        data = {"sessionstate": "readonly", "page": page, "start": start, "limit": limit}
        x = requests.post(self.API_ENDPOINT+'LearningTasks.svc/GetAllTaskCategories', headers=self.headers, cookies=self.cookies, json=data).json()
        a = []
        for f in x['d']:
            a += [TaskCategory.parse_obj(f)]
        return a

    def getUpcoming(self) -> list:
        """Get Upcoming Events"""
        data = {"sessionstate": "readonly", "userId": int(self.dt['userId']), "targetUserId": int(self.dt['userId'])}
        x = requests.post(self.API_ENDPOINT+'NewsFeed.svc/GetMyUpcoming', headers=self.headers, cookies=self.cookies, json=data).json()
        a = []
        for f in x['d']:
            a += [AlertItem.parse_obj(f)]
        return a

    def getLocations(self, page: int = 1, start: int = 0, limit: int = 50) -> list:
        """Get all buildings in school"""
        x = requests.get(self.API_ENDPOINT+f'ReferenceDataCache.svc/GetAllLocations?sessionstate=readonly&page={page}&start={start}&limit={limit}', headers=self.headers, cookies=self.cookies).json()
        a = []
        for f in x['d']:
            a += [Location.parse_obj(f)]
        return a

    def getInfo(self, targetUserId: int = None) -> UserDetailsBlob:
        """Get Current User Info"""
        if targetUserId == None:
            targetUserId = self.dt['userId']
        data = {"sessionstate": "readonly", "userId": int(self.dt['userId']), "targetUserId": int(targetUserId)}
        x = requests.post(self.API_ENDPOINT+'User.svc/GetUserDetailsBlobByUserId', headers=self.headers, cookies=self.cookies, json=data).json()
        return UserDetailsBlob.parse_obj(x['d'])

    def getNamesById(self, ids: list, page: int = 1, start: int = 0, limit: int = 25):
        data = {"userIds": ','.join(ids), "page": page, "start": start, "limit": limit}
        x = requests.post(API_ENDPOINT+'User.svc/GetNamesById', headers=self.headers, cookies=self.cookies, json=data).json()
        print(x)
        # Unfinished

    def getTimetable(self, dt: str = None) -> GenericMobileResponse:
        """Get your timetable"""
        if dt == None:
            da = date.today().strftime(f"%d/%m/%Y")
        else:
            da = datetime.strptime(str(dt), f"%d/%m/%Y").strftime(f"%d/%m/%Y")
        data = {"date": f"{da} - 12:00 am", "sessionstate": "readonly", "userId": int(self.dt['userId'])}
        x = requests.post(self.API_ENDPOINT+'mobile.svc/GetScheduleLinesForDate', headers=self.headers, cookies=self.cookies, json=data).json()
        return GenericMobileResponse.parse_obj(x['d'])

    def getStaff(self, page: int = 1, start: int = 0, limit: int = 50) -> list:
        """Get All Staff Members"""
        data = {"sessionstate": "readonly", "userId": int(self.dt['userId']), "page": page, "start": start, "limit": limit}
        x = requests.post(self.API_ENDPOINT+'User.svc/GetAllStaff', headers=self.headers, cookies=self.cookies, json=data).json()
        a = []
        for f in x['d']:
            a += [User.parse_obj(f)]
        return a

    def login(self) -> bool:
        """Function for logging in"""
        if not self.user:
            d = self.dt.copy()
            x = requests.post(self.API_ENDPOINT+'Accounts.svc/GetAccount', headers=self.headers, cookies=self.cookies)
            try:
                x = x.json()
            except Exception as e:
                raise APIError(x.text)
            print('login', x)
            self.user = Account.parse_obj(x['d'])
            self.dt = {'userId': self.user.userId, 'cookie': self.cookie, 'subdomain': self.schoolSubdomain}
            logging.info('Compass - Logged in', self.user)
            return True
        else:
            logging.warning('Compass - Already logged in')
            return True
