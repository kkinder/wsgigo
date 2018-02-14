import flask

from wsgigo import AppRouter

#####################################################################
# Main flask app
main_website = flask.Flask('main_website')


@main_website.route("/")
def index():
    return "Hello World! This is my main website."


#####################################################################
# Special app for docs
docs_app = flask.Flask('docs_app')


@docs_app.route('/docs/')
def docs_index():
    return "These are your documentation files."


#####################################################################
# API Wsgi app
api_app = flask.Flask('api_app')


@api_app.route("/api/test")
def api_test():
    return flask.jsonify({'Hello': 'World'})


#####################################################################
# PUT IT ALL TOGETHER
app = AppRouter(default_app=main_website)
app.add_startswith(docs_app, '/docs/')
app.add_hostname(api_app, 'api.local')

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server('', 8000, app)
    print("Serving HTTP on port 8000...\n"
          "Add api.local to your /etc/hosts file pointing to 127.0.0.1 and try one of these URLs:\n"
          "    http://api.local:8000/api/test\n"
          "    http://localhost:8000/\n"
          "    http://localhost:8000/docs/\n"
          "ENJOY!\n\n")

    httpd.serve_forever()
