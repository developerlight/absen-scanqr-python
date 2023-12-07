const scanner = new Html5QrcodeScanner('reader', {
    qrbox: {
        width: 250,
        height: 250,
    },
    fps: 20,
});

const startScanButton = document.getElementById('startScanButton');
const resultDiv = document.getElementById('result');
const readerDiv = document.getElementById('reader');
const listSiswa = document.getElementById('listSiswa');

startScanButton.addEventListener('click', () => {
    startScanButton.style.display = 'none';
    readerDiv.style.display = 'block';
    // scanner.render(success, error);
    setInterval(scanner.render(success, error), 5000000);
});

function success(result) {
    const dataToSend = { scannedData: result };

    fetch('/absensii', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend),
    })
    .then(response => response.json())
    .then(data => {
        const date = data['data'][0]['date'];
        const arr = data['data'][0]['data_absensi'];

        // Bersihkan elemen <ul> sebelum menambahkan data baru
        listSiswa.innerHTML = '';

        arr.forEach(function(item) {
            var li = document.createElement('li');
            li.textContent = item;
            li.id = 'hasil_scan';
            listSiswa.appendChild(li);
        });

        resultDiv.innerHTML = `
            <h2>Success!</h2>
            <p href="${result}">${result}</p>
            <p>${JSON.stringify(data.message)}</p>
        `;
        scanner.clear();
        readerDiv.style.display = 'none'; // Matikan tampilan kamera
        startScanButton.style.display = 'block'; // Tampilkan tombol "Start Scan" kembali
        
        // Tampilkan notifikasi berhasil
        showNotification('Scan QR berhasil!', 'success');
    })
    .catch(error => {
        console.error(error);

        // Tampilkan notifikasi ketika terjadi kesalahan
        showNotification('Terjadi kesalahan saat mengirim data.', 'error');
    });
}

function error(err) {
    console.error(err);

    // Tampilkan notifikasi ketika terjadi kesalahan
    showNotification('Terjadi kesalahan saat melakukan scanning.', 'error');
}

// Fungsi untuk menampilkan notifikasi
function showNotification(message, type) {
    const notificationDiv = document.getElementById('notification');
    notificationDiv.innerHTML = `<div class="${type}">${message}</div>`;

    // Hilangkan notifikasi setelah beberapa detik (opsional)
    setTimeout(() => {
        notificationDiv.innerHTML = '';
    }, 3000); // Hilangkan notifikasi setelah 3 detik (3000 milidetik)
}


function error(err) {
    console.error(err);
}