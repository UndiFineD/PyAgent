#!/usr/bin/env python3


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import ntpath
import re
import urllib.parse
import urllib.request
import hashlib
from threading import Thread

# For compatibility with ported Python 2 code
urlparse = urllib.parse
urllib2 = urllib.request


class BColors:
# [BATCHFIX] Commented metadata/non-Python
#     pass  # [BATCHFIX] inserted for empty class
"""TITLE = "\033[95m"""
# [BATCHFIX] Commented metadata/non-Python
# #     OKBLUE = "\033[94m"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #     OKGREEN = "\033[92m"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #     INFO = "\033[93m"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #     OKRED = "\033[91m"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #     ENDC = "\033[0m"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #     BOLD = "\033[1m"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #     BGRED = "\033[41m"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #     UNDERLINE = "\033[4m"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #     FGWHITE = "\033[37m"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #     FAIL = "\033[95m"  # [BATCHFIX] closed string


rootDir = os.path.expanduser("~") + "/.APKEnum/"  # ConfigFolder ~/.SourceCodeAnalyzer/
# projectDir =
# apkFilePath =
# apkFileName =
# apkHash =
scopeMode = False


# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # scopeList = []


# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # authorityList = []
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # inScopeAuthorityList = []
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # publicIpList = []
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # s3List = []
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # s3WebsiteList = []
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # gmapKeys = []
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # vulnerableGmapKeys = []
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # unrestrictedGmapKeys = []
gmapURLs = [
    "https://maps.googleapis.com/maps/api/staticmap?center=45%2C10&zoom=7&size=400x400&key=",
# [BATCHFIX] Commented metadata/non-Python
# #     ("https://maps.googleapis.com/maps/api/streetview?size=400x400&location=40.720032,-73.988354&fov=90&heading="  # [BATCHFIX] closed string
     "235&pitch=10&key="),
    "https://www.google.com/maps/embed/v1/place?q=Seattle&key=",
    "https://www.google.com/maps/embed/v1/search?q=record+stores+in+Seattle&key=",
# [BATCHFIX] Commented metadata/non-Python
# #     ("https://maps.googleapis.com/maps/api/directions/json?origin=Disneyland&destination=Universal+Studios+"  # [BATCHFIX] closed string
     "Hollywood4&key="),
    "https://maps.googleapis.com/maps/api/geocode/json?latlng=40,30&key=",
# [BATCHFIX] Commented metadata/non-Python
# #     ("https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=40.6655101,-73.89188969999998"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #      "&destinations=40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #      "-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.659569%2C-73.933783%7C40.729029%2C"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #      "-73.851524%7C40.6860072%2C-73.6334271%7C40.598566%2C-73.7527626%7C40.659569%2C-73.933783%7C40.729029%2C"  # [BATCHFIX] closed string
     "-73.851524%7C40.6860072%2C-73.6334271%7C40.598566%2C-73.7527626&key="),
# [BATCHFIX] Commented metadata/non-Python
# #     ("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Museum%20of%20Contemporary%20Art"  # [BATCHFIX] closed string
     "%20Australia&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key="),
    "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=Bingh&types=%28cities%29&key=",
    "https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536,-104.9847034&key=",
    "https://maps.googleapis.com/maps/api/timezone/json?location=39.6034810,-119.6822510&timestamp=1331161200&key=",
# [BATCHFIX] Commented metadata/non-Python
# #     ("https://roads.googleapis.com/v1/nearestRoads?points=60.170880,24.942795|"  # [BATCHFIX] closed string
     "60.170879,24.942796|60.170877,24.942796&key="),
]

# [BATCHFIX] Commented metadata/non-Python
# # apktoolPath = "./Dependencies/apktool.jar"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
# urlRegex = (
# [BATCHFIX] Commented metadata/non-Python
# #     r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+):?\\\\d*)([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"  # [BATCHFIX] closed string
)  # regex to extract domain
# s3Regex1 = rhttps*://(.+?)\.s3\..+?\.amazonaws\.com\/.+?
# s3Regex2 = rhttps*://s3\..+?\.amazonaws\.com\/(.+?)\/.+?
# s3Regex3 = rS3://(.+?)/
# s3Website1 = rhttps*://(.+?)\.s3-website\..+?\.amazonaws\.com
# s3Website2 = rhttps*://(.+?)\.s3-website-.+?\.amazonaws\.com
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
# publicIp = (
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # #     rhttps*://(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(?<!172\.(16|17|18|19|20|21|22|23|24
# [BATCHFIX] Commented metadata/non-Python
# #     r"|25|26|27|28|29|30|31))(?<!127)(?<!^10)(?<!^0)\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #     r"[0-5])(?<!192\.168)(?<!172\.(16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31))\.([0-9]|"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #     r"[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #     r"(?<!\.255$))"  # [BATCHFIX] closed string
)
# [BATCHFIX] Commented metadata/non-Python
# # gMapsAPI = r"(AIzaSy[\w-]{33})"  # [BATCHFIX] closed string


def myPrint(text: str, print_type: str) -> None:
    pass  # [BATCHFIX] inserted for empty block
""""Print text with color based on the print type."""
#     if print_type == "INFO":
#         print()
        return
    if print_type == "INFO_WS":
        print()
        return
    if print_type == "PLAIN_OUTPUT_WS":
        print()
        return
    if print_type == "ERROR":
        print()
        return
    if print_type == "MESSAGE_WS":
        print()
        return
    if print_type == "MESSAGE":
        print()
        return
    if print_type == "INSECURE":
        print()
        return
    if print_type == "INSECURE_WS":
        print()
        return
    if print_type == "OUTPUT":
        print()
        return
    if print_type == "OUTPUT_WS":
        print()
        return
    if print_type == "SECURE_WS":
        print()
        return
    if print_type == "SECURE":
        print()
        return


def isNewInstallation() -> bool:
    if not os.path.exists(rootDir):
        myPrint("Thank you for installing APKEnum", "OUTPUT_WS")
        os.mkdir(rootDir)
        return True
    else:
        return False


def isValidPath(apkFilePath):
    global apkFileName
    myPrint("I: Checking if the APK file path is valid.", "INFO_WS")
    if not os.path.exists(apkFilePath):
        myPrint("E: Incorrect APK file path found. Please try again with correct file name.", "ERROR")
        print
        exit(1)
    else:
        myPrint("I: APK File Found.", "INFO_WS")
        apkFileName = ntpath.basename(apkFilePath)


def printList(lst):
    counter = 0
    for item in lst:
        counter = counter + 1
        entry = str(counter) + ". " + item
        myPrint(entry, "PLAIN_OUTPUT_WS")


def reverseEngineerApplication(apkFileName):
    global projectDir
    myPrint("I: Initiating APK decompilation process", "INFO_WS")
    projectDir = rootDir + apkFileName + "_" + hashlib.md5().hexdigest()
    if os.path.exists(projectDir):
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         myPrint(
            "I: The APK is already decompiled. Skipping decompilation and proceeding with scanning the application.",
            "INFO_WS",
        )
        return projectDir
    os.mkdir(projectDir)
    myPrint("I: Decompiling the APK file using APKtool.", "INFO_WS")
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#     result = os.system(
# [BATCHFIX] Commented metadata/non-Python
# #         "java -jar"  # [BATCHFIX] closed string
        + apktoolPath
# [BATCHFIX] Commented metadata/non-Python
# #         + " d"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #         + "--output"  # [BATCHFIX] closed string
        + '"'
        + projectDir
# [BATCHFIX] Commented metadata/non-Python
# #         + "/apktool/"  # [BATCHFIX] closed string
        + '"'
        '"""'+ ' "'
        + apkFilePath
        + '"'
#         + ">/'"""'dev/null
    )
    if result != 0:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         myPrint(
# [BATCHFIX] Commented metadata/non-Python
# #             "E: Apktool failed with exit status " + str(result) + ". Please try updating the APKTool binary.", "ERROR"  # [BATCHFIX] closed string
        )
        print
        exit(1)
    myPrint("I: Successfully decompiled the application. Proceeding with scanning code.", "INFO_WS")


def findS3Bucket(line):
    temp = re.findall(s3Regex1, line)
    if len(temp) != 0:
        for element in temp:
            s3List.append(element)

    temp = re.findall(s3Regex2, line)
    if len(temp) != 0:
        for element in temp:
            s3List.append(element)

    temp = re.findall(s3Regex3, line)
    if len(temp) != 0:
        for element in temp:
            s3List.append(element)


def findGoogleAPIKeys(line):
    temp = re.findall(gMapsAPI, line)
    if len(temp) != 0:
        for element in temp:
            gmapKeys.append(element)


# def findUnrestrictedGmapKeys():
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # # 	response=[]
# 	for key in gmapKeys:
# 		for url in gmapURLs:
# 			try:
# 				response = requests.get(url+key)
# 			except requests.exceptions.ConnectionError as e:
# 				myPrint("I: Connection error while finding network calls","INFO")
# 			except Exception:
# 				continue
# 		if response.status_code == 200:
# 				unrestrictedGmapKeys.append(key)
# 		continue


def findS3Website(line):
    temp = re.findall(s3Website1, line)
    if len(temp) != 0:
        for element in temp:
            s3WebsiteList.append(element)

    temp = re.findall(s3Website2, line)
    if len(temp) != 0:
        for element in temp:
            s3WebsiteList.append(element)


def findUrls(line):
    temp = re.findall(urlRegex, line)
    if len(temp) != 0:
        for element in temp:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             authorityList.append(element[0] + "://" + element[1])
            if scopeMode:
                for scope in scopeList:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                     if scope in element[1]:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                         inScopeAuthorityList.append(element[0] + "://" + element[1])


def findPublicIPs(line):
    temp = re.findall(publicIp, line)
    if len(temp) != 0:
        for element in temp:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             publicIpList.append(element[0])


def performRecon():
    global authorityList, inScopeAuthorityList
#     filecontent =
    for dir_path, dirs, file_names in os.walk(rootDir + apkFileName + "_" + hashlib.md5().hexdigest()):
        for file_name in file_names:
            try:
                fullpath = os.path.join(dir_path, file_name)
                fileobj = open(fullpath, mode="r")
                filecontent = fileobj.read()
                fileobj.close()
            except Exception:
                myPrint("E: Exception while reading " + fullpath, "ERROR")

            try:
                # findUrls(filecontent)
                # findPublicIPs(filecontent)
                # findS3Bucket(filecontent)
                # findS3Website(filecontent)
                # findGoogleAPIKeys(filecontent)
                # findUnrestrictedGmapKeys()
                t1 = Thread(target=findUrls, args=(filecontent,))
                t2 = Thread(target=findPublicIPs, args=(filecontent,))
                t3 = Thread(target=findS3Bucket, args=(filecontent,))
                t4 = Thread(target=findS3Website, args=(filecontent,))
                t5 = Thread(target=findGoogleAPIKeys, args=(filecontent,))
                t1.start()
                t2.start()
                t3.start()
                t4.start()
                t5.start()
                t1.join()
                t2.join()
                t3.join()
                t4.join()
                t5.join()
                # t6 = Thread(target=findUnrestrictedGmapKeys, args=())
                # t6.start()
                # t6.join()
            except Exception:
                myPrint("E: Error while spawning threads", "ERROR")


def displayResults():
    global inScopeAuthorityList, authorityList, s3List, s3WebsiteList, publicIpList, gmapKeys, unrestrictedGmapKeys
    inScopeAuthorityList = list(set(inScopeAuthorityList))
    authorityList = list(set(authorityList))
    s3List = list(set(s3List))
    s3WebsiteList = list(set(s3WebsiteList))
    publicIpList = list(set(publicIpList))
    gmapKeys = list(set(gmapKeys))
    unrestrictedGmapKeys = list(set(unrestrictedGmapKeys))

    if len(authorityList) == 0:
        myPrint("\nNo URL found", "INSECURE")
    else:
        myPrint("\nList of URLs found in the application", "SECURE")
        printList(authorityList)

    if scopeMode and len(inScopeAuthorityList) == 0:
        myPrint("\nNo in-scope URL found", "INSECURE")
    elif scopeMode:
        myPrint("\nList of in scope URLs found in the application", "SECURE")
        printList(inScopeAuthorityList)

    if len(s3List) == 0:
        myPrint("\nNo S3 buckets found", "INSECURE")
    else:
        myPrint("\nList of in S3 buckets found in the application", "SECURE")
        printList(s3List)

    if len(s3WebsiteList) == 0:
        myPrint("\nNo S3 websites found", "INSECURE")
    else:
        myPrint("\nList of in S3 websites found in the application", "SECURE")
        printList(s3WebsiteList)

    if len(publicIpList) == 0:
        myPrint("\nNo IPs found", "INSECURE")
    else:
        myPrint("\nList of IPs found in the application", "SECURE")
        printList(publicIpList)

    if len(gmapKeys) == 0:
        myPrint("\nNo Google MAPS API Keys found", "INSECURE")
    else:
        myPrint("\nList of Google Map API Keys found in the application", "SECURE")
        printList(gmapKeys)
        # if (len(unrestrictedGmapKeys)==0):
        # 	myPrint("\nNo Unrestricted Google MAPS API Keys found", "INSECURE")
        # 	return
        # myPrint("\nList of Unrestricted Google Map API Keys found in the application", "SECURE")
        # printList(unrestrictedGmapKeys)

    print()


####################################################################################################


####################################################################################################

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
# print(
    BColors.OKBLUE
#     +

:::'###::::'########::'##:::'##:'########:'##::: ##:'##::::'##:'##::::'##:
::'## ##::: ##.... ##: ##::'##:: ##.....:: ###:: ##: ##:::: ##: ###::'###:"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string
:'##:. ##:: ##:::: ##: ##:'##::: ##::::::: ####: ##: ##:::: ##: ####'####:"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
# '##:::. ##: ########:: #####:::: ######::: ## ## ##: ##:::: ##: ## ### ##:"  # [BATCHFIX] closed string
 #########: ##.....::: ##. ##::: ##...:::: ##. ####: ##:::: ##: ##. #: ##:
 ##.... ##: ##:::::::: ##:. ##:: ##::::::: ##:. ###: ##:::: ##: ##:.:: ##:
 ##:::: ##: ##:::::::: ##::. ##: ########: ##::. ##:. #######:: ##:::: ##:
..:::::..::..:::::::::..::::..::........::..::::..:::.......:::..:::::..::
# #
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#     "+ BColors.OKRED"  # [BATCHFIX] closed string
    + BColors.BOLD
#     +
                  # Developed By Shiv Sahni - @shiv__sahni
# #
    + BColors.ENDC
)

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # if (len(sys.argv) == 2) and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     myPrint('Usage: python APKEnum.py -p/--path <apkPathName> [ -s/--scope "comma, seperated, list"]', "ERROR")
    myPrint("\t-p/--path: Pathname of the APK file", "ERROR")
    myPrint("\t-s/--scope: List of keywords to filter out domains", "ERROR")
    print()
    exit(1)

if len(sys.argv) < 3:
    myPrint("E: Please provide the required arguments to initiate", "ERROR")
    print()
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     myPrint('E: Usage: python APKEnum.py -p/--path <apkPathName> [ -s/--scope "comma, seperated, list"]', "ERROR")
    myPrint("E: Please try again!!", "ERROR")
    print()
    exit(1)

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # if (len(sys.argv) > 4) and (sys.argv[3] == "-s" or sys.argv[3] == "--scope"):
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     scopeString = sys.argv[4].strip()
    scopeList = scopeString.split(",")
    if len(scopeList) != 0:
        scopeMode = True

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # if sys.argv[1] == "-p" or sys.argv[1] == "--path":
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     apkFilePath = sys.argv[2]
    try:
        isNewInstallation()
        isValidPath(apkFilePath)
        reverseEngineerApplication(apkFileName)
        performRecon()
        displayResults()
    except KeyboardInterrupt:
        myPrint("I: Acknowledging KeyboardInterrupt. Thank you for using APKEnum", "INFO")
        exit(0)
myPrint("Thank You For Using APKEnum", "OUTPUT")
