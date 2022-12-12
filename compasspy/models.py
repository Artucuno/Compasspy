# Artucuno.dev

from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from .errors import *

# The following models use data parsed from the public-ish Compass API

# Note: The API that Compass has is very painful, but i have written some 'descriptions' for parts that may not make sense
# If you know what some of the variables mean, please open an issue on Github or submit a pull request!

class ExtendedStatus(BaseModel):
    __type: Optional[str]
    id: int
    uiStatus: Optional[int]
    shortName: str
    attendanceGridDisplayMode: Optional[None] # Unsure
    attendanceGridOrdinal: Optional[None] # Unsure
    c: Optional[str] # Unsure (Some sort of code)
    d: Optional[str] # Details (EG: The student is present on school grounds.)
    # def: bool # Unsure - Unable to add because of Python
    eventsUi: bool # Unsure (Possibly something to do with the events page)
    lastModified: Optional[str]
    lastModifiedUserId: Optional[int]
    n: Optional[str] # Another Status (EG: Present) (Possibly means name)
    note: Optional[str]
    parentApprovalsUi: bool # Unsure
    periodCalc_LateParentApproved: bool # If parent has submitted a late notice
    periodCalc_LateUnapproved: bool
    periodCalc_Present: bool # Present
    periodCalc_NotMarked: bool # Period not marked

class TimelinePeriod(BaseModel):
    """Model for a period"""
    __type: Optional[str]
    userId: int
    name: str
    onCampus: bool
    status: Optional[int]
    statusName: Optional[str] # Timeline Status (If User attended or not)
    teachingTime: bool # Unsure
    attendanceOverride: bool # Unsure (Possibly to override if a user attended)
    exportId: Optional[str] # Unsure
    extendedStatus: Optional[ExtendedStatus]
    start: Optional[str]
    finish: Optional[str]

class User(BaseModel):
    __type: Optional[str]
    id: int
    sussiId: Optional[str] # Secondary ID
    userStatus: int
    n: str # Fullname
    fn: str # Firstname
    ln: str # Lastname
    namePrefFirst: Optional[str]
    namePrefLastId: Optional[str] # "Lastname, Firstname (displayCode)"
    nif: Optional[str] # "Firstname Lastname (displayCode)"
    ns: str # Fullname with uppercase Lastname
    campusId: int # Campus they work in
    baseRole: int # Role in the school
    ce: Optional[str] # Unsure
    displayCode: str # Teacher Display code
    ii: str # Same as displayCode from what I can tell
    mobileNumber: Optional[str] # No teachers have this (I think)
    nameFirstPrefLastIdForm: str # Mix of full name and displayCode
    doNotContact: bool
    f: Optional[str] # Unsure
    start: Optional[str] # When they started working
    finish: Optional[str] # When they finish working / resign (?)
    govtCode1: Optional[str] # Unsure
    govtCode2: Optional[str] # Unsure
    hasRegisteredDevice: bool

class UserDetailsBlob(BaseModel):
    __type: Optional[str]
    userId: int # Internal Student ID
    chroniclePinnedCount: Optional[int]
    userDisplayCode: str # Student ID
    userSussiID: Optional[str] # Secondary Student ID
    userDetails: str # Time since Date of Birth
    userEmail: str
    userFirstName: str
    userLastName: str
    userYearLevel: str # Year Level String
    userYearLevelId: int # Year Level Number
    userPreferredName: Optional[str]
    userPreferredLastName: Optional[str]
    userFullName: str
    userRole: int # Unsure yet (Possibly to tell between staff / student)
    userStatus: int # Unsure yet (Possibly to show if student is at school)
    userPhotoPath: Optional[str] # Location of user profile picture
    userSquarePhotoPath: Optional[str] # Square Photo
    userHouse: Optional[str] # User House Group
    userGenderPronouns: Optional[str] # Not implemented at my school
    userFormGroup: str # Year / House
    userSchoolURL: Optional[str]
    userSchoolId: Optional[str]
    userTimeLinePeriods: List[TimelinePeriod]

class StandardClass(BaseModel):
    __type: Optional[str]
    id: int
    subjectId: int # Different to id
    name: str
    subjectLongName: str
    facultyName: Optional[str]
    description: Optional[str]
    importIdentifier: Optional[str]
    subjectImportIdentifier: Optional[str]
    importTeachers: bool # Unsure
    layerAllowsImport: bool # Unsure
    layerId: int # Unsure
    locationId: Optional[int]
    managerId: int # Possibly Teacher ID
    managerImportIdentifier: str # Manager identifier
    attendanceModeDefault: int # Unsure
    campusId: Optional[int]
    checkInEnabledDefault: int # Unsure
    customLocation: Optional[str] # Unsure
    extendedStatusId: int # Unsure
    start: Optional[str] # Date the subject starts
    finish: Optional[str] # Date the subject finishes
    haparaSyncEnabled: bool # Unsure
    yearLevelShortName: Optional[str]

class DataExtGridDataContainer(BaseModel):
    __type: Optional[str]
    data: List[StandardClass]
    total: int

class Location(BaseModel):
    __type: Optional[str]
    id: int
    roomName: str
    n: Optional[str] # Same as roomName
    longName: str
    building: Optional[str]
    archived: bool

class AlertItem(BaseModel):
    __type: Optional[str]
    Type: int # Unsure
    AlertItemId: int
    Body: Optional[str] # Alert Item Body (HTML)
    Dismissible: bool
    ImageSourceUrl: Optional[str]
    IsWarning: bool
    LinkText: Optional[str]
    LinkUrl: Optional[str]
    Title: Optional[str]

class TaskCategory(BaseModel):
    __type: Optional[str]
    categoryId: int
    categoryName: Optional[str] # Name (EG: Homework, Assignment, etc)
    categoryColour: Optional[str] # Hex code

class CalendarTransport(BaseModel):
    __type: Optional[str]
    activityId: int
    activityType: int
    instanceId: Optional[str]
    topTitleLine: Optional[str]
    bottomTitleLine: Optional[str]
    topAndBottomLine: Optional[str]
    allDay: bool
    start: Optional[str]
    finish: Optional[str]
    rollMarked: bool
    runningStatus: int
    attendanceMode: int # Unsure
    backgroundColor: str # Unsure

class GenericMobileResponse(BaseModel):
    __type: Optional[str]
    data: List[CalendarTransport]

def getType(tp: str): # Converts __type to a class model
    p = {
    "UserDetailsBlob": UserDetailsBlob,
    "User:http://jdlf.com.au/ns/data/users": User,
    "TimelinePeriod:http://jdlf.com.au/ns/data/attendance/v2": TimelinePeriod,
    "Es:http://jdlf.com.au/ns/business/attendance/transport": ExtendedStatus,
    "DataExtGridDataContainer:http://jdlf.com.au/ns/business/transport": DataExtGridDataContainer,
    "StandardClass:http://jdlf.com.au/ns/business/curriculum": StandardClass,
    "LC": Location,
    "AlertItem:http://jdlf.com.au/ns/data/newsfeed": AlertItem,
    "GenericMobileResponse:http://jdlf.com.au/ns/data/mobile/": GenericMobileResponse,
    "CalendarTransport:http://jdlf.com.au/ns/data/mobile": CalendarTransport
    }
    if tp in p:
        return p[tp]
    raise UnknownType(f"{tp}")
