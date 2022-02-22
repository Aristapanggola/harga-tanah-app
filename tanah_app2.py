import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import xlrd

dtt = pd.read_excel('data_transform.xlsx', index_col=0) #read data Ridge

#Variabel Independen
X = dtt.drop(["harga_total"], axis=1)

#Variabel Dependen
y=dtt["harga_total"]
#Split Data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.25, random_state = 123)

#ridge Model
from sklearn.linear_model import Ridge
reg_rid = Ridge()
reg_rid.fit(X_train, y_train)

##Data Eksplorasi
visualisasi = pd.read_excel('harga_tanah.xlsx', index_col=0)

###
pilihan = st.sidebar.radio("",("Latar Belakang & Dataset","Gambaran Umum Data","Prediksi Harga Tanah"))

def get_pilihan(pilihan):
    global output 
    if pilihan == "Latar Belakang & Dataset":
        st.title("Latar Belakang & Dataset")
        st.write('Tanah menjadi salah satu sumber daya yang berperan penting dalam memenuhi kebutuhan pembangunan tempat tinggal suatu wilayah dengan tingkat kepadatan dan laju pertumbuhan penduduk yang cukup tinggi. Namun, kenyataannya dalam proses pembangunan sering terhambat diakibatkan harga tanah dipasaran terus melonjak khususnya di wilayah DKI Jakarta. Sehingga dengan kondisi harga tanah tersebut menjadi cukup sulit dijangkau oleh masyarakat kelas ekonomi menengah kebawah. Oleh karena itu, Website ini hadir untuk membantu para pengguna khususnya masyarakat kelas ekonomi menengah kebawah untuk mencari tanah yang sesuai dengan kebutuhannya berdasarkan Harga Tanah Per meter Persegi, Cicilan per Bulan, Luas Tanah per Meter Persegi, dan Kabupaten Kota di DKI Jakarta.')
        st.subheader('Dataset diambil dari website Rumah.com per tanggal 17 Maret 2020')
        output = st.dataframe(visualisasi)
    elif pilihan == "Gambaran Umum Data":
        st.title("Gambaran Umum Data Penjualan Tanah di DKI Jakarta")
        kabupaten = visualisasi.kab_kota.value_counts().rename_axis('Kabupaten').reset_index(name='Jumlah')
        output=st.plotly_chart(px.pie(kabupaten, values='Jumlah', names='Kabupaten', title='Persentase Penjualan Tanah Berdasarkan Kabupaten/Kota'))
        sertifikat=visualisasi.sertifikat.value_counts().rename_axis('Sertifikat').reset_index(name='Jumlah')
        output=st.plotly_chart(px.bar(sertifikat, x='Jumlah', y='Sertifikat', text='Jumlah',color='Sertifikat',
        title='Jumlah Penjualan Tanah Berdasarkan Sertifikat Tanah').update_layout(showlegend=False).update_xaxes(categoryorder='total descending'))
        harga_to = visualisasi.groupby('kab_kota')['harga_total'].mean().rename_axis('Kabupaten').reset_index(name= 'Harga(Rp)')
        output = st.plotly_chart(px.bar(harga_to, y='Harga(Rp)',x="Kabupaten",color='Kabupaten',text=round(harga_to['Harga(Rp)'],0),
        title="Rata-rata Harga Penjualan Tanah Berdasarkan Kabupaten/Kota").update_layout(showlegend=False).update_xaxes(categoryorder='total descending'))
        harga_pm = visualisasi.groupby('kab_kota')['harga_perm'].mean().rename_axis('Kabupaten').reset_index(name= 'Harga_per_Meter_Persegi(Rp)')
        output=st.plotly_chart(px.bar(harga_pm,x="Kabupaten", y='Harga_per_Meter_Persegi(Rp)',color='Kabupaten',text=round(harga_pm['Harga_per_Meter_Persegi(Rp)'],1),
        title="Rata-rata Harga Tanah per Meter Persegi Berdasarkan Kabupaten/Kota").update_layout(showlegend=False).update_xaxes(categoryorder='total descending'))
        cicil = visualisasi.groupby('kab_kota')['cicilan'].mean().rename_axis('Kabupaten').reset_index(name= 'Cicilan_per_Bulan(Rp)')
        output=st.plotly_chart(px.bar(cicil,x="Kabupaten", y='Cicilan_per_Bulan(Rp)',color='Kabupaten',text=round(cicil['Cicilan_per_Bulan(Rp)'],2),
        title="Rata-rata Cicilan Tanah Berdasarkan Kabupaten/Kota").update_layout(showlegend=False).update_xaxes(categoryorder='total descending'))
        luas_t = visualisasi.groupby('kab_kota')['luas'].mean().rename_axis('Kabupaten').reset_index(name= 'Luas_per_Meter_Persegi')
        output=st.plotly_chart(px.bar(luas_t,x="Kabupaten", y='Luas_per_Meter_Persegi',color='Kabupaten',text=round(luas_t.Luas_per_Meter_Persegi,1),
        title="Rata-rata Luas Tanah Berdasarkan Kabupaten/Kota").update_layout(showlegend=False).update_xaxes(categoryorder='total descending'))
        jakbar =visualisasi[visualisasi['kab_kota']=='Jakarta Barat']
        ser_jakbar = jakbar['sertifikat'].value_counts().rename_axis('Sertifikat').reset_index(name= 'Jumlah')
        output=st.plotly_chart(px.bar(ser_jakbar, y="Sertifikat", x='Jumlah',text='Jumlah',color='Sertifikat',
        title="Penjualan Tanah Berdasarkan Sertifikat di Jakarta Barat").update_layout(showlegend=False,barmode='stack').update_xaxes(categoryorder='total descending'))
        jakpus =visualisasi[visualisasi['kab_kota']=='Jakarta Pusat']
        ser_jakpus = jakpus['sertifikat'].value_counts().rename_axis('Sertifikat').reset_index(name= 'Jumlah')
        output=st.plotly_chart(px.bar(ser_jakpus, y="Sertifikat", x='Jumlah',text='Jumlah',color='Sertifikat',
        title="Penjualan Tanah Berdasarkan Sertifikat di Jakarta Pusat").update_layout(showlegend=False,barmode='stack').update_xaxes(categoryorder='total descending'))
        jaksel =visualisasi[visualisasi['kab_kota']=='Jakarta Selatan']
        ser_jaksel = jaksel['sertifikat'].value_counts().rename_axis('Sertifikat').reset_index(name= 'Jumlah')
        output =st.plotly_chart(px.bar(ser_jaksel, y="Sertifikat", x='Jumlah',text='Jumlah',color='Sertifikat',
        title="Penjualan Tanah Berdasarkan Sertifikat di Jakarta Selatan").update_layout(showlegend=False,barmode='stack').update_xaxes(categoryorder='total descending'))
        jaktim =visualisasi[visualisasi['kab_kota']=='Jakarta Timur']
        ser_jaktim = jaktim['sertifikat'].value_counts().rename_axis('Sertifikat').reset_index(name= 'Jumlah')
        output =st.plotly_chart(px.bar(ser_jaktim, y="Sertifikat", x='Jumlah',text='Jumlah',color='Sertifikat',
        title="Penjualan Tanah Berdasarkan Sertifikat di Jakarta Timur").update_layout(showlegend=False).update_xaxes(categoryorder='total descending'))
        jakut =visualisasi[visualisasi['kab_kota']=='Jakarta Utara']
        ser_jakut = jakut['sertifikat'].value_counts().rename_axis('Sertifikat').reset_index(name= 'Jumlah')
        output=st.plotly_chart(px.bar(ser_jakut, y="Sertifikat", x='Jumlah',text='Jumlah',color='Sertifikat',
        title="Penjualan Tanah Berdasarkan Sertifikat di Jakarta Utara").update_layout(showlegend=False).update_xaxes(categoryorder='total descending'))
    else:
        st.title("Prediksi Harga Tanah di DKI Jakarta")
        st.subheader("Silahkan Tentunkan Harga Tanah Anda!")
        st.write('Harga Per Meter Persegi')
        harga_perm = st.slider('',min_value=100000, max_value=19000000)
        st.write('Cicilan per Bulan (Jangka Waktu: 25 Tahun)')
        cicilan = st.slider('',min_value=50000, max_value=8000000)
        st.write('Luas Meter Persegi')
        luas = st.slider('',min_value=50, max_value=300)
        st.write('Kabupaten/Kota')
        kab_kota = st.selectbox("",options=['Jakarta Pusat', 'Jakarta Selatan','Jakarta Timur','Jakarta Utara'])
        kab_kota_Jakpus , kab_kota_Jaksel , kab_kota_Jaktim,kab_kota_Jakut = 0,0,0,0
        if kab_kota == 'Jakarta Pusat':
            kab_kota_Jakpus  = 1
        elif kab_kota == 'Jakarta Selatan':
            kab_kota_Jaksel = 1
        elif kab_kota == 'Jakarta Timur':
            kab_kota_Jaktim = 1
        else:
            kab_kota_Jakut = 1

        input_data = [[harga_perm,cicilan,luas,kab_kota_Jakpus,kab_kota_Jaksel,kab_kota_Jaktim,kab_kota_Jakut]]
        output=reg_rid.predict(input_data)
        if st.button("Predict"):
            st.write('Harga Tanah Anda Adalah Sebesar: Rp{:,.0f}'.format(np.exp(*output)))
    return output
output =get_pilihan(pilihan)