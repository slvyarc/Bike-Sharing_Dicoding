# Library yang digunakan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Load tabel "day"
day_df = pd.read_csv("https://raw.githubusercontent.com/slvyarc/Bike-Sharing_Dicoding/main/Dashboard/cleaned_bikeshare.csv")
day_df.head()

# Menghapus kolom windspeed (tidak sesuai dengan pertanyaan bisnis)
drop_cols = ['windspeed']
day_df.drop(columns=drop_cols, inplace=True, errors='ignore')

# Mengubah nama kolom (opsional)
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'cnt': 'count'
}, inplace=True)

# Mengganti tipe data pada kolom dateday menjadi datetime
day_df['dateday'] = pd.to_datetime(day_df['dateday'])

# Mengubah tipe data kolom weekday, month, year
day_df['weekday'] = day_df['dateday'].dt.day_name()
day_df['month'] = day_df['dateday'].dt.month_name()
day_df['year'] = day_df['dateday'].dt.year


# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    # Resample data berdasarkan bulan dan menghitung total rides
    monthly_rent_df = df.resample(rule='M', on='dateday').agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    # Ubah format indeks menjadi bulan-tahun (Jan-20, Feb-20, dll.)
    monthly_rent_df.index = monthly_rent_df.index.strftime('%b-%y')
    monthly_rent_df = monthly_rent_df.reset_index()
    # Ubah nama kolom
    monthly_rent_df.rename(columns={
        "dateday": "yearmonth",
        "count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return monthly_rent_df


# Menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    # Kelompokkan data berdasarkan hari libur
    holiday_rent_df = df.groupby("holiday").agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    holiday_rent_df = holiday_rent_df.reset_index()
    # Ubah nama kolom
    holiday_rent_df.rename(columns={
        "count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    # Ubah keterangan pada kolom holiday
    holiday_rent_df['holiday'] = holiday_rent_df['holiday'].map({
        0: 'Not a Holiday',
        1: 'Holiday'
    })
    return holiday_rent_df


# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    # Kelompokkan data berdasarkan hari dalam seminggu
    weekday_rent_df = df.groupby("weekday").agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    weekday_rent_df = weekday_rent_df.reset_index()
    # Ubah nama kolom
    weekday_rent_df.rename(columns={
        "count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    # Melt DataFrame untuk mengubah struktur data
    weekday_rent_df = pd.melt(weekday_rent_df,
                              id_vars=['weekday'],
                              value_vars=['casual_rides', 'registered_rides'],
                              var_name='type_of_rides',
                              value_name='count_rides')
    
    # Urutkan data berdasarkan urutan hari dalam seminggu
    weekday_rent_df['weekday'] = pd.Categorical(weekday_rent_df['weekday'],
                                                categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    weekday_rent_df = weekday_rent_df.sort_values('weekday')
    
    return weekday_rent_df


# Menyiapkan workingday_rent_df
def create_workingday_rent_df(df):
    # Kelompokkan data berdasarkan hari kerja
    workingday_rent_df = df.groupby(by='workingday').agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    workingday_rent_df = workingday_rent_df.reset_index()
    # Ubah nama kolom
    workingday_rent_df.rename(columns={
        "count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    return workingday_rent_df


# Menyiapkan seasonly_rent_df
def create_seasonly_rent_df(df):
    # Kelompokkan data berdasarkan musim
    seasonly_rent_df = df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    seasonly_rent_df = seasonly_rent_df.reset_index()
    # Ubah nama kolom
    seasonly_rent_df.rename(columns={
        "count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    # Melt DataFrame untuk mengubah struktur data
    seasonly_rent_df = pd.melt(seasonly_rent_df,
                               id_vars=['season'],
                               value_vars=['casual_rides', 'registered_rides'],
                               var_name='type_of_rides',
                               value_name='count_rides')
    
    # Ubah kolom musim menjadi kategori dengan urutan yang benar
    seasonly_rent_df['season'] = pd.Categorical(seasonly_rent_df['season'],
                                                categories=['Spring', 'Summer', 'Fall', 'Winter'])
    seasonly_rent_df = seasonly_rent_df.sort_values('season')
    
    return seasonly_rent_df


# Menyiapkan filter components (komponen filter)
min_date = day_df["dateday"].min()
max_date = day_df["dateday"].max()

# Menampilkan logo Capital Bikeshare di sidebar
st.sidebar.image("https://jugnoo.io/wp-content/uploads/2022/05/on-demand-bike-sharing-1-1024x506.jpg")

# Menampilkan header "Filter" di sidebar
st.sidebar.header("Filter:")
# Memilih rentang tanggal dengan date_input di sidebar
start_date, end_date = st.sidebar.date_input(
    label="Date",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Menampilkan header "Connect with me" di sidebar
st.sidebar.header("Connect with me:")

# Menampilkan ikon media sosial di sidebar
st.sidebar.markdown("Silvia Dharma")


# Menambahkan tautan LinkedIn di sidebar
col1 = st.sidebar
with col1:
    st.markdown("[![LinkedIn]](https://id.linkedin.com/in/silvia-dharma-1a7265219?trk=public_profile_browsemap)")

# Menambahkan teks penjelasan di sidebar
st.sidebar.markdown("For inquiries and collaborations, feel free to contact me!")

# Menampilkan teks motivasi di sidebar
st.sidebar.markdown("Keep riding and stay healthy!")

# Menambahkan pemisah horizontal di sidebar
st.sidebar.markdown("---")

# Menampilkan tautan dataset
st.sidebar.markdown("[Dataset](https://drive.google.com/file/d/1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ/view)")

# Hubungkan filter dengan main_df
main_df = day_df[
    (day_df["dateday"] >= str(start_date)) &
    (day_df["dateday"] <= str(end_date))
]

# Assign main_df ke helper functions yang telah dibuat sebelumnya
monthly_rent_df = create_monthly_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
seasonly_rent_df = create_seasonly_rent_df(main_df)
# Menampilkan judul "Bike Sharing Dashboard" di halaman utama
st.title("🚲 Bike Sharing Dashboard 🚲")
st.markdown("##")

# Membagi layar menjadi 3 kolom
col1, col2, col3 = st.columns(3)

# Menampilkan total rides di kolom pertama
with col1:
    total_all_rides = main_df['count'].sum()
    st.metric("Total Rides", value=total_all_rides)

# Menampilkan total casual rides di kolom kedua
with col2:
    total_casual_rides = main_df['casual'].sum()
    st.metric("Total Casual Rides", value=total_casual_rides)

# Menampilkan total registered rides di kolom ketiga
with col3:
    total_registered_rides = main_df['registered'].sum()
    st.metric("Total Registered Rides", value=total_registered_rides)

# Menampilkan pemisah horizontal
st.markdown("---")


# ----- CHART 1: Monthly Line Chart -----
fig = px.line(monthly_rent_df,
              x='yearmonth',
              y=['casual_rides', 'registered_rides', 'total_rides'],
              color_discrete_sequence=["#FF69B4", "#00FF00", "#0000FF"],  # Ubah warna menjadi pink, hijau, dan biru
              markers=True,
              title="Monthly Customer Bikeshare Usage")  # Ubah judul
fig.update_layout(xaxis_title='', yaxis_title='Total Rides',
                  xaxis=dict(showgrid=False, showline=True, linecolor='rgb(204, 204, 204)', linewidth=2, mirror=True),
                  yaxis=dict(showgrid=False, zeroline=False, showline=True, linecolor='rgb(204, 204, 204)', linewidth=2, mirror=True),
                  plot_bgcolor='rgba(255, 255, 255, 0)',
                  showlegend=True,
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig, use_container_width=True)

# ----- CHART 2: Daily Bar Chart -----
fig2 = px.bar(weekday_rent_df,
              x='weekday',
              y=['count_rides'],
              color='type_of_rides',
              barmode='group',
              color_discrete_sequence=["cyan", "salmon", "lightgreen"],  # Ubah palet warna
              title='Customer Bikeshare Usage by Weekday').update_traces(marker_line_width=1.5, marker_line_color="black")  # Ubah bentuk dan warna garis pinggir

st.plotly_chart(fig2, use_container_width=True)

# ----- CHART 3: Seasonal Area Chart -----
fig3 = px.area(seasonly_rent_df,
               x='season',
               y='count_rides',
               color='type_of_rides',
               title='Customer Bikeshare Usage by Season',
               labels={'count_rides': 'Total Rides', 'season': 'Season'},
               line_shape='spline')

st.plotly_chart(fig3, use_container_width=True)

# ----- CHART 4: Holiday Bar Chart -----
fig4 = px.bar(data_frame=holiday_rent_df,
              x='holiday',
              y=['total_rides', 'casual_rides', 'registered_rides'],
              barmode='group',
              color_discrete_map={'total_rides': '#FFD700', 'casual_rides': '#FF6347', 'registered_rides': '#20B2AA'},
              title='Customer Bikeshare Usage by Holiday')
fig4.update_layout(xaxis_title='Holiday', yaxis_title='Total Rides')

st.plotly_chart(fig4, use_container_width=True)

# ----- CHART 5: Pie Chart -----
# Create DataFrame for Pie Chart
workingday_rent_df = pd.DataFrame({
    'workingday': ['Yes', 'No'],
    'total_rides': [300, 400]
})

# Create donut pie chart using Plotly Express
fig5 = px.pie(workingday_rent_df, values='total_rides', names='workingday', 
              title='Customer Bikeshare Usage by Working Day',
              hole=0.5,
              color_discrete_sequence=px.colors.sequential.RdBu)

st.plotly_chart(fig5, use_container_width=True)
st.caption('Copyright (c), created by Silvia Dharma')
