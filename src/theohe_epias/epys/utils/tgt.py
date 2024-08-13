from requests import post, request
from json import dumps
from getpass import getpass
from pwinput import pwinput
import sys

class RequestFunctions():       
    def request_TGT(self, password):
        if password == None:
            password = self.type_password()
            if password == "q":
                print("Exited.")
                self.status  = False
                self.tgt_response = "Exited"
                return None

        self.tgt_request = post(
            self.url, 
            params={
                "username": self.username,
                "password": password,
                "format": "text"
            },
            headers = {
                "Cache-Control": "no-cache",
                "Content-Type": "application/x-www-form-urlencoded"
            })
        
        self.status  = self.check_password()
        self.tgt_response = self.tgt_request.text
        return 

    def type_password(self):
        print("Enter your password: (q for quit)")

        if sys.__stdin__.isatty():
            password = pwinput()
        else:
            password = getpass('Password:')
        return password


    def check_password(self):
        if str(self.tgt_request.status_code)[0] != "2":
            print("Login is failed.")
            print(self.tgt_request.text)
            return False
        else:
            # print("Successful login")
            return True
        
