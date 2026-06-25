from flask import Flask, render_template, request, send_file, jsonify
import os
from huffman import compress_file, decompress_file


app = Flask(__name__)


UPLOAD_FOLDER="uploads"
COMPRESSED_FOLDER="compressed"
DECOMPRESSED_FOLDER="decompressed"


for folder in [UPLOAD_FOLDER,COMPRESSED_FOLDER,DECOMPRESSED_FOLDER]:
    os.makedirs(folder,exist_ok=True)



@app.route("/")
def home():

    return render_template("index.html")



@app.route("/upload",methods=["POST"])
def upload():


    file=request.files["file"]

    path=os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )


    file.save(path)


    size=os.path.getsize(path)


    return jsonify({"success": True, "filename": file.filename, "size": size})



@app.route("/download_compressed/<filename>")
def download_compressed(filename):
    file_path = os.path.join(COMPRESSED_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404

# MODULE 2

@app.route("/compress",methods=["POST"])
def compress():

    filename=request.form["filename"]


    input_path=os.path.join(
        UPLOAD_FOLDER,
        filename
    )


    output_path=os.path.join(
        COMPRESSED_FOLDER,
        filename+".huff"
    )

    if not os.path.exists(input_path):
        return jsonify({"success": False, "error": "Please upload the file first."})


    try:
        ratio=compress_file(
            input_path,
            output_path
        )
        return jsonify({"success": True, "ratio": ratio, "compressed_filename": filename+".huff"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})



# MODULE 3

@app.route("/decompress",methods=["POST"])
def decompress():


    filename=request.form["filename"]


    input_path=os.path.join(
        COMPRESSED_FOLDER,
        filename
    )


    output_path=os.path.join(
        DECOMPRESSED_FOLDER,
        filename.replace(".huff","")
    )


    if not os.path.exists(input_path):
        return f"File not found: {input_path}", 404

    try:
        decompress_file(
            input_path,
            output_path
        )
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return f"Error decompressing: {str(e)}", 500



app.run(debug=True)