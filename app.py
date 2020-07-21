import flask
import time
import random
from flask import request

app = flask.Flask(__name__)

# Returns random act
def get_act(time, ind, act):
    arr = ["Бумага", "Ножницы", "Камень"]
    l = random.randint(-ind, time)
    for i in range(1, time + 1):
        for j in range(1, time % 300 + 1):
            l *= random.randint(-i, j)
        act = arr[abs(l) % 3]
    return act


@app.route("/", methods=["GET", "POST"])
def game():
    resp = None
    # Filter requests
    if request.method == "GET":
        resp = flask.make_response(flask.render_template("index_get.html"))
    else:
        arr = ["Бумага", "Ножницы", "Камень"]
        res = request.values.to_dict()["res"]
        # Get seconds since 20 last minutes
        time_now_sec = int(time.time()) % 1000
        if res in arr:
            # Get ind to make choice more random
            z, tr = 0, True
            while tr:
                if arr[z] == res:
                    tr = False
                z += 1
            z %= 3
            act, ind = arr[z], z
            # Get random choice
            act = get_act(time_now_sec, ind, act)
            d = {"Бумага": "Камень", "Ножницы": "Бумага", "Камень": "Ножницы"}
            # Check results
            if act == res or d[act] == res:
                resp = flask.make_response(flask.render_template("index_post_loose.html"))
            else:
                resp = flask.make_response(flask.render_template("index_post_win.html"))
        else:
            resp = flask.make_response(flask.render_template("index_post_loose.html"))
    return resp


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=False)

