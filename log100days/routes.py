from quart import render_template, redirect
from markdown2 import markdown
from markupsafe import escape
import requests

from log100days import app


@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    return render_template("home.html.j2")


def safely_render_markdown(raw):
    """
    Render raw markdown securely into HTML

    HTML contained in the input string is sanitized.

    :param raw: Raw Markdown formatted string
    :type raw: string

    :returns: HTML string created form Markdown
    :rtype: string
    """
    safe_markdown = escape(raw)
    return markdown(safe_markdown)


@app.route("/<string:markdownfile>.md")
def render_log_repo_markdown_file_in_site(markdownfile):
    file_URL = ("https://raw.githubusercontent.com/tbrlpld/"
                "100-days-of-code/master/" + markdownfile + ".md")
    request = requests.get(file_URL)
    rendered_content = safely_render_markdown(request.content.decode("utf8"))
    return render_template(
        "rendered_content.html.j2",
        rendered_content=rendered_content,
        pagetitle=markdownfile.title()
    )
