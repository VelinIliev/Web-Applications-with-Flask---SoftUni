from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    context = {
        'name': 'SoftUni',
        'paragraph': 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Labore error, \dolorem sint, nisi quod doloribus eius voluptas atque eveniet sequi molestiae recusandae fugiat minus nostrum nobis consequuntur mollitia eos? A!'}
    return render_template('index.html', **context)


if __name__ == '__main__':
    app.run(debug=True)