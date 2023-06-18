from flask import Flask, render_template, request

app = Flask("server")

@app.route('/')
def index():
    return render_template('text_to_flask.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    # Save the file or process it as needed
    print(file.name)
    file.save(file.filename)
    return 'File uploaded successfully.'

if __name__ == '__main__':
    app.run()
