from flask import Flask, render_template
import re
import os
import numpy

app=Flask(__name__)

@app.route('/')
def run_script():
    file = open(r'./data_process.py', 'r').read()
    exec(file)                                        #excute python script
    from data_process import scr_dic, AffectedBodyPart_flag, Distance_flag
    return render_template("Visuliazation Summary of HazardLog.html", scr_dic =scr_dic,
                           AffectedBodyPart_flag=AffectedBodyPart_flag, Distance_flag=Distance_flag)              #call render_template function, upload html file

if __name__=="__main__":
    app.run(debug=True)