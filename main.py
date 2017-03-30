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
import webapp2
import cgi

indexHeader = """
<!DOCTYPE html>
<html>
<head>
    <title>User-Signup</title>
    <style>
        span.error {
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


class Index(webapp2.RequestHandler):

    """Handles requests coming in to '/' """
    def get(self):


        userNameForm = """
        <form method ="post">
            <table>
                <tbody>
                    <tr>
                        <td>
                            <label for="username">Username</label>
                        </td>
                        <td>
                            <input name="username" type="text" value required>"""
        userNameErrorSpan = ""
        userNameErrorMsg = self.request.get('userNameError')
        if userNameErrorMsg:
            userNameErrorSpan = "<span class='error'>" + cgi.escape(userNameErrorMsg) + "</span>"
        passwordForm = """

                        </td>
                    </tr>

                    <tr>
                        <td>
                            <label for="password">Password</label>
                        </td>
                        <td>
                            <input name="password" type="password" value required>
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <label for="verifyPassword">Verify Password</label>
                        </td>
                        <td>
                            <input name="verifyPassword" type="password" value required>"""
        passwordErrorSpan = ""
        passwordErrorMsg = self.request.get('passwordError')
        if passwordErrorMsg:
                passwordErrorSpan = "<span class='error'>" + cgi.escape(passwordErrorMsg) + "</span>"
        emailForm = """

                            <span class="error"></span>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="email">Email (optional)</label>
                        </td>
                        <td>
                            <input name="email" type="email">
                            <span class="error"></span>
                        </td>
                    </tr>
                </tbody>
            </table>
            <input type="submit">
        </form>
        """
#must have seperate error castings so that the proper error lands in proper location?



        formContent = indexHeader + userNameForm + userNameErrorSpan + passwordForm + passwordErrorSpan + emailForm + indexFooter
        self.response.write(formContent)
    def post(self):
        #looks inside the request to see what the user typed into form

        user_Name = self.request.get("username")

        if " " in user_Name:
            self.redirect('/?userNameError= Please enter valid Username that contains no spaces.')

        user_Email = self.request.get("email")

        user_Password = self.request.get("password")

        user_VerifyPassword = self.request.get("verifyPassword")

        if user_Password != user_VerifyPassword:
            self.redirect('/?passwordError= Passwords must match.')





app = webapp2.WSGIApplication([
    ('/', Index)
], debug=True)
