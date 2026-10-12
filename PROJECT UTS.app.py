import streamlit as st

# ==========================================
# 1. KONFIGURASI HALAMAN WEB
# ==========================================
st.set_page_config(
    page_title="Smart Budget Planner",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Smart Budget Planner (Tugas UTS)")
st.write("Aplikasi pengelola keuangan mahasiswa menggunakan **Algoritma Rule-Based (50/30/20)** dan **Greedy Priority Queue**.")

# ==========================================
# 2. INPUT DATA DARI USER
# ==========================================
st.header("1. Input Keuangan Bulanan")
pendapatan = st.number_input("Masukkan Pendapatan Bulanan Anda (Rp):", min_value=0, step=50000, value=2000000)

st.header("2. Daftar Tagihan / Kebutuhan Desak")
st.write("Masukkan tagihan yang harus dibayar bulan ini beserta skala prioritasnya.")

# Membuat form input dinamis sederhana untuk 3 tagihan utama
col1, col2 = st.columns([2, 1])
with col1:
    tagihan1_nama = st.text_input("Nama Tagihan 1:", value="Kos / Kontrakan")
    tagihan2_nama = st.text_input("Nama Tagihan 2:", value="Makan & Transport")
    tagihan3_nama = st.text_input("Nama Tagihan 3:", value="Kuota Internet")
with col2:
    tagihan1_biaya = st.number_input("Biaya 1 (Rp):", min_value=0, step=10000, value=800000)
    tagihan2_biaya = st.number_input("Biaya 2 (Rp):", min_value=0, step=10000, value=600000)
    tagihan3_biaya = st.number_input("Biaya 3 (Rp):", min_value=0, step=10000, value=150000)

# Dropdown Prioritas (1 = Paling Penting/Darurat, 3 = Bisa Ditunda)
prio1 = st.selectbox("Prioritas Tagihan 1:", [1, 2, 3], index=0)
prio2 = st.selectbox("Prioritas Tagihan 2:", [1, 2, 3], index=1)
prio3 = st.selectbox("Prioritas Tagihan 3:", [1, 2, 3], index=2)

# Tombol untuk eksekusi algoritma
if st.button("Hitung Alokasi & Rekomendasi", type="primary"):
    
    # ==========================================
    # 3. IMPLEMENTASI ALGORITMA 1: RULE-BASED (50/30/20)
    # ==========================================
    budget_kebutuhan = pendapatan * 0.50
    budget_keinginan = pendapatan * 0.30
    budget_tabungan = pendapatan * 0.20
    
    st.markdown("---")
    st.header("📊 Hasil Alokasi Porsi Dana (Rule 50/30/20)")
    
    col_keb, col_kei, col_tab = st.columns(3)
    col_keb.metric("Kebutuhan (50%)", f"Rp {budget_kebutuhan:,.0f}")
    col_kei.metric("Keinginan (30%)", f"Rp {budget_keinginan:,.0f}")
    col_tab.metric("Tabungan (20%)", f"Rp {budget_tabungan:,.0f}")
    
    # ==========================================
    # 4. IMPLEMENTASI ALGORITMA 2: GREEDY ALGORITHM
    # ==========================================
    st.header("⚡ Urutan Pembayaran Tagihan (Greedy Approach)")
    st.write("Sistem otomatis mengurutkan tagihan dari prioritas tertinggi dan memotong dana Kebutuhan.")

# Menggabungkan data tagihan ke dalam list of dictionaries
    daftar_tagihan = [
        {"nama": tagihan1_nama, "biaya": tagihan1_biaya, "prioritas": prio1},
        {"nama": tagihan2_nama, "biaya": tagihan2_biaya, "prioritas": prio2},
        {"nama": tagihan3_nama, "biaya": tagihan3_biaya, "prioritas": prio3},
    ]
    
    # PROSES SORTING: Mengurutkan berdasarkan prioritas terkecil (angka 1 = urutan pertama)
    # Jika prioritas sama, diurutkan berdasarkan biaya terbesar (Greedy)
    daftar_tagihan.sort(key=lambda x: (x["prioritas"], -x["biaya"]))
    
    sisa_dana_kebutuhan = budget_kebutuhan
    
    # LOOPING GREEDY: Bayar tagihan satu per satu selama dana kebutuhan masih cukup
    for idx, tagihan in enumerate(daftar_tagihan, 1):
        if tagihan["biaya"] <= sisa_dana_kebutuhan:
            status = "✅ LUNAS DIBAYAR"
            sisa_dana_kebutuhan -= tagihan["biaya"]
            warna = "green"
        else:
            status = "❌ DANA TIDAK CUKUP (DITUNDA)"
            warna = "red"
            
        st.markdown(f"**{idx}. {tagihan['nama']}** (Prioritas: {tagihan['prioritas']})")
        st.write(f"- Biaya: Rp {tagihan['biaya']:,.0f}")
        st.markdown(f"- Status: :{warna}[{status}]")
        st.write("---")
        
    st.subheader(f"💰 Sisa Dana Kebutuhan Akhir: Rp {sisa_dana_kebutuhan:,.0f}")
    if sisa_dana_kebutuhan < 0:
        st.error("Peringatan: Dana kebutuhan kamu minus! Sebaiknya kurangi porsi Keinginan (30%) untuk menutupi kekurangan.")
    else:
        st.success("Aman! Dana kebutuhan kamu mencukupi untuk membayar tagihan prioritas bulan ini.")