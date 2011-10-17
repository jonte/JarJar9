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

class Helpers:
    DEBUG = True
    def getCookie(self, headers):
        for header in headers:
            hs = header.split(": ")
            if hs[0] == "Set-Cookie":
                var, val = hs[1].split(";")[0].split("=")
                return (var,val)

    def doPost(self, url, additionalHeaders, data):
        headers = { "Content-type"  : "application/json",\
                    "Host"          : "game03.wordfeud.com",\
                    "Connection"    : "Keep-Alive",\
                    "User-Agent"    : "WebFeudClient/1.2.8 (Android 2.2.3)",\
                    }
        headers.update(additionalHeaders)
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        return response

    def getSaltedPassword(self):
        f = open(os.path.expanduser("~"+os.sep+".wf_login.txt"), "r")
        f.readline()
        password = f.readline().strip()
        m = hashlib.new("sha1")
        salt = "JarJarBinks9"
        m.update(password+salt)
        return m.hexdigest()

    def getUsername(self):
        f = open(os.path.expanduser("~"+os.sep+".wf_login.txt"),"r")
        return f.readline().strip()

    def debug(self, txt):
        if self.DEBUG:
            print txt

    def prettyPrintGames(self, gameData):
        js = json.loads(gameData)
        if(js['status'] == 'success'):
            c = js['content']
            for game in c['games']:
                print "ID: %s" % game['id']
                print "%s VS %s" % (game['players'][0]['username'], game['players'][1]['username'])
                print

    def printBoard(self, board):
        for row in board:
            if type(row[0]) == type(1):
                sRow = map(str, row)
            else:
                sRow = row
            print ' '.join(sRow)

    def getWords(self, letters, board):
        words = set()
        for (x,y,letter, b) in letters:
            board[y][x] = letter
        
        for (x,y,letter,b) in letters:
            leastX = x
            while leastX >= 0 and board[y][leastX] != ' ':
                leastX -= 1

            wordX = ''
            mostX = leastX+1
            while mostX < 15 and board[y][mostX] != ' ':
                wordX += board[y][mostX]
                mostX += 1
            words.add(wordX)

            leastY = y
            while leastY >= 0 and board[leastY][x] != ' ':
                leastY -= 1

            wordY = ''
            mostY = leastY+1
            while mostY < 15 and board[mostY][x] != ' ':
                wordY += board[mostY][x]
                mostY += 1
            words.add(wordY)
        return filter(lambda x: len(x) > 1, sorted(words))
       
    def setLetterPoints(self, letterPointsDict):
        self.letterPoints = letterPointsDict

    def getLetterPoints(self, letter):
        return self.letterPoints[letter]

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

    def getGames(self):
        assert(self.cookie != None)
        url         = "http://game03.wordfeud.com/wf/user/games/"
        message     = ""
        response    = self.h.doPost(url, self.cookie, message)
        return response.read()

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

