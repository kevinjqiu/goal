import functools
import flask
# from flask.ext.cors import cross_origin
from flask_cors import cross_origin


def json_response(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        return flask.jsonify(result)
    return wrapper


def v2_route(app, route, *args, **kwargs):
    def decorator(fn):
        return app.route(route, *args, **kwargs)(
            cross_origin()(json_response(fn)))

    return decorator


class MyJSONEncoder(flask.json.JSONEncoder):
    def default(self, o):
        if hasattr(o, '__json__'):
            return o.__json__()
        return super(MyJSONEncoder, self).default(o)


app = flask.Flask(__name__)
app.json_encoder = MyJSONEncoder
