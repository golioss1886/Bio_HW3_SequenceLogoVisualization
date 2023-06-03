from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def handle_submit():
    print("??????????????")
    print(request.files, request.form)
    text = request.form['text']
    print(".........")
    file = request.files['file']
    print("!!!!!!!!!!!")
    # You can now handle the text and the file. For example, you could print the text and save the file:
    print(text)
    file_contents = file.read().decode('utf-8')
    print(file_contents)
    # file.save('/path/to/save/' + file.filename)
    return jsonify({'result': 'Success'})

if __name__ == '__main__':
    app.run(debug=True)