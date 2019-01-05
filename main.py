from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Build-A-Blog:123456@localhost:8889/Build-A-Blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    post = db.Column(db.Text)

    def __init__(self, title, post):
        self.title = title
        self.post = post 


@app.route('/', methods=["POST", "GET"])
def show_blog():
    post_id = request.args.get('id')
    if post_id:
        blog = Blog.query.get(post_id)
        return render_template('single_post.html', blog=blog, title="Single Post")
    else:
        
        all_blog_posts = Blog.query.all()
        
        return render_template('blog.html', all_blog_posts=all_blog_posts, title="All Blog")

@app.route('/newpost', methods=['GET', 'POST'])
def add_entry():

    if request.method == 'POST':

        title_error = ""
        blog_entry_error = ""

        post_title = request.form['blog_title']
        post_entry = request.form['blog_post']
        post_new = Blog(post_title, post_entry)

        if post_title and post_entry:
            db.session.add(post_new)
            db.session.commit()
            post_link = "/?id=" + str(post_new.id)
            return redirect(post_link)
        else:
            if not post_title and not post_entry:
                title_error = "Please enter text for blog title"
                blog_entry_error = "Please enter text for blog entry"
                return render_template('new_post.html', blog_entry_error=blog_entry_error, title_error=title_error)
            elif not post_title:
                title_error = "Please enter text for blog title"
                return render_template('new_post.html', title_error=title_error, post_entry=post_entry)
            elif not post_entry:
                blog_entry_error = "Please enter text for blog entry"
                return render_template('new_post.html', blog_entry_error=blog_entry_error, post_title=post_title)

    # DISPLAYS NEW BLOG ENTRY FORM
    else:
        return render_template('new_post.html')
        

if __name__ == '__main__':
    app.run()