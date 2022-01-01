import streamlit as st
import pandas as pd
import plotly.express as px
import datetime as dt

# Dùng tính năng button download: 
# https://docs.streamlit.io/library/api-reference/widgets/st.download_button#stdownload_button
# Nếu muốn tự up file lên hệ thống thì dùng tính năng st.file_uploader
# sau đó cho tất cả câu lệnh vô if st.file_uploader:
st.cache()
st.set_page_config(page_title='Excel app',page_icon='📈')
st.header('Vẽ biểu đồ bằng file excel')

# Tạo hàm download file
def download_csv(df):
    return df.to_csv(index=None,encoding='utf-8')
# Tạo hàm download file html
def download_html(fig):
    return fig.to_html()

# Tự nạp file
df = pd.read_excel(io='Data.xlsx', engine='openpyxl')
df['Month'] = pd.to_datetime(df['Order Date'], format('%d-%m-%Y')).dt.month
st.write(df)

# Chọn group theo drop down-list
st.markdown('------')
group = st.selectbox('Bạn muốn group theo:',
            options=['Ship Mode','Segment','Category', 'Sub-Category'],)
# Hiện data sau khi group
output_columns = ['Sales', 'Profit']
df_group = df.groupby(by=group, as_index=False)[output_columns].sum()
st.write(df_group)
# Tạo nút download dữ liệu
csv = download_csv(df_group)
st.download_button('Tải csv', csv, file_name='grouped_data.csv')

# Vẽ đồ thị
fig = px.bar(
    df_group,
    x=group,
    y='Sales',
    color='Profit',
    color_continuous_scale=['red', 'yellow', 'green'],
    title=f'<b>Sales & Profit by {group}</b>'
)
st.plotly_chart(fig)
html = download_html(fig)
st.download_button('Tải biểu đồ',html, 'chart.html')

# Tạo và vẽ biểu đồ animation
st.markdown('---------------------')
st.header('Phân bổ theo tháng')
df['Month'] = pd.to_datetime(df['Order Date'], format('%d-%m-%Y')).dt.month
# Group theo State
df_region = df.groupby(by=['Region', 'Month'], as_index=False).sum()
st.write(df_region)
fig2 = px.bar(
    df_region,
    x='Region',
    y='Sales',
    color= 'Profit',
    color_continuous_scale=['red', 'yellow', 'green'],
    animation_frame= 'Month',
    range_y =[0,50000],
    title=f'<b>Biến động theo tháng của từng vùng</b>'
    
)
st.plotly_chart(fig2)

fig3 = px.area(
    df_region,
    x='Month',
    y='Sales',
    color='Region',
    range_x=[1,12],
    title=f'<b>Doanh thu theo từng tháng</b>'
)
st.plotly_chart(fig3)