import socket
import requests as req
import json
from time import sleep
import os

ENDPOINT = 'https://api.intra.42.fr'

SEOUL = '29'
C_PISCINE = '9'
piscine_project = {
	'shell-00' : 1255,
	'shell-01' : 1256,
	'c-00' : 1257,
	'c-01' : 1258,
	'c-02' : 1259,
    'c-03' : 1260,
    'c-04' : 1261,
    'c-05' : 1262,
    'c-06' : 1263,
    'c-07' : 1270,
    'c-08' : 1264,
    'c-09' : 1265,
    'c-10' : 1266,
    'c-11' : 1267,
    'c-12' : 1268,
    'c-13' : 1271,
    'exam-00' : 1301,
    'exam-01' : 1302,
    'exam-02' : 1303,
    'exam-final' : 1304,
    'rush-00' : 1308,
    'rush-01' : 1310,
    'rush-02' : 1309,
    'bsq' : 1305
}

#u = os.environ["UID42"]
#s = os.environ["SECRET42"]

# def get_code(uid:str, secret:str):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind((HOST, PORT))
#         print("Hit the 'try this url' button!")
#         s.listen()
#         connection, address = s.accept()
#         with connection:
#             print('Connected by', address)
#             data = connection.recv(128)
#             if not data:
#                 return None
#             else:
#                 return (str(data).split(' ')[1][7:])

def auth():
    uid = None
    secret = None
    # with open("api_auth.txt", 'r') as file:
    # with open("api_auth.txt", 'r' as file:
    with open("/home/bocal/auth.txt", 'r') as file:
        uid = file.readline()[0:-1]
        secret = file.readline()[0:-1]
    return uid, secret

class HttpRequest(object):

    def __init__(self, target: str, session, **kwargs):
        self.url = f"{ENDPOINT}{target}"
        self.session = session
        if "filter" in kwargs:
            self.filter = kwargs["filter"]
        else:
            self.filter = {}
        if "page" in kwargs:
            self.page = kwargs["page"]
        else:
            self.page = {"size": 100, "number": 1}  # MAX size
        if "sort" in kwargs:
            self.sort = kwargs["sort"]
        else:
            self.sort = ""
        if "range" in kwargs:
            self.range = kwargs["range"]
        # Needs to handle kwargs into different parameters

    def parse_params(self):
        if self.filter:
            filtering = '&'.join([f"filter[{key}]={value}" for key, value in self.filter.items()]) + '&'
        else:
            filtering = ""
        page = '&'.join([f"page[{key}]={value}" for key, value in self.page.items()])
        parsed_param = filtering + page
        if self.sort:
            parsed_param += f"&sort={self.sort}"
        ### needs to add range, to reduce number of requests...
        return f"?{parsed_param}"

    def get(self):
        print(self.url + self.parse_params())
        resp = self.session.get(self.url + self.parse_params())
        try:
            resp.raise_for_status()
        except req.exceptions.HTTPError as e:
            print(resp.content)
        return resp.json()

    def put(self, data: json):
        resp = self.session.put(self.url, json=data)
        try:
            resp.raise_for_status()
        except req.exceptions.HTTPError as e:
            print(resp.content)
        return resp

    def post(self, data: json):
        resp = self.session.post(self.url, json=data)
        try:
            resp.raise_for_status()
        except req.exceptions.HTTPError as e:
            print(resp.content)
        return resp

    def patch(self, data: json):
        resp = self.session.patch(self.url, json=data)
        try:
            resp.raise_for_status()
        except req.exceptions.HTTPError as e:
            print(resp.content)
        return resp

    def delete(self):
        resp = self.session.delete(self.url)
        resp.raise_for_status()
        return resp


class Api(object):

    def __init__(self, uid: str, secret: str, req_code: str = None,
                 redirect: str = None, token: str = None):
        self.uid = uid
        self.secret = secret
        self.req_code = req_code
        self.__token = token
        self.redirect = redirect
        if self.__token is None:
            self.__token = self.Authenticate()
        self.session = req.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.__token}"})

    def Authenticate(self):
        if self.req_code:
            # 3 legged authentication
            auth_data = {
                "grant_type": "authorization_code",
                "client_id": self.uid,
                "client_secret": self.secret,
                "code": self.req_code,
                "redirect_uri": self.redirect
            }
        else:
            # 2 legged authentication
            auth_data = {
                "grant_type": "client_credentials",
                "client_id": self.uid,
		"scope": "public profile projects tig",
                "client_secret": self.secret
            }

        resp = req.post("https://api.intra.42.fr/oauth/token", data=auth_data)
        resp.raise_for_status()
        parsed_resp = resp.json()
        return parsed_resp["access_token"]

    #######################################################
    #                    users                            #
    #######################################################

    def users(self, user_id: str = None, **kwargs):
        if user_id:
            target = f"/v2/users/{user_id}"
        else:
            target = "/v2/users"
        return HttpRequest(target, self.session, **kwargs)

    def users_exams(self, user_id: str, **kwargs):
        target = f"/v2/users/{user_id}/exams"
        return HttpRequest(target, self.session, **kwargs)

    def users_slots(self, user_id: str, **kwargs):
        target = f"/v2/users/{user_id}/slots"
        return HttpRequest(target, self.session, **kwargs)

    def users_teams(self, user_id: str, **kwargs):
        target = f"/v2/users/{user_id}/teams"
        return HttpRequest(target, self.session, **kwargs)

    def users_roles(self, user_id: str, **kwargs):
        target = f"/v2/users/{user_id}/roles"

    def users_titles(self, user_id: str, **kwargs):
        target = f"/v2/users/{user_id}/roles"
        return HttpRequest(target, self.session, **kwargs)

    def users_titlesUsers(self, user_id: str, **kwargs):
        target = f"/v2/users/{user_id}/titles_users"
        return HttpRequest(target, self.session, **kwargs)

    def users_closes(self, user_id: str, **kwargs):
        target = f"/v2/users/{user_id}/closes"
        return HttpRequest(target, self.session, **kwargs)

    def users_groups(self, user_id: str, **kwargs):
        target = f"/v2/users/{user_id}/groups"
        return HttpRequest(target, self.session, **kwargs)

    def users_groupsUsers(self, user_id: str, **kwargs):
        target = f"/v2/users/{user_id}/groups_users"
        return HttpRequest(target, self.session, **kwargs)

    def users_projectsUsers(self, user_id: str, **kwargs):
        target = f"/v2/users/{user_id}/project_users"
        return HttpRequest(target, self.session, **kwargs)

    def users_cursusUsers(self, user_id: str, **kwargs):
        target = f"/v2/users/{user_id}/cursus_users"
        return HttpRequest(target, self.session, **kwargs)

    #######################################################
    #                      cursus                         #
    #######################################################

    def cursus(self, cursus_id: str = None, **kwargs):
        if cursus_id:
            target = f"/v2/cursus/{cursus_id}"
        else:
            target = "/v2/cursus"
        return HttpRequest(target, self.session, **kwargs)

    def cursus_users(self, cursus_id: str, **kwargs):
        target = f"/v2/cursus/{cursus_id}/users"
        return HttpRequest(target, self.session, **kwargs)

    def cursusUsers(self, cursus_user_id: str = None, **kwargs):
        if cursus_user_id:
            target = f"/v2/cursus_users/{cursus_user_id}"
        else:
            target = f"/v2/cursus_users"
        return HttpRequest(target, self.session, **kwargs)

    def cursus_cursusUsers(self, cursus_id: str, **kwargs):
        target = f"/v2/cursus/{cursus_id}/cursus_users"
        return HttpRequest(target, self.session, **kwargs)

    def cursus_projects(self, cursus_id: str, **kwargs):
        target = f"/v2/cursus/{cursus_id}/projects"
        return HttpRequest(target, self.session, **kwargs)
    
    def cursusUser_fromUserId(self, user_id: str, **kwargs):
        target = f"/v2/users/{user_id}/cursus_users"
        return HttpRequest(target, self.session, **kwargs)
    
    #######################################################
    #                    campus                           #
    #######################################################

    def campus_users(self, campus_id: str, **kwargs):
        target = f"/v2/campus/{campus_id}/users"
        return HttpRequest(target, self.session, **kwargs)

    def campus_exams(self, campus_id: str, **kwargs):
        target = f"/v2/campus/{campus_id}/exams"
        return HttpRequest(target, self.session, **kwargs)

    def campus_locations(self, campus_id, **kwargs):
        target = f"/v2/campus/{campus_id}/locations"
        return HttpRequest(target, self.session, **kwargs)

    #######################################################
    #                    projects users                   #
    #######################################################

    def projectUsers(self, project_user_id: str = None, **kwargs):
        if project_user_id:
            target = f"/v2/projects_users/{project_user_id}"
        else:
            target = "/v2/projects_users"
        return HttpRequest(target, self.session, **kwargs)

    def projects_projectsUsers(self, project_id: str, **kwargs):
        target = f"/v2/projects/{project_id}/projects_users"
        return HttpRequest(target, self.session, **kwargs)

    def projects_register(self, project_id: str, **kwargs):
        target = f"/v2/projects/{project_id}/register"
        return HttpRequest(target, self.session, **kwargs)

    #######################################################
    #                       roles                         #
    #######################################################

    def roles(self, role_id: str = None, **kwargs):
        if role_id:
            target = f"/v2/roles/{role_id}"
        else:
            target = "/v2/roles"
        return HttpRequest(target, self.session, **kwargs)

    def rolesEntities(self, role_id: str = None, **kwargs):
        if role_id:
            target = f"/v2/roles_entities/{role_id}"
        else:
            target = "/v2/roles_entities"
        return HttpRequest(target, self.session, **kwargs)

    def roles_rolesEntities(self, role_id: str, **kwargs):
        target = f"/v2/roles/{role_id}/roles_entities"
        return HttpRequest(target, self.session, **kwargs)

    #######################################################
    #                       groups                        #
    #######################################################

    def groups(self, group_id: str = None, **kwargs):
        if group_id:
            target = f"/v2/groups/{group_id}"
        else:
            target = "/v2/groups"
        return HttpRequest(target, self.session, **kwargs)

    def groups_groupsUsers(self, group_id: str = None, **kwargs):
        if group_id:
            target = f"/v2/groups/{group_id}/groups_users"
        else:
            target = "/v2/groups/{g}"
        return HttpRequest(target, self.session, **kwargs)

    def groupsUsers(self, group_user_id: str = None, **kwargs):
        if group_user_id:
            target = f"/v2/groups_users/{group_user_id}"
        else:
            target = f"/v2/groups_users"
        return HttpRequest(target, self.session, **kwargs)

    #######################################################
    #                       scales                        #
    #######################################################

    def scales(self, **kwargs):
        target = "/v2/scales"
        return HttpRequest(target, self.session, **kwargs)

    #######################################################
    #                   scales_teams                      #
    #######################################################

    def users_scaleTeams(self, user_id: str, **kwargs):
        target = f"/v2/users/{user_id}/scale_teams"
        return HttpRequest(target, self.session, **kwargs)

    def users_scaleTeams_asCorrector(self, user_id: str, **kwargs):
        target = f"/v2/users/{user_id}/scale_teams/as_corrector"
        return HttpRequest(target, self.session, **kwargs)

    def users_scaleTeams_asCorrected(self, user_id: str, **kwargs):
        target = f"/v2/users/{user_id}/scale_teams/as_corrected"
        return HttpRequest(target, self.session, **kwargs)

    #######################################################
    #                    evaluations                      #
    #######################################################

    def feedbacks(self, feedback_id: str = None, **kwargs):
        if feedback_id:
            target = f"/v2/feedbacks/{feedback_id}"
        else:
            target = "/v2/feedbacks"
        return HttpRequest(target, self.session, **kwargs)

    #######################################################
    #                       teams                         #
    #######################################################

    def teams(self, team_id: str = None, **kwargs):
        if team_id:
            target = f"/v2/teams/{team_id}"
        else:
            target = "/v2/teams"
        return HttpRequest(target, self.session, **kwargs)

    #######################################################
    #                  user_candidatures                  #
    #######################################################

    def userCandidatures(self, candid_id: str = None, **kwargs):
        if candid_id:
            target = f"/v2/user_candidatures/{candid_id}"
        else:
            target = f"/v2/user_candidatures"
        return HttpRequest(target, self.session, **kwargs)

    def user_candidatures(self, user_id: str, **kwargs):
        target = f"/v2/users/{user_id}/user_candidature"
        return HttpRequest(target, self.session, **kwargs)

    #######################################################
    #                       levels                         #
    #######################################################

    def levels(self, cursus_id: str = None, **kwargs):
        if cursus_id:
            target = f"/v2/cursus/{cursus_id}/levels"
        else:
            target = "/v2/levels"
        return HttpRequest(target, self.session, **kwargs)

    ########################################################

    def path(self, path: str, **kwargs):
        target = f"/v2/{path}"
        return HttpRequest(target, self.session, **kwargs)

    def pisciners(self, piscine_year: str, piscine_month: str):
        target = f"/v2/campus/{SEOUL}/users"
        filter={"pool_year": piscine_year, "pool_month": piscine_month}
        idx = 1
        user_data = []
        while True:
            resp = HttpRequest(target, self.session, filter=filter, page={"size": 100, "number": idx}).get()
            if len(resp) < 1:
                break
            user_data = user_data + resp
            idx += 1
            sleep(0.5)
        return user_data

    def active_users(self, cluster: str=None):
        target = f"/v2/campus/{SEOUL}/locations/"
        filter={"active": "true"}
        all_user = []
        return_user = []
        c1 = []
        c2 = []
        c3 = []
        c4 = []
        c5 = []
        c6 = []

        idx = 1
        while True:
            resp = HttpRequest(target, self.session, filter=filter, page={"size": 100, "number": idx}).get()
            if len(resp) < 1:
                break
            user_data = []
            for location in resp:
                user_data.append({"host": location['host'], 'login': location['user']['login'], 'id': location['user']['id']})
            all_user = all_user + user_data
            idx += 1
            sleep(0.5)
        for user in all_user:
            if user['host'].find("c1") > -1:
                c1.append(user)
        for user in all_user:
            if user['host'].find("c2") > -1:
                c2.append(user)
        for user in all_user:
            if user['host'].find("c3") > -1:
                c3.append(user)
        for user in all_user:
            if user['host'].find("c4") > -1:
                c4.append(user)
        for user in all_user:
            if user['host'].find("c5") > -1:
                c5.append(user)
        for user in all_user:
            if user['host'].find("c6") > -1:
                c6.append(user)
        return c1+c2, c3+c4, c5+c6
