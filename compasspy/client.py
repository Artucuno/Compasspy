# Created by Artucuno
# https://artucuno.dev

import logging
from datetime import datetime, date

import requests

from .models import *


# StandardClass:1,Event:2,Meeting:3,Assembly:4,GenericActivity:5,CalendarItem:7,GenericGroup:8,ProfessionalDevelopment:9,LearningTask:10,Exam:11,OnCall:12,MinutesMeeting:13

class Compass:
    def __init__(self, schoolSubdomain: str, cookie: str, login: bool = False):
        # API Endpoint Stuffs
        self.API_ENDPOINT = f'https://{schoolSubdomain}.compass.education/Services/'
        self.headers = {"Accept": "*/*", "Content-Type": "application/json", "Accept-Encoding": "gzip, deflate", "User-Agent": "iOS/14_6_0 type/iPhone CompassEducation/6.3.0", "Accept-Language": "en-au", "Connection": "close"}
        self.cookies = {"ASP.NET_SessionId": cookie}

        self.schoolSubdomain = schoolSubdomain
        self.userId = ''
        self.cookie = cookie
        self.dt = {'userId': None, 'cookie': cookie, 'subdomain': schoolSubdomain}
        self.user = None

        if login:
            self.login()

    def getAccount(self) -> Account:
        """
        Get the account of the user
        :return: Account
        """
        d = self.dt
        #x = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies).json()
        x = requests.post(self.API_ENDPOINT+'Accounts.svc/GetAccount', headers=self.headers, cookies=self.cookies)
        try:
            x = x.json()
        except Exception as e:
            raise APIError(x.text)
        return Account.parse_obj(x['d'])

    def saveTask(self, task: str) -> int:
        """
        Save a task to the 'My Tasks' section
        :param task: The task to save
        :return: The ID of the task
        """
        data = {"sessionstate": "readonly", "userId": int(self.dt['userId']), "task": {"id": 0, "taskName": task, "status": False}}
        x = requests.post(self.API_ENDPOINT+'TaskService.svc/SaveTaskItem', headers=self.headers, cookies=self.cookies, json=data).json()['d']
        return x

    def getTasks(self, page: int = 1, start: int = 0, limit: int = 50) -> List[Task]:
        """
        Get the tasks of the user
        :param page: Page number
        :param start: Start number
        :param limit: Task limit
        :return: List[Task]
        """
        data = {"sessionstate": "readonly", "userId": int(self.dt['userId']), "page": page, "start": start, "limit": limit}
        x = requests.post(self.API_ENDPOINT+'TaskService.svc/GetTaskItems', headers=self.headers, cookies=self.cookies, json=data).json()
        a = []
        for f in x['d']:
            a += [Task.parse_obj(f)]
        return a

    def getTaskCategories(self, page: int = 1, start: int = 0, limit: int = 50) -> List[TaskCategory]:
        """
        Get task categories (Eg. Homework, Assessment)
        :param page: Page number
        :param start: Start number
        :param limit: Task limit
        :return: List[TaskCategory]
        """
        data = {"sessionstate": "readonly", "page": page, "start": start, "limit": limit}
        x = requests.post(self.API_ENDPOINT+'LearningTasks.svc/GetAllTaskCategories', headers=self.headers, cookies=self.cookies, json=data).json()
        a = []
        for f in x['d']:
            a += [TaskCategory.parse_obj(f)]
        return a

    def getUpcoming(self) -> List[AlertItem]:
        """
        Get upcoming events
        :return: List[AlertItem]
        """
        data = {"sessionstate": "readonly", "userId": int(self.dt['userId']), "targetUserId": int(self.dt['userId'])}
        x = requests.post(self.API_ENDPOINT+'NewsFeed.svc/GetMyUpcoming', headers=self.headers, cookies=self.cookies, json=data).json()
        a = []
        for f in x['d']:
            a += [AlertItem.parse_obj(f)]
        return a

    def getLocations(self, page: int = 1, start: int = 0, limit: int = 50) -> List[Location]:
        """
        Get all buildings on Campus
        :param page: Page number
        :param start: Start number
        :param limit: Location limit
        :return:
        """
        x = requests.get(self.API_ENDPOINT+f'ReferenceDataCache.svc/GetAllLocations?sessionstate=readonly&page={page}&start={start}&limit={limit}', headers=self.headers, cookies=self.cookies).json()
        a = []
        for f in x['d']:
            a += [Location.parse_obj(f)]
        return a

    def getInfo(self, targetUserId: int = None) -> UserDetailsBlob:
        """
        Get user info
        :param targetUserId: The optional user ID of the target user
        :return: UserDetailsBlob
        """
        if targetUserId == None:
            targetUserId = self.dt['userId']
        data = {"sessionstate": "readonly", "userId": int(self.dt['userId']), "targetUserId": int(targetUserId)}
        x = requests.post(self.API_ENDPOINT+'User.svc/GetUserDetailsBlobByUserId', headers=self.headers, cookies=self.cookies, json=data).json()
        return UserDetailsBlob.parse_obj(x['d'])

    def getNamesById(self, ids: list, page: int = 1, start: int = 0, limit: int = 25) -> None:
        """
        Get names by ID
        :param ids: IDs of users
        :param page: Page number
        :param start: Start number
        :param limit: Return limit
        :return:
        """
        data = {"userIds": ','.join(ids), "page": page, "start": start, "limit": limit}
        x = requests.post(self.API_ENDPOINT+'User.svc/GetNamesById', headers=self.headers, cookies=self.cookies, json=data).json()
        print(x)
        # Unfinished

    def getTimetable(self, dt: str = None) -> GenericMobileResponse:
        """
        Get the timetable of the user
        :param dt: The date to get the timetable for
        :return: GenericMobileResponse
        """
        if dt == None:
            da = date.today().strftime(f"%d/%m/%Y")
        else:
            da = datetime.strptime(str(dt), f"%d/%m/%Y").strftime(f"%d/%m/%Y")
        data = {"date": f"{da} - 12:00 am", "sessionstate": "readonly", "userId": int(self.dt['userId'])}
        x = requests.post(self.API_ENDPOINT+'mobile.svc/GetScheduleLinesForDate', headers=self.headers, cookies=self.cookies, json=data).json()
        return GenericMobileResponse.parse_obj(x['d'])

    def getStaff(self, page: int = 1, start: int = 0, limit: int = 50) -> List[User]:
        """
        Get All Staff Members
        :param page: Page number
        :param start: Start number
        :param limit: Return limit
        :return: List[User]
        """
        data = {"sessionstate": "readonly", "userId": int(self.dt['userId']), "page": page, "start": start, "limit": limit}
        x = requests.post(self.API_ENDPOINT+'User.svc/GetAllStaff', headers=self.headers, cookies=self.cookies, json=data).json()
        a = []
        for f in x['d']:
            a += [User.parse_obj(f)]
        return a

    def getAllStudents(self, page: int = 1, start: int = 0, limit: int = 50) -> List[User]:
        """
        Get All Students - Requires a staff account
        :param page: Page number
        :param start: Start number
        :param limit: Return limit
        :return: List[User]
        """
        data = {"sessionstate": "readonly", "userId": int(self.dt['userId']), "page": page, "start": start, "limit": limit}
        x = requests.post(self.API_ENDPOINT+'User.svc/GetAllStudents', headers=self.headers, cookies=self.cookies, json=data).json()
        if 'h' in x:
            raise UnauthorisedError(x['h'])
        a = []
        for f in x['d']:
            a += [User.parse_obj(f)]
        return a

    def getAllStudentsBasic(self, page: int = 1, start: int = 0, limit: int = 50) -> List[UserBasic]:
        """
        Get All Students (Basic Info) - Requires a staff account
        :param page: Page number
        :param start: Start number
        :param limit: Return limit
        :return: List[UserBasic]
        """
        data = {"sessionstate": "readonly", "userId": int(self.dt['userId']), "page": page, "start": start, "limit": limit}
        x = requests.post(self.API_ENDPOINT+'User.svc/GetAllStudentsBasic', headers=self.headers, cookies=self.cookies, json=data).json()
        if 'h' in x:
            raise UnauthorisedError(x['h'])
        a = []
        for f in x['d']:
            a += [UserBasic.parse_obj(f)]
        return a

    def login(self) -> bool:
        """
        Attempt to login to Compass
        :return: True if successful, False if not
        """
        if not self.user:
            d = self.dt.copy()
            x = requests.post(self.API_ENDPOINT+'Accounts.svc/GetAccount', headers=self.headers, cookies=self.cookies)
            try:
                x = x.json()
            except Exception as e:
                raise APIError(x.text)
            if 'h' in x:
                raise UnauthorisedError(x['h'])
            self.user = Account.parse_obj(x['d'])
            self.dt = {'userId': self.user.userId, 'cookie': self.cookie, 'subdomain': self.schoolSubdomain}
            logging.info('Compass - Logged in', self.user)
            return True
        else:
            logging.warning('Compass - Already logged in')
            return True
