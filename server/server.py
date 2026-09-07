import os
from flask import Flask, request, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = './files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        student_class = request.form.get('student_class', 'unknown_class')
        student_name = request.form.get('student_name', 'unknown_name')
        
        student_folder_name = f"{student_class}_{student_name}"
        user_dir = os.path.join(UPLOAD_FOLDER, student_folder_name)

        if os.path.exists(user_dir):
            return jsonify({
                "status": "error",
                "message": f"學生 {student_name} 已經繳交過作業！若有需求請聯繫管理員。"
            }), 400 

        os.makedirs(user_dir)
        
        saved_files = []
        for i in range(1, 4):
            file_key = f"prob_{i}"
            if file_key in request.files:
                file_obj = request.files[file_key]
                if file_obj and file_obj.filename != '':
                    save_name = f"P{i}.py"
                    save_path = os.path.join(user_dir, save_name)
                    file_obj.save(save_path)
                    saved_files.append(save_name)

        return jsonify({
            "status": "success",
            "message": f"成功接收 {len(saved_files)} 個檔案！",
            "saved_files": saved_files
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True, use_reloader=False)