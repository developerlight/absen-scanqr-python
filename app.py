from flask import Flask, request, render_template, jsonify
from datetime import datetime
import cv2
import qrcode

app = Flask(__name__)

data_siswa = [
    {
        'nama': 'siswa 1',
        'kelas': '7'
    },
    {
        'nama': 'siswa 2',
        'kelas': '7'
    },
    {
        'nama': 'siswa 3',
        'kelas': '7'
    }
]

absen = []  # List untuk menyimpan nama-nama yang sudah absen
data_absen = []  # List untuk menyimpan data absensi

@app.route('/scan_qr', methods=['GET'])
def scan_qr():
    return render_template('scan_qr.html')

@app.route('/process_qr', methods=['POST'])
def process_qr():
    # Inisialisasi kamera
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if ret:
            # Membaca QR Code dari frame
            decoded_objects = qrcode.decode(frame)
            if decoded_objects:
                # Mendapatkan data QR Code
                qr_data = decoded_objects[0].data.decode('utf-8')

                # Menutup kamera
                cap.release()
                cv2.destroyAllWindows()

                # Memproses data QR Code
                nama = qr_data
                print(nama)
                tgl_sekarang = datetime.now()
                tgl_format = tgl_sekarang.strftime('%A, %d %B %Y')

                # Periksa apakah nama ada di daftar siswa
                siswa_terdaftar = False
                for siswa in data_siswa:
                    if siswa['nama'] == nama:
                        siswa_terdaftar = True
                        break

                if not siswa_terdaftar:
                    return 'Nama tidak terdaftar sebagai siswa'
                
                if nama in absen:
                    return 'Siswa sudah melakukan absensi'
                else:
                    absen.append(nama)
                    data_exists = False
                    for data in data_absen:
                        if data['date'] == tgl_format:
                            data['data_absensi'] = absen
                            data_exists = True
                            break
                    if not data_exists:
                        data_absen.append({
                            'date': tgl_format,
                            'data_absensi': absen
                        })
                    return f"Absensi berhasil disimpan untuk: {nama}"

        return 'QR Code tidak terdeteksi'


@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/absensi', methods=['GET', 'POST'])
def absensi():
    if request.method == 'POST':
        nama = request.form['nama']

        if nama:
            tgl_sekarang = datetime.now()
            tgl_format = tgl_sekarang.strftime('%A, %d %B %Y')

            # Periksa apakah nama ada di daftar siswa
            siswa_terdaftar = False
            for siswa in data_siswa:
                if siswa['nama'] == nama:
                    siswa_terdaftar = True
                    break

            if not siswa_terdaftar:
                return 'Nama tidak terdaftar sebagai siswa'
            
            if nama in absen:
                return 'Siswa sudah melakukan absensi'
            else:
                absen.append(nama)
                data_exists = False
                for data in data_absen:
                    if data['date'] == tgl_format:
                        data['data_absensi'] = absen
                        data_exists = True
                        break
                if not data_exists:
                    data_absen.append({
                        'date': tgl_format,
                        'data_absensi': absen
                    })
                # return data_absen
                return f"Absensi berhasil disimpan untuk: {nama}"
        else:
            return "Nama tidak boleh kosong."

    return render_template('absensi.html', data_absen=data_absen)

@app.route('/absensii', methods=['GET','POST'])
def absensii():
    if request.method == 'POST':
        data = request.get_json()
        scanned_data = data.get('scannedData')

        if scanned_data:
            tgl_sekarang = datetime.now()
            tgl_format = tgl_sekarang.strftime('%A, %d %B %Y')

            # Periksa apakah data QR Code sesuai dengan nama siswa
            siswa_terdaftar = False
            for siswa in data_siswa:
                if siswa['nama'] == scanned_data:
                    siswa_terdaftar = True
                    break

            if not siswa_terdaftar:
                return jsonify({'message': 'Nama tidak terdaftar sebagai siswa'})
            
            if scanned_data in absen:
                return jsonify({'message': 'Siswa sudah melakukan absensi'})
            else:
                absen.append(scanned_data)
                data_exists = False
                for data in data_absen:
                    if data['date'] == tgl_format:
                        data['data_absensi'] = absen
                        data_exists = True
                        break
                if not data_exists:
                    data_absen.append({
                        'date': tgl_format,
                        'data_absensi': absen
                    })
                return jsonify({
                    'message': f"Absensi berhasil disimpan untuk: {scanned_data}", 
                    'data': data_absen
                    })
        else:
            return jsonify({'message': 'Data QR Code kosong'})
    
    return render_template('index.html')

def generate_qr(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

@app.route('/generate_qrcode', methods=['GET', 'POST'])
def generate_qr_code():
    qr_data = {"nama": "", "matkul": ""}
    if request.method == 'POST':
        nama = request.form['nama']
        kelas = request.form['kelas']
        qr_data = {"nama": nama, "kelas": kelas}
        data_siswa.append(qr_data)
        filename = 'static/qrcode.png'
        generate_qr(nama, filename)

    return render_template('generate_qr.html', qr_data=qr_data)

if __name__ == '__main__':

    app.run(host = '0.0.0.0', port=5000, debug=True)
