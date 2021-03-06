#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
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
#

 #TODO:DONE impliment regular expressions for input (bottom of udacity page)
 #TODO:DONE multiple errors show all their messages on the same redirect
 #TODO:DONE preserve user imput through redirect (string substitution?



import webapp2
import cgi
import re
#HTML saved into variable
indexHeader = """
<!DOCTYPE html>
<html>
<head>
    <title>User-Signup</title>
    <style>
        span.error {
            color:red;
        }
        div.error {
            color:red;
        }
    </style>
</head>
<body>
    <h1>Signup</h1>
"""
indexFooter = """
</body>
</html>
"""


#Main form for signup page

form = """
<form method ="post">
    <table>
        <tbody>
            <tr>
                <td>
                    <label for="username">Username</label>
                </td>
                <td>
                    <input name="username" type="text" value="%(username)s">
                    <span class='error'>%(userNameErrorMsg)s</span>
                </td>
            </tr>

            <tr>
                <td>
                    <label for="password">Password</label>
                </td>
                <td>
                    <input name="password" type="password" value required value="%(password)s">
                    <span class='error'>%(passwordErrorMsg)s</span>
                </td>
            </tr>

            <tr>
                <td>
                    <label for="verifyPassword">Verify Password</label>
                </td>
                <td>
                    <input name="verifyPassword" type="password" value required value="%(verifyPassword)s">
                    <span class='error'>%(verifyPasswordErrorMsg)s</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="email">Email (optional)</label>
                </td>
                <td>
                    <input name="email" type="text" value="%(email)s">
                    <span class="error">%(emailErrorMsg)s</span>
                </td>
            </tr>
        </tbody>
    </table>
    <input type="submit">
</form>"""

#RE checks various requirements for inputs
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)
#no spaces, no characters(?), 3<
PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)
#3<
MAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return MAIL_RE.match(email)

def passwordsMatch(password, verifyPassword):
    if password == verifyPassword:
        passwordVerified = True
    else:
        passwordVerified = False

#variable that contains HTML code
formContent = indexHeader + form + indexFooter

#handles '/'
class Index(webapp2.RequestHandler):

    def get(self):

        self.write_form_includes_Errors()
#includes error information and user input information in form space
    def write_form_includes_Errors(self, userNameErrorMsg="", passwordErrorMsg ="", emailErrorMsg="", verifyPasswordErrorMsg="", username="", password="", verifyPassword="", email=""):

        self.response.out.write(formContent % {"userNameErrorMsg": userNameErrorMsg, "passwordErrorMsg": passwordErrorMsg, "emailErrorMsg": emailErrorMsg, "verifyPasswordErrorMsg": verifyPasswordErrorMsg, "username": cgi.escape(username), "password": cgi.escape(password), "verifyPassword": cgi.escape(verifyPassword), "email": cgi.escape(email)})


    def post(self, userNameErrorMsg="", passwordErrorMsg ="", emailErrorMsg="", verifyPasswordErrorMsg="", username="", password="", verifyPassword="", email=""):

#casts escaped user input into variables
        user_Name = cgi.escape(self.request.get("username"))
        user_Email = cgi.escape(self.request.get("email"))
        user_Password = cgi.escape(self.request.get("password"))
        user_VerifyPassword = cgi.escape(self.request.get("verifyPassword"))

#validates above variables using above RE criteria
        validUsername = valid_username(user_Name)
        validEmail = valid_email(user_Email)
        validPassword = valid_password(user_Password)

#checks if user input passed validation f(x)s and flags error messages if they dont
        if validUsername == None:
            userNameErrorMsg = "Please enter valid username."
        if validEmail == None:
            emailErrorMsg = "Please enter valid email."
        if validPassword == None:
            passwordErrorMsg = "Please enter valid password."
        if user_Password != user_VerifyPassword:
            verifyPasswordErrorMsg = "Passwords must match."
#if any input is invalid remakes the form with correct and separate error messages, also preserves username and email input
        if validUsername == None or validEmail == None or validPassword == None or user_Password != user_VerifyPassword:

            self.response.out.write(formContent % {"userNameErrorMsg": userNameErrorMsg, "passwordErrorMsg": passwordErrorMsg, "emailErrorMsg": emailErrorMsg, "verifyPasswordErrorMsg": verifyPasswordErrorMsg, "username": cgi.escape(user_Name), "password": cgi.escape(password), "verifyPassword": cgi.escape(verifyPassword), "email": cgi.escape(user_Email)})
#if all input is valid, sends to '/welcome'***also sends username info for welcome greeting
        else:
            self.redirect("/welcome?username="+user_Name)

class WelcomeHandler(webapp2.RequestHandler):
#welcome pages greets new user with their chosen user name input
#TODO: LAST STEP: cant get "user_Name" into html but its getting the correct value in urlbar
    def get(self):
        postHeader = "<h1>Welcome, " + self.request.get("username") + "!</h1>"
        self.response.out.write(postHeader)



app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', WelcomeHandler,)
], debug=True)
