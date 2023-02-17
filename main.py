import os
import shutil
import markdown
from jinja2 import Environment, FileSystemLoader


def generate_routes(content_dir):
    routes = []
    for root, _, files in os.walk(content_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                route = {
                    "name": os.path.splitext(file)[0],
                    "url": os.path.relpath(file_path, content_dir).replace("\\", "/").replace(".md", ".html")
                }
                routes.append(route)
    return routes


def generate_post_routes(input_dir):
    posts_dir = os.path.join(input_dir, 'posts')
    post_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(
        posts_dir) for f in filenames if os.path.splitext(f)[1] == '.md']
    routes = []
    for post_file in post_files:
        post_name = os.path.splitext(os.path.basename(post_file))[0]
        route_name = post_name.replace('_', ' ').title()
        route = {'name': route_name, 'url': f'posts/{post_name}.html'}
        routes.append(route)
    return routes


def generate_index_page(input_dir, output_dir, index_template, base_template, routes):
    index_content = read_markdown(os.path.join(input_dir, "index.md"))
    index_html = index_template.render(
        title=index_content["title"], content=index_content["html"], routes=routes)
    render_page(base_template, index_html,
                os.path.join(output_dir, "index.html"))


def main():
    input_dir = "content"
    output_dir = "output"
    templates_dir = "templates"
    static_dir = "static"

    # Copying the static files to the output directory
    shutil.copytree(static_dir, os.path.join(output_dir, static_dir))

    # Loading the templates
    env = Environment(loader=FileSystemLoader(templates_dir))
    index_template = env.get_template("index_routes.html")
    article_template = env.get_template("article.html")
    about_template = env.get_template("about.html")
    not_found_template = env.get_template("404.html")
    base_template = env.get_template("base.html")
    nav_template = env.get_template("base.html")


    routes = generate_post_routes(input_dir)
    print(routes)

    generate_index_page(input_dir, output_dir, index_template, base_template, routes)


    # Generate the about page
    about_content = read_markdown(os.path.join(input_dir, "about.md"))

    about_html = about_template.render(navigation = nav_template,
        title=about_content["title"], content=about_content["html"])

    
    render_page(base_template, about_html,
                os.path.join(output_dir, "about.html"))
    

    # Generate the article pages
    posts_dir = os.path.join(input_dir, "posts")
    for filename in os.listdir(posts_dir):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(posts_dir, filename)
        article_content = read_markdown(filepath)
        article_html = article_template.render(
            title=article_content["title"], content=article_content["html"])
        output_path = os.path.join(
            output_dir, "posts", os.path.splitext(filename)[0] + ".html")
        render_page(base_template, article_html, output_path)

    # Generating the 404 page
    not_found_html = not_found_template.render()
    render_page(base_template, not_found_html,
                os.path.join(output_dir, "404.html"))


def read_markdown(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    md = markdown.Markdown(extensions=["meta"])
    html = md.convert(content)
    return {"title": md.Meta.get("title", ["Untitled"])[0], "html": html}


def render_page(base_template, content_html, output_path):
    output_html = base_template.render(content=content_html)
    with open(output_path, "w") as f:
        f.write(content_html)


if __name__ == "__main__":
    main()
