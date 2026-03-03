import math
from flask import Flask, render_template, request




app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    return render_template("index.html")


@app.route('/anagram', methods=['POST'])
def ana():
    anagram = request.form['letters']

    def frequency(inp_word):
        word = inp_word.upper()
        freq = [0 for i in range(26)]
        a_code = ord('A')
        for i in word:
            val = ord(i) - a_code
            if val >= 0 and val <= 25:
                freq[val] += 1
        return freq

    def anagram_check_freq(user, dictionary):
        for i in range(len(user)):
            if user[i] < dictionary[i]:
                return False
        return True

    def anagram_check_word(user, dictionary):
        user_freq = frequency(user)
        res = []
        for i in range(len(dictionary)):
            dict_freq = frequency(dictionary[i])
            if anagram_check_freq(user_freq, dict_freq):
                res.append(dictionary[i])
        return res

    def arrange(words):
        emp_cnt = (8 - len(words) % 8) % 8
        for i in range(emp_cnt):
            words.append("")
        result = ["" for i in range(len(words))]
        for i in range(len(words)):
            index = math.floor(i / 8) + math.floor(len(words) / 8) * (i%8)
            result[i] = words[index]
        return result

    def fixword(word):
        res = ""
        for i in range(len(word)):
            if word[i].isalpha():
                res += word[i]
        return res

    f = open("static/dictionary.txt", 'r')
    o = f.readlines()

    alternatives = o
    string_without_line_breaks = ""
    for line in alternatives:
        stripped_line = line.rstrip()
        string_without_line_breaks += stripped_line
    ko = string_without_line_breaks.split("\t")
    ko = str(ko)
    ko = ko.split(" ")
    f.close()

    ko[0] = fixword(ko[0])
    ko[-1] = fixword(ko[-1])
    
    zomb = anagram_check_word(anagram, ko)
    anag_arr = len(zomb)
    lett = anagram.replace(" ", "")
    clear = len(lett)
    alph = sorted(anagram)
    ttt = "".join(alph).upper()
    zomb = sorted(zomb, key=lambda s: (len(s), s))
    zomb = arrange(zomb)
    result = render_template("index.html", zomb=zomb, anag_arr=anag_arr, lett=lett, ttt=ttt, clear=clear)
    return result

from flask import send_from_directory

@app.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js')

if __name__ == '__main__':
    app.run()
