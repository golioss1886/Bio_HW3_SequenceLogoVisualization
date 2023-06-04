from flask import Flask, render_template, request, jsonify
import logomaker
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def handle_submit():
    print(request.files, request.form)
    # print("??", text)
    if len(request.files) != 0:
        file = request.files['file']
        file_contents = file.read().decode('utf-8')
        sequences = extract(file_contents)
        # plt.show()
        # print(file_contents)
        # print(len(file_contents))
        # print(type(file_contents))
        # print((file_contents[9])=='\n')
        # return jsonify(img_path)
    elif len(request.form['text']) != 0:
        # print(request.form['text'])
        text = request.form['text']
        sequences = extract(text)
        # print(text)
    print(sequences, "::::::::::::::::::::::::")
    if sequences == []:
        print("[][][:::::::::::::]")
        return jsonify({'error': 'Invalid input'})
    counts_df = logomaker.alignment_to_matrix(sequences)
    prob_df = counts_df.div(counts_df.sum(axis=1), axis=0)
    logo = logomaker.Logo(prob_df, color_scheme='classic')
    logo.ax.set_xlabel('Position')
    logo.ax.set_ylabel('Frequency')
    img_path = "static/sequence_logo.png"
    plt.savefig(img_path, dpi=300) 
    return jsonify(img_path)
    # You can now handle the text and the file. For example, you could print the text and save the file:
    # file.save('/path/to/save/' + file.filename)
    # return jsonify({'result': 'Success'})

def extract(file_contents):
    head = 0
    sequences = []
    for idx, i in enumerate(file_contents):
        if i =='\n' or i == ' ' or idx == len(file_contents)-1:
            print(file_contents[head:idx])
            if len(file_contents)-1 == idx:
                sequences.append(file_contents[head:idx+1])
            else:
                sequences.append(file_contents[head:idx])
            head = idx+1
    print("sequences:",sequences)
    if len(sequences[0]) > 16 or check_string_list_lengths(sequences)==False or len(sequences) > 17:
        print("something is wrong")
        print(len(sequences[0]) > 16)
        print(check_string_list_lengths(sequences)==False)
        print(len(sequences) > 17)
        return []
    return sequences

def check_string_list_lengths(lst):
    print(lst)
    if not lst:  # If the list is empty, return False
        return False
    first_length = len(lst[0])  # Get the length of the first element
    print("first_length:", first_length)
    for element in lst:
        if len(element) != first_length:
            print(len(element),"::::::")
            return False
    return True


if __name__ == '__main__':
    app.run(debug=True)