import cv2
import os
from werkzeug.utils import secure_filename
from flask import Flask,request,render_template, send_file, Blueprint

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)

UPLOAD_FOLDER = '/home/johurul/temp/flask/temp/spitfire/static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def make_sketch(img):
    grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(grayed)
    blurred = cv2.GaussianBlur(inverted, (19, 19), sigmaX=0, sigmaY=0)
    final_result = cv2.divide(grayed, 255 - blurred, scale=256)
    return final_result

def make_grey(img):
    greyed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    return greyed

def make_resize(img,w,h):
    resized = cv2.resize(img,(int(w),int(h)))
    
    return resized


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sketch')
def sketch():
    return render_template('sketch.html')

@app.route('/grey')
def grey():
    return render_template('grey.html')

@app.route('/resize')
def resize():
    return render_template('resize.html')


@app.route('/sketched',methods=['POST'])
def sketched():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img = cv2.imread(UPLOAD_FOLDER+'/'+filename)
        sketch_img = make_sketch(img)
        sketch_img_name = filename.split('.')[0]+"_sketch.jpg"
        _ = cv2.imwrite(UPLOAD_FOLDER+'/'+sketch_img_name, sketch_img)
        return render_template('sketch.html',org_img_name=filename,sketch_img_name=sketch_img_name)

@app.route('/greyed',methods=['POST'])
def greyed():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img = cv2.imread(UPLOAD_FOLDER+'/'+filename)
        grey_img = make_grey(img)
        grey_img_name = filename.split('.')[0]+"_greyscale.jpg"
        _ = cv2.imwrite(UPLOAD_FOLDER+'/'+grey_img_name, grey_img)
        return render_template('grey.html',org_img_name=filename,grey_img_name=grey_img_name)

@app.route('/resized',methods=['POST'])
def resized():
    file = request.files['file']
    w=request.form['w']
    h=request.form['h']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img = cv2.imread(UPLOAD_FOLDER+'/'+filename)
        (wh,hi,de) = img.shape
        resize_img = make_resize(img,w,h)
        resize_img_name = filename.split('.')[0]+"_"+str(w)+"X"+str(h)+"_resize.jpg"
        _ = cv2.imwrite(UPLOAD_FOLDER+'/'+resize_img_name, resize_img)
        return render_template('resize.html',org_img_name=filename,resize_img_name=resize_img_name,wh=wh,hi=hi,w=w,h=h)


@app.route('/download', methods=['POST'])
def download_file():
    img = request.form['download']
    p = f'/home/johurul/temp/flask/temp/spitfire/static/uploads/{img}'
    return send_file(p, as_attachment=True)





if __name__ == '__main__':
    app.run(debug=True)
