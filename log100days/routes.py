# -*- coding: utf-8 -*-

"""Defines possible URLs and their functions."""

# Thrid-Party Imports
import aiohttp
from markdown2 import markdown
from markupsafe import escape
from quart import render_template

# First-Party Imports
from log100days import app


@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    """Render index template."""
    return render_template("home.html.j2")


def safely_render_markdown(raw):
    """
    Render raw markdown securely into HTML.

    HTML contained in the input string is sanitized.

    :param raw: Raw Markdown formatted string
    :type raw: string

    :returns: HTML string created form Markdown
    :rtype: string
    """
    safe_markdown = escape(raw)
    return markdown(safe_markdown)


@app.route("/<string:markdownfile>.md")
async def render_log_repo_markdown_file_in_site(markdownfile):
    """Render markdown file from journal repo as save HTML in base template."""
    file_url = (
        "https://raw.githubusercontent.com/tbrlpld/"
        + "100-days-of-code/master/"
        + markdownfile
        + ".md"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            markdown_content = await response.text(encoding="utf8")

    rendered_content = safely_render_markdown(markdown_content)
    return await render_template(
        "rendered_content.html.j2",
        rendered_content=rendered_content,
        pagetitle=markdownfile.title(),
    )
