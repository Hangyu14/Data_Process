from flask import Flask, render_template
app=Flask(__name__)

@app.route('/')
def run_script():
    file = open(r'./data_process.py', 'r').read()
    exec(file)                                        #excute python script
    from data_process import img_path_list, document_number
    return render_template("Visuliazation Summary of HazardLog1.html", img_path_list = img_path_list, document_number = document_number)              #call render_template function, upload html file

if __name__=="__main__":
    app.run(debug=True)