import os
from os import path
import datetime
import string

import yaml
import jinja2
import markdown


VALID_URL_CHARS = string.ascii_lowercase + "-_"


def sanitize(s):
    s = s.lower().replace(" ", "_")
    return "".join(filter(lambda x: x in VALID_URL_CHARS, s))


def load_yaml(p):
    with open(p) as f:
        return yaml.load(f)


if __name__ == "__main__":
    env = jinja2.Environment(
        loader=jinja2.PackageLoader("website"),
        autoescape=jinja2.select_autoescape(["html", "xml"])
    )

    env.filters["sanitize"] = sanitize
    env.filters["md"] = lambda s: jinja2.Markup(markdown.markdown(s))

    os.makedirs("out", exist_ok=True)
    template_index = env.get_template("index.html")
    with open("out/index.html", "w") as f:
        f.write(template_index.render(**load_yaml("content/index.yaml")))

    os.makedirs("out/cv", exist_ok=True)
    template_cv = env.get_template("cv.html")
    with open("out/cv/index.html", "w") as f:
        f.write(template_cv.render(**load_yaml("content/cv.yaml")))

    os.makedirs("out/blog", exist_ok=True)
    template_post = env.get_template("post.html")

    posts = filter(lambda x: not path.isfile(x), os.listdir("content/posts"))
    posts = map(lambda x: load_yaml("content/posts/" + x), posts)
    posts = filter(lambda x: x.get("released", False), posts)
    posts = list(sorted(posts, key=lambda x: x["release_date"], reverse=True))

    for i in posts:
        url = i["url"]
        assert url == sanitize(url)
        os.makedirs("out/blog/" + url, exist_ok=True)
        with open("out/blog/" + url + "/index.html", "w") as f:
            f.write(template_post.render(posts=posts, **i))

    template_posts = env.get_template("posts.html")
    with open("out/blog/index.html", "w") as f:
        f.write(template_posts.render(posts=posts))
