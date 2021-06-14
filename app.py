from flask import Flask, render_template, request, flash
import random, string, subprocess, sys, os, secrets

app = Flask(__name__)
secret = secrets.token_urlsafe(16)
app.secret_key = secret

#for ide
@app.route('/')
def ide():
    flash("Note: C and C++ codes can't be run temprorily. Sorry for inconvenience :(")
    return render_template('ide/ide.html')

#for compiler
@app.route('/compiler', methods=['GET', 'POST'])
def compiler():
    if request.method == 'POST':
        language = request.form['language']
        code = request.form['code']
        input = request.form['input']
        filename = ''.join(random.choice(string.ascii_letters+'_'+string.digits) for _ in range(10))

        inputFile = f'static/ide/temp/{filename}.txt'
        inputFile_obj = open(inputFile, 'w')
        inputFile_obj.write(input)
        inputFile_obj.close()
    
        file = f'static/ide/temp/{filename}.{language}'
        file_obj = open(file, 'w')
        file_obj.write(code)
        file_obj.close()

        if language == 'c':
            exe = subprocess.Popen(["gcc", file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = exe.communicate()
            if exe.returncode == 0:
                sys.stdin = open(inputFile, 'r')
                CompletedProcess = subprocess.run('./a.exe', capture_output=True, text=True, stdin=sys.stdin)
                sys.stdin.close()
                output = CompletedProcess.stdout
                os.remove(file)
                os.remove(inputFile)
                return output
            os.remove(file)
            os.remove(inputFile)
            return stderr


        if language == 'cpp':
            exe = subprocess.Popen(["g++", file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = exe.communicate()
            if exe.returncode == 0:
                sys.stdin = open(inputFile, 'r')
                CompletedProcess = subprocess.run('./a.exe', capture_output=True, text=True, stdin=sys.stdin)
                sys.stdin.close()
                output = CompletedProcess.stdout
                os.remove(file)
                os.remove(inputFile)
                return output
            os.remove(file)
            os.remove(inputFile)
            return stderr
            

        if language == 'py':
            sys.stdin = open(inputFile, 'r')
            CompletedProcess = subprocess.run(['python', file], capture_output=True, text=True, stdin=sys.stdin)
            sys.stdin.close()
            if CompletedProcess.returncode == 0:
                output = CompletedProcess.stdout
                os.remove(file)
                os.remove(inputFile)
                return output
            else:
                output = CompletedProcess.stderr
                os.remove(file)
                os.remove(inputFile)
                return output

@app.route('/about')
def about():
    return  render_template("about.html")


@app.route('/aboutme')
def aboutme():
    return render_template("about_me.html")

if __name__ == "__main__":
    app.run(debug=True, port=1000)
        