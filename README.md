1. Permasalahan yang Dihadapi :
Komunikasi antar-microservices sering menjadi sumber bottleneck performa.
REST API meski populer, memiliki overhead JSON yang tinggi.
gRPC menawarkan efisiensi lebih baik, tetapi kurang kompatibel dengan sistem legacy.
Evaluasi performa biasanya statis, tidak mempertimbangkan dinamika workload.

2. Solusi yang Diberikan :
Melakukan eksperimen komparatif antara REST API dan gRPC menggunakan framework MECE.
Mengusulkan Adaptive Communication Protocol Selection Framework untuk melakukan switching protokol secara dinamis.

3. Mengapa Memakai Solusi Tersebut? :
Framework MECE memberikan evaluasi multi-dimensi yang lebih representatif.
Adaptive framework memungkinkan sistem memilih protokol sesuai kondisi workload secara real-time.
Solusi ini menjawab kebutuhan fleksibilitas komunikasi pada arsitektur microservices modern.

4. Improvement yang Diberikan :
Memperkenalkan monitoring module dan decision engine berbasis aturan.
Mengintegrasikan feedback loop agar keputusan switching semakin adaptif.
Memberikan baseline implementasi yang dapat dikembangkan lebih lanjut ke arah machine learning-based decision making.

5. Kekurangan dari Solusi :
Eksperimen dilakukan pada environment lokal, sehingga hasil belum sepenuhnya mencerminkan kondisi produksi.
Implementasi gRPC masih terbatas (menggunakan simulasi), sehingga validitasnya perlu diperluas.
Skala pengujian terbatas pada operasi CRUD sederhana dan belum mencakup workload kompleks.
Belum ada integrasi aspek keamanan dalam framework adaptif.

6. Kesimpulan Implementasi Eksperimen :
REST API unggul pada skenario sederhana, latency rendah, dan integrasi dengan sistem legacy.
gRPC lebih tepat untuk skenario data besar, high concurrency, dan kebutuhan transmisi efisien.
Framework adaptif memungkinkan pemilihan protokol secara dinamis, meningkatkan fleksibilitas sekaligus mengoptimalkan performa komunikasi microservices.
Tidak ada protokol yang sepenuhnya dominan; pendekatan adaptif menjadi solusi paling relevan untuk konteks sistem nyata.