#    This file is part of JarJar9.
#
#    JarJar9 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    JarJar9 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with JarJar9.  If not, see <http://www.gnu.org/licenses/>.

import hashlib, urllib2, json, os
from Helpers import Helpers

class JJB9:
    def __init__(self):
        self.h = Helpers()
        self.board = [[' ' for x in range(15)] for x in range(15)]
        self.staticTiles = [[0 for x in range(15)] for x in range(15)]

    def getLetterPoints(self, ruleset):
        assert(self.cookie != None)
        url         = "http://game03.wordfeud.com/wf/tile_points/%s/" % ruleset
        messageJSON = "{}"

        response = self.h.doPost(url, self.cookie, messageJSON)
        response = json.loads(response.read())
        self.h.setLetterPoints(response['content']['tile_points'])

        self.h.debug(response)

    def setStaticTiles(self, number):
        assert(self.cookie != None)
        url         = "http://game03.wordfeud.com/wf/board/%s/" % number
        messageJSON = "{}"

        response = self.h.doPost(url, self.cookie, messageJSON)
        response = json.loads(response.read())
        self.staticTiles = response['content']['board']
        self.h.debug(response)

    def sendMessage(self, game, message):
        assert(self.cookie != None)
        url         = "http://game03.wordfeud.com/wf/game/%s/chat/send/" % game
        messageJSON = "{\"message\": \"%s\"}" % message

        response = self.h.doPost(url, self.cookie, messageJSON)
        self.h.debug(response.read())
    
    """
    Returns a list of games
    """
    def getGames(self):
        assert(self.cookie != None)
        url         = "http://game03.wordfeud.com/wf/user/games/"
        message     = ""
        response    = self.h.doPost(url, self.cookie, message).read()
        return json.loads(response)['content']['games']

    def getGame(self, game):
        assert(self.cookie != None)
        url         = "http://game06.wordfeud.com/wf/game/%s/" % game
        message     = ""
        response    = self.h.doPost(url, self.cookie, message)
        response    = response.read()
        js          = json.loads(response)
        content     = js['content']['game']
        board       = content['tiles']
        staticTiles = content['board']
        ruleSet     = content['ruleset']
       
        self.setStaticTiles(staticTiles)
        self.getLetterPoints(ruleSet)
        self.buildBoard(board)
        self.h.printBoard(self.board)

        return response

    def buildBoard(self, newBoard):
        for w in newBoard:
            self.board[w[1]][w[0]] = w[2]

    def playPieces(self, game, moves):
        assert(self.cookie != None)
        words = self.h.getWords(moves, self.board)
        url         = "http://game06.wordfeud.com/wf/game/%s/move/" % game
        message     = { 'words'     : words,
                        'ruleset'   : 4,
                        'move'      : moves }
        message = json.dumps(message)
        self.h.debug(message)
        response    = self.h.doPost(url, self.cookie, message)
        return response.read()


    # Sets proper member variables on successful login, throws exception on failed 
    # login.
    def login(self, email, password):
        url = "http://game03.wordfeud.com/wf/user/login/email/"
        data = "{\"password\": \"%s\",\
                 \"email\": \"%s\"}" % (password, email)
        response = self.h.doPost(url, {}, data)
        dictedResponse = json.loads(response.read())
        if (dictedResponse['status'] == 'success'):
            cookie = self.h.getCookie(response.info().headers)
            self.cookie     = {"Cookie" : "%s=%s" % (cookie[0],cookie[1])}
            content         = dictedResponse['content']
            self.uid        = content['id']
            self.username   = content['username']
            self.email      = content['email']
            self.h.debug(self.cookie)
            self.h.debug(dictedResponse)
            self.h.debug(self.uid)
        else:
            raise Exception("Login failed: %s" % dictedResponse)
