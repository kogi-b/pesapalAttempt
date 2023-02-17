import os
import shutil
import markdown
from jinja2 import Environment, FileSystemLoader


def generate_post_routes(input_dir):
    '''This function generates routes which will be used to create links to all posts.
    The function returns a list of dictionaries containing the name and the relative path of the post.'''
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
    '''This function creates the index page, it parses the markdown and uses the list of routes to generate links to the posts dynamically.'''
    index_content = read_markdown(os.path.join(input_dir, "index.md"))
    index_html = index_template.render(
        title=index_content["title"], content=index_content["html"], routes=routes)
    render_page(base_template, index_html,
                os.path.join(output_dir, "index.html"))


def main():
    # we initialize the input directory to a folder named content.
    input_dir = "content" 

    # we initialize the output directory to a folder named output.
    output_dir = "output"

    # this is the location of the templates.
    templates_dir = "templates"

    # this is the location of the static files.
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
    

    # Generating the article pages
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
