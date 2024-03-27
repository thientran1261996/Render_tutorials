import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from glob import glob


st.set_page_config(page_title="Du Lieu A0",
                   page_icon=":bar_chart:",
                   layout="wide")


@st.cache
def get_data_excel():
    DiaChi_SL = glob(r".\thong_so\*.xlsx")
    df_tong = pd.DataFrame()
    for path in DiaChi_SL:
        subdf = pd.read_excel(path,engine='openpyxl')
        # subdf["TenFile"] = path.split("\\")[-1][:-5]
        df_tong = pd.concat([subdf, df_tong])

    # df = pd.read_excel(io="Ao_Thong so xuat tuyen 17-09-2023.xlsx",
    #                   engine='openpyxl')
    df_tong.rename(columns={'Trạm NM':'TramNM', 'Cấp Điện Áp':'CapDienAp',
                            'Mô Tả':'MoTa', 'Ngăn':'Ngan','Thông Số':'ThongSo',
                            'Đơn Vị':'DonVi','Ngày':'Ngay',}, inplace=True)
    pd.to_datetime(df_tong["Ngay"], format='%Y-%m-%d')
    return df_tong


def half(a):
    return a/2


df_tong = get_data_excel()
# st.dataframe(df_tong)
# SIDE BAR
st.sidebar.header("Please Filter Here:")

purpose = st.sidebar.multiselect("Choose Purpose:",
                             options=['Loading Condition', 'Loading Calculation'])

if purpose[0] is 'Loading Condition':
    st.subheader('Options:')
    st.text('Opt No.1: Loading Condition of 1 Transmission Line/Substation')
    st.text('Opt No.2: Loading Condition of 2 Transmission Lines/Substations')
    st.text('Opt No.3: Loading Condition of 3 Transmission Lines/Substations')

    num = st.sidebar.multiselect("Choose Option:",
                                 options=['1', '2', '3'])
    if num[0] is '1':
        ngay1 = st.sidebar.multiselect("Choose 1st Date:",
                                      options=df_tong["Ngay"].unique())

        df_11 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram1 = st.sidebar.multiselect("Choose 1st Substation/Power Plant:",
                                      options=df_11["TramNM"].unique())

        df_21 = df_11.query("TramNM == @tram1").reset_index(drop=True)

        ngan1 = st.sidebar.multiselect("Choose 1st Lines/Eqt:",
                                      options=df_21["Ngan"].unique())

        df_31 = df_21.query("Ngan == @ngan1").reset_index(drop=True)

        thongso1 = st.sidebar.multiselect("Choose 1st Parameters(P/Q/I):",
                                         options=df_31["ThongSo"].unique())

        df_selection1 = df_31.query("ThongSo == @thongso1").reset_index(drop=True)

        # MainPage
        st.title(":bar_chart: General Inform Dashboard")
        st.markdown("##")

        # General Information
        df1 = df_selection1.iloc[-1, 7:-1]
        df1 = df1.astype(float)

        df = pd.DataFrame([df1]).reset_index(drop=True)

        aver = round(df1.mean(), 1)
        max_value = round(df1.max(), 1)
        max_hrs = pd.DataFrame(df1)
        max_hrs = list(max_hrs.idxmax(axis=0))[-1]
        min_value = round(df1.min(), 1)
        min_hrs = pd.DataFrame(df1)
        min_hrs = list(min_hrs.idxmin(axis=0))[-1]
        limit_value = df_selection1.iloc[-1,-1]
        units = str(df_selection1['DonVi'].iloc[-1])

        cols = st.columns(4)
        cols[0].header("Average Value:")
        cols[0].write(f'{aver} {units}')
        cols[1].header("Maximum Value:")
        cols[1].write(f'{max_value} {units} at {max_hrs}')
        cols[2].header("Minimum Value:")
        cols[2].write(f'{min_value} {units} at {min_hrs}')
        cols[3].header("Limit Value:")
        cols[3].write(f'{limit_value} {units}')

        # st.dataframe(df1)
        # st.dataframe(df)
        st.dataframe(df_selection1)

        st.markdown("----")
        units = str(df_selection1['DonVi'].iloc[-1])

        fig1 = go.Figure(
            data=[
                go.Scatter(x=df.columns, y=df.iloc[0], name=f"{ngan1} - {tram1}")
            ]
        )
        fig1.update_layout(
            autosize=False,
            width=1200,
            height=800,
            yaxis=dict(
                title_text=f"Value ({units})",
                titlefont=dict(size=30),
            ),
            xaxis=dict(
                title_text="Hour",
                titlefont=dict(size=30),
            )
        )

        st.plotly_chart(fig1, theme="streamlit")
        ##

    if num[0] is '2':
        ngay1 = st.sidebar.multiselect("Choose 1st Date:",
                                       options=df_tong["Ngay"].unique())

        df_11 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram1 = st.sidebar.multiselect("Choose 1st Substation/Power Plant:",
                                       options=df_11["TramNM"].unique())

        df_21 = df_11.query("TramNM == @tram1").reset_index(drop=True)

        ngan1 = st.sidebar.multiselect("Choose 1st Lines/Eqt:",
                                       options=df_21["Ngan"].unique())

        df_31 = df_21.query("Ngan == @ngan1").reset_index(drop=True)

        thongso1 = st.sidebar.multiselect("Choose 1st Parameters(P/Q/I):",
                                          options=df_31["ThongSo"].unique())

        df_selection1 = df_31.query("ThongSo == @thongso1").reset_index(drop=True)

        ngay2 = st.sidebar.multiselect("Choose 2nd Date:",
                                      options=df_tong["Ngay"].unique())

        df_12 = df_tong.query("Ngay == @ngay2").reset_index(drop=True)

        tram2 = st.sidebar.multiselect("Choose 2nd Substation/Power Plant:",
                                      options=df_12["TramNM"].unique())

        df_22 = df_12.query("TramNM == @tram2").reset_index(drop=True)

        ngan2 = st.sidebar.multiselect("Choose 2nd Lines/Eqt:",
                                      options=df_22["Ngan"].unique())

        df_32 = df_22.query("Ngan == @ngan2").reset_index(drop=True)

        thongso2 = st.sidebar.multiselect("Choose 2nd Parameters(P/Q/I):",
                                         options=df_32["ThongSo"].unique())

        df_selection2 = df_32.query("ThongSo == @thongso2").reset_index(drop=True)

        # MainPage
        st.title(":bar_chart: General Inform Dashboard")
        st.markdown("##")

        # General Information
        df1 = df_selection1.iloc[-1, 7:-1]
        df1 = df1.astype(float)

        df2 = df_selection2.iloc[-1, 7:-1]
        df2 = df2.astype(float)

        df12 = pd.DataFrame([df1, df2]).reset_index(drop=True)

        df_sel = pd.DataFrame([df_selection1.iloc[-1], df_selection2.iloc[-1]]).reset_index(drop=True)
        st.dataframe(df_sel)
        st.dataframe(df12)

        for i in range(1, int(num[0])+1):
            aver = round(df12.iloc[i-1].mean(), 1)
            max_value = round(df12.iloc[i-1].max(), 1)
            max_hrs = pd.DataFrame(df12.iloc[i-1])
            max_hrs = list(max_hrs.idxmax(axis=0))[-1]
            min_value = round(df12.iloc[i-1].min(), 1)
            min_hrs = pd.DataFrame(df12.iloc[i-1])
            min_hrs = list(min_hrs.idxmin(axis=0))[-1]
            limit_value = df_sel['Max'].iloc[i-1]
            units = str(df_sel['DonVi'].iloc[i-1])

            cols = st.columns(4)
            cols[0].header("Average Value:")
            cols[0].write(f'{aver} {units}')
            cols[1].header("Maximum Value:")
            cols[1].write(f'{max_value} {units} at {max_hrs}')
            cols[2].header("Minimum Value:")
            cols[2].write(f'{min_value} {units} at {min_hrs}')
            cols[3].header("Limit Value:")
            cols[3].write(f'{limit_value} {units}')

        units = str(df_sel['DonVi'].iloc[-1])
        st.markdown("----")

        fig1 = go.Figure(
            data=[
                go.Scatter(x=df12.columns, y=df12.iloc[0], name=f"{ngan1} - {tram1}"),
                go.Scatter(x=df12.columns, y=df12.iloc[1], name=f"{ngan2} - {tram2}"),
            ]
        )
        fig1.update_layout(
            autosize=False,
            width=1200,
            height=800,
            yaxis=dict(
                title_text=f"Value ({units})",
                titlefont=dict(size=30),
            ),
            xaxis=dict(
                title_text="Hour",
                titlefont=dict(size=30),
            )
        )

        st.plotly_chart(fig1, theme="streamlit")
        ##

    if num[0] is '3':
        ngay1 = st.sidebar.multiselect("Choose 1st Date:",
                                       options=df_tong["Ngay"].unique())

        df_11 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram1 = st.sidebar.multiselect("Choose 1st Substation/Power Plant:",
                                       options=df_11["TramNM"].unique())

        df_21 = df_11.query("TramNM == @tram1").reset_index(drop=True)

        ngan1 = st.sidebar.multiselect("Choose 1st Lines/Eqt:",
                                       options=df_21["Ngan"].unique())

        df_31 = df_21.query("Ngan == @ngan1").reset_index(drop=True)

        thongso1 = st.sidebar.multiselect("Choose 1st Parameters(P/Q/I):",
                                          options=df_31["ThongSo"].unique())

        df_selection1 = df_31.query("ThongSo == @thongso1").reset_index(drop=True)
        # st.dataframe(df_selection1)

        ngay2 = st.sidebar.multiselect("Choose 2nd Date:",
                                       options=df_tong["Ngay"].unique())

        df_12 = df_tong.query("Ngay == @ngay2").reset_index(drop=True)

        tram2 = st.sidebar.multiselect("Choose 2nd Substation/Power Plant:",
                                       options=df_12["TramNM"].unique())

        df_22 = df_12.query("TramNM == @tram2").reset_index(drop=True)

        ngan2 = st.sidebar.multiselect("Choose 2nd Lines/Eqt:",
                                       options=df_22["Ngan"].unique())

        df_32 = df_22.query("Ngan == @ngan2").reset_index(drop=True)

        thongso2 = st.sidebar.multiselect("Choose 2nd Parameters(P/Q/I):",
                                          options=df_32["ThongSo"].unique())

        df_selection2 = df_32.query("ThongSo == @thongso2").reset_index(drop=True)
        # st.dataframe(df_selection2)

        ngay3 = st.sidebar.multiselect("Choose 3rd Date:",
                                       options=df_tong["Ngay"].unique())

        df_13 = df_tong.query("Ngay == @ngay3").reset_index(drop=True)

        tram3 = st.sidebar.multiselect("Choose 3rd Substation/Power Plant:",
                                       options=df_13["TramNM"].unique())

        df_23 = df_13.query("TramNM == @tram3").reset_index(drop=True)

        ngan3 = st.sidebar.multiselect("Choose 3rd Lines/Eqt:",
                                       options=df_23["Ngan"].unique())

        df_33 = df_23.query("Ngan == @ngan3").reset_index(drop=True)

        thongso3 = st.sidebar.multiselect("Choose 3rd Parameters(P/Q/I):",
                                          options=df_33["ThongSo"].unique())

        df_selection3 = df_33.query("ThongSo == @thongso3").reset_index(drop=True)
        # st.dataframe(df_selection3)

        # MainPage
        st.title(":bar_chart: General Inform Dashboard")
        st.markdown("##")

        # General Information
        df1 = df_selection1.iloc[-1, 7:-1]
        df1 = df1.astype(float)

        df2 = df_selection2.iloc[-1, 7:-1]
        df2 = df2.astype(float)

        df3 = df_selection3.iloc[-1, 7:-1]
        df3 = df3.astype(float)

        df123 = pd.DataFrame([df1, df2, df3]).reset_index(drop=True)

        df_sel = pd.DataFrame([df_selection1.iloc[-1],
                               df_selection2.iloc[-1],
                               df_selection3.iloc[-1]]).reset_index(drop=True)
        st.dataframe(df_sel)

        for i in range(1, int(num[0]) + 1):
            aver = round(df123.iloc[i - 1].mean(), 1)
            max_value = round(df123.iloc[i - 1].max(), 1)
            max_hrs = pd.DataFrame(df123.iloc[i - 1])
            max_hrs = list(max_hrs.idxmax(axis=0))[-1]
            min_value = round(df123.iloc[i - 1].min(), 1)
            min_hrs = pd.DataFrame(df123.iloc[i - 1])
            min_hrs = list(min_hrs.idxmin(axis=0))[-1]
            limit_value = df_sel['Max'].iloc[i - 1]
            units = str(df_sel['DonVi'].iloc[i - 1])

            cols = st.columns(4)
            cols[0].header("Average Value:")
            cols[0].write(f'{aver} {units}')
            cols[1].header("Maximum Value:")
            cols[1].write(f'{max_value} {units} at {max_hrs}')
            cols[2].header("Minimum Value:")
            cols[2].write(f'{min_value} {units} at {min_hrs}')
            cols[3].header("Limit Value:")
            cols[3].write(f'{limit_value} {units}')

        units = str(df_sel['DonVi'].iloc[-1])
        st.markdown("----")

        ##
        fig1 = go.Figure(
            data=[
                go.Scatter(x=df123.columns, y=df123.iloc[0], name=f"{ngan1} - {tram1}"),
                go.Scatter(x=df123.columns, y=df123.iloc[1], name=f"{ngan2} - {tram2}"),
                go.Scatter(x=df123.columns, y=df123.iloc[2], name=f"{ngan3} - {tram3}"),
            ]
        )
        fig1.update_layout(
            autosize=False,
            width=1200,
            height=800,
            yaxis=dict(
                title_text=f"Value ({units})",
                titlefont=dict(size=30),
            ),
            xaxis=dict(
                title_text="Hour",
                titlefont=dict(size=30),
            )
        )

        st.plotly_chart(fig1, theme="streamlit")
        ##

############################################
if purpose[0] is 'Loading Calculation':
    st.subheader('Options:')
    st.text('Opt No.1: Shifting 1 Line to Substation with 2 parallel ATs')
    st.text('Opt No.2: Shifting 2 Lines to Substation with 2 parallel ATs')
    st.text('Opt No.3: Shifting 3 Lines to Substation with 2 parallel ATs')
    st.text("Opt No.4: Checking Loading Cond of TxLine to which 1 Line is shifted")
    st.text("Opt No.5: Checking Loading Cond of TxLine to which 2 Lines are shifted")
    st.text("Opt No.6: Checking Loading Cond of TxLine to which 3 Lines are shifted")
    st.text("Opt No.7: Checking Loading Cond of TxLine to which 4 Lines are shifted")

    num = st.sidebar.multiselect("Choose Option:",
                                 options=['1', '2', '3', '4', '5', '6', '7'])

    if num[0] is '1':
        ngay1 = st.sidebar.multiselect("Choose Date:",
                                       options=df_tong["Ngay"].unique())

        df_11 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram1 = st.sidebar.multiselect("Choose 1st Substation/Power Plant:",
                                       options=df_11["TramNM"].unique())

        df_21 = df_11.query("TramNM == @tram1").reset_index(drop=True)

        ngan1 = st.sidebar.multiselect("Choose 1st Line:",
                                       options=df_21["Ngan"].unique())

        df_31 = df_21.query("Ngan == @ngan1").reset_index(drop=True)

        thongso1 = st.sidebar.multiselect("Choose 1st Parameter(P/Q/I):",
                                          options=df_31["ThongSo"].unique())

        df_selection1 = df_31.query("ThongSo == @thongso1").reset_index(drop=True)

        df_12 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram2 = st.sidebar.multiselect("Choose 2nd Substation/Power Plant:",
                                      options=df_12["TramNM"].unique())

        df_22 = df_12.query("TramNM == @tram2").reset_index(drop=True)

        ngan2 = st.sidebar.multiselect("Choose 2nd Line:",
                                      options=df_22["Ngan"].unique())

        df_32 = df_22.query("Ngan == @ngan2").reset_index(drop=True)

        thongso2 = st.sidebar.multiselect("Choose 2nd Parameter(P/Q/I):",
                                         options=df_32["ThongSo"].unique())

        df_selection2 = df_32.query("ThongSo == @thongso2").reset_index(drop=True)

        # MainPage
        st.title(":bar_chart: General Inform Dashboard")
        st.markdown("##")

        # General Information
        df1 = df_selection1.iloc[-1, 7:-1]
        df1 = df1.astype(float)
        df11 = pd.DataFrame(df1).reset_index(drop=True)
        df11 = df11.apply(half, axis=0)
        df11 = pd.DataFrame(df11).astype(float)

        df2 = df_selection2.iloc[-1, 7:-1]
        df2 = df2.astype(float)
        df21 = pd.DataFrame(df2).reset_index(drop=True)
        df = df21.add(df11, fill_value=0)
        df = pd.DataFrame(data=df.values.astype(float), index=df2.index)
        # pd.DataFrame(data=no_col_names_df.values, columns=col_names_df.columns)

        df_sel = pd.DataFrame([df_selection1.iloc[-1], df_selection2.iloc[-1]]).reset_index(drop=True)
        st.dataframe(df_sel)
        # st.dataframe(df1)
        # st.write(df1.dtype)
        # st.dataframe(df11)
        # st.write(df11.dtype)
        # st.dataframe(df2)
        # st.write(df2.dtype)
        # st.dataframe(df)
        # st.write(df.dtypes)

        df12 = pd.DataFrame([df1.T, df2.T]).reset_index(drop=True)
        df12 = pd.concat([df12, df.T], ignore_index=True)
        # st.dataframe(df12)

        for i in range(1, int(num[0])+3):
            aver = round(df12.iloc[i-1].mean(), 1)
            max_value = round(df12.iloc[i-1].max(), 1)
            max_hrs = pd.DataFrame(df12.iloc[i-1])
            max_hrs = list(max_hrs.idxmax(axis=0))[-1]
            min_value = round(df12.iloc[i-1].min(), 1)
            min_hrs = pd.DataFrame(df12.iloc[i-1])
            min_hrs = list(min_hrs.idxmin(axis=0))[-1]
            if i is not int(num[0])+2:
                limit_value = df_sel['Max'].iloc[i-1]
                units = str(df_sel['DonVi'].iloc[i-1])
            else:
                limit_value = df_sel['Max'].iloc[i - 2]
                units = str(df_sel['DonVi'].iloc[i - 2])

            cols = st.columns(4)
            cols[0].header("Average Value:")
            cols[0].write(f'{aver} {units}')
            cols[1].header("Maximum Value:")
            cols[1].write(f'{max_value} {units} at {max_hrs}')
            cols[2].header("Minimum Value:")
            cols[2].write(f'{min_value} {units} at {min_hrs}')
            cols[3].header("Limit Value:")
            cols[3].write(f'{limit_value} {units}')

        units = str(df_sel['DonVi'].iloc[-1])
        st.markdown("----")

        fig1 = go.Figure(
            data=[
                go.Scatter(x=df12.columns, y=df12.iloc[0], name=f"{ngan1} - {tram1}"),
                go.Scatter(x=df12.columns, y=df12.iloc[1], name=f"{ngan2} - {tram2} before"),
                go.Scatter(x=df12.columns, y=df12.iloc[2], name=f"{ngan2} - {tram2} after"),
            ]
        )
        fig1.update_layout(
            autosize=False,
            width=1200,
            height=800,
            yaxis=dict(
                title_text=f"Value ({units})",
                titlefont=dict(size=30),
            ),
            xaxis=dict(
                title_text="Hour",
                titlefont=dict(size=30),
            )
        )

        st.plotly_chart(fig1, theme="streamlit")

    if num[0] is '2':
        ngay1 = st.sidebar.multiselect("Choose Date:",
                                       options=df_tong["Ngay"].unique())

        df_11 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram1 = st.sidebar.multiselect("Choose 1st Substation/Power Plant:",
                                       options=df_11["TramNM"].unique())

        df_21 = df_11.query("TramNM == @tram1").reset_index(drop=True)

        ngan1 = st.sidebar.multiselect("Choose 1st Line:",
                                       options=df_21["Ngan"].unique())

        df_31 = df_21.query("Ngan == @ngan1").reset_index(drop=True)

        thongso1 = st.sidebar.multiselect("Choose 1st Parameter(P/Q/I):",
                                          options=df_31["ThongSo"].unique())

        df_selection1 = df_31.query("ThongSo == @thongso1").reset_index(drop=True)

        df_12 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram2 = st.sidebar.multiselect("Choose 2nd Substation/Power Plant:",
                                       options=df_12["TramNM"].unique())

        df_22 = df_12.query("TramNM == @tram2").reset_index(drop=True)

        ngan2 = st.sidebar.multiselect("Choose 2nd Line:",
                                       options=df_22["Ngan"].unique())

        df_32 = df_22.query("Ngan == @ngan2").reset_index(drop=True)

        thongso2 = st.sidebar.multiselect("Choose 2nd Parameter(P/Q/I):",
                                          options=df_32["ThongSo"].unique())

        df_selection2 = df_32.query("ThongSo == @thongso2").reset_index(drop=True)

        method1 = st.sidebar.multiselect("Choose Method:", options=['Sum', 'Subtract'])

        df_13 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram3 = st.sidebar.multiselect("Choose 3rd Substation/Power Plant:",
                                       options=df_13["TramNM"].unique())

        df_23 = df_13.query("TramNM == @tram3").reset_index(drop=True)

        ngan3 = st.sidebar.multiselect("Choose 3rd Line:",
                                       options=df_23["Ngan"].unique())

        df_33 = df_23.query("Ngan == @ngan3").reset_index(drop=True)

        thongso3 = st.sidebar.multiselect("Choose 3rd Parameter(P/Q/I):",
                                          options=df_33["ThongSo"].unique())

        df_selection3 = df_33.query("ThongSo == @thongso3").reset_index(drop=True)

        # MainPage
        st.title(":bar_chart: General Inform Dashboard")
        st.markdown("##")

        # General Information
        df1 = df_selection1.iloc[-1, 7:-1]
        df1 = df1.astype(float)

        df2 = df_selection2.iloc[-1, 7:-1]
        df2 = df2.astype(float)

        df3 = df_selection3.iloc[-1, 7:-1]
        df3 = df3.astype(float)

        df11 = pd.DataFrame(df1).reset_index(drop=True)
        df21 = pd.DataFrame(df2).reset_index(drop=True)

        if method1[0] is 'Sum':
            df = df11.add(df21, fill_value=0)
        else:
            df = df11.sub(df21, fill_value=0)

        st.dataframe(df)

        df21 = df.apply(half, axis=0)
        df21 = pd.DataFrame(df21).astype(float)

        df31 = pd.DataFrame(df3).reset_index(drop=True).add(df21, fill_value=0)
        df31 = pd.DataFrame(data=df31.values.astype(float), index=df2.index)

        df = pd.DataFrame([df1.T, df2.T, df3.T]).reset_index(drop=True)
        df123 = pd.concat([df, df31.T], ignore_index=True)

        df_sel = pd.DataFrame([df_selection1.iloc[-1],
                               df_selection2.iloc[-1],
                               df_selection3.iloc[-1]]).reset_index(drop=True)

        st.dataframe(df_sel)

        for i in range(1, int(num[0])+3):
            aver = round(df123.iloc[i - 1].mean(), 1)
            max_value = round(df123.iloc[i - 1].max(), 1)
            max_hrs = pd.DataFrame(df123.iloc[i - 1])
            max_hrs = list(max_hrs.idxmax(axis=0))[-1]
            min_value = round(df123.iloc[i - 1].min(), 1)
            min_hrs = pd.DataFrame(df123.iloc[i - 1])
            min_hrs = list(min_hrs.idxmin(axis=0))[-1]
            if i is not int(num[0])+2:
                limit_value = df_sel['Max'].iloc[i - 1]
                units = str(df_sel['DonVi'].iloc[i - 1])
            else:
                limit_value = df_sel['Max'].iloc[i - 2]
                units = str(df_sel['DonVi'].iloc[i - 2])

            cols = st.columns(4)
            cols[0].header("Average Value:")
            cols[0].write(f'{aver} {units}')
            cols[1].header("Maximum Value:")
            cols[1].write(f'{max_value} {units} at {max_hrs}')
            cols[2].header("Minimum Value:")
            cols[2].write(f'{min_value} {units} at {min_hrs}')
            cols[3].header("Limit Value:")
            cols[3].write(f'{limit_value} {units}')

        # for i in range(1, int(num[0]) + 1):
        units = str(df_sel['DonVi'].iloc[-1])
        st.markdown("----")

        fig1 = go.Figure(
            data=[
                go.Scatter(x=df123.columns, y=df123.iloc[0], name=f"{ngan1} - {tram1}"),
                go.Scatter(x=df123.columns, y=df123.iloc[1], name=f"{ngan2} - {tram2}"),
                go.Scatter(x=df123.columns, y=df123.iloc[2], name=f"{ngan3} - {tram3} before"),
                go.Scatter(x=df123.columns, y=df123.iloc[3], name=f"{ngan3} - {tram3} after"),
            ]
        )
        fig1.update_layout(
            autosize=False,
            width=1200,
            height=800,
            yaxis=dict(
                title_text=f"Value ({units})",
                titlefont=dict(size=30),
            ),
            xaxis=dict(
                title_text="Hour",
                titlefont=dict(size=30),
                )
            )

        st.plotly_chart(fig1, theme="streamlit")

    if num[0] is '3':
        ngay1 = st.sidebar.multiselect("Choose Date:",
                                       options=df_tong["Ngay"].unique())

        df_11 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram1 = st.sidebar.multiselect("Choose 1st Substation/Power Plant:",
                                       options=df_11["TramNM"].unique())

        df_21 = df_11.query("TramNM == @tram1").reset_index(drop=True)

        ngan1 = st.sidebar.multiselect("Choose 1st Line:",
                                       options=df_21["Ngan"].unique())

        df_31 = df_21.query("Ngan == @ngan1").reset_index(drop=True)

        thongso1 = st.sidebar.multiselect("Choose 1st Parameter(P/Q/I):",
                                          options=df_31["ThongSo"].unique())

        df_selection1 = df_31.query("ThongSo == @thongso1").reset_index(drop=True)

        df_12 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram2 = st.sidebar.multiselect("Choose 2nd Substation/Power Plant:",
                                       options=df_12["TramNM"].unique())

        df_22 = df_12.query("TramNM == @tram2").reset_index(drop=True)

        ngan2 = st.sidebar.multiselect("Choose 2nd Line:",
                                       options=df_22["Ngan"].unique())

        df_32 = df_22.query("Ngan == @ngan2").reset_index(drop=True)

        thongso2 = st.sidebar.multiselect("Choose 2nd Parameter(P/Q/I):",
                                          options=df_32["ThongSo"].unique())

        df_selection2 = df_32.query("ThongSo == @thongso2").reset_index(drop=True)

        method1 = st.sidebar.multiselect("Choose 1st Method:", options=['Sum', 'Subtract'])

        df_13 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram3 = st.sidebar.multiselect("Choose 3rd Substation/Power Plant:",
                                       options=df_13["TramNM"].unique())

        df_23 = df_13.query("TramNM == @tram3").reset_index(drop=True)

        ngan3 = st.sidebar.multiselect("Choose 3rd Line:",
                                       options=df_23["Ngan"].unique())

        df_33 = df_23.query("Ngan == @ngan3").reset_index(drop=True)

        thongso3 = st.sidebar.multiselect("Choose 3rd Parameter(P/Q/I):",
                                          options=df_33["ThongSo"].unique())

        df_selection3 = df_33.query("ThongSo == @thongso3").reset_index(drop=True)

        method2 = st.sidebar.multiselect("Choose 2nd Method:", options=['Sum', 'Subtract'])

        df_14 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram4 = st.sidebar.multiselect("Choose 4th Substation/Power Plant:",
                                       options=df_14["TramNM"].unique())

        df_24 = df_14.query("TramNM == @tram4").reset_index(drop=True)

        ngan4 = st.sidebar.multiselect("Choose 4th Line:",
                                       options=df_24["Ngan"].unique())

        df_34 = df_24.query("Ngan == @ngan4").reset_index(drop=True)

        thongso4 = st.sidebar.multiselect("Choose 4th Parameter(P/Q/I):",
                                          options=df_34["ThongSo"].unique())

        df_selection4 = df_34.query("ThongSo == @thongso4").reset_index(drop=True)

        # MainPage
        st.title(":bar_chart: General Inform Dashboard")
        st.markdown("##")

        # General Information
        df1 = df_selection1.iloc[-1, 7:-1]
        df1 = df1.astype(float)

        df2 = df_selection2.iloc[-1, 7:-1]
        df2 = df2.astype(float)

        df3 = df_selection3.iloc[-1, 7:-1]
        df3 = df3.astype(float)

        df4 = df_selection4.iloc[-1, 7:-1]
        df4 = df4.astype(float)

        df11 = pd.DataFrame(df1).reset_index(drop=True)
        df21 = pd.DataFrame(df2).reset_index(drop=True)
        df31 = pd.DataFrame(df3).reset_index(drop=True)

        if method1[0] is 'Sum':
            df21 = df11.add(df21, fill_value=0)
        else:
            df21 = df11.sub(df21, fill_value=0)

        if method2[0] is 'Sum':
            df321 = pd.DataFrame(df21).reset_index(drop=True).add(df31, fill_value=0)
        else:
            df321 = pd.DataFrame(df21).reset_index(drop=True).sub(df31, fill_value=0)

        df321 = df321.apply(half, axis=0)
        df321 = pd.DataFrame(df321).astype(float)

        df41 = pd.DataFrame(df4).reset_index(drop=True).add(df321, fill_value=0)
        df41 = pd.DataFrame(data=df41.values.astype(float), index=df2.index)

        df = pd.DataFrame([df1.T, df2.T, df3.T, df4.T]).reset_index(drop=True)
        df = pd.concat([df, df41.T], ignore_index=True)

        df_sel = pd.DataFrame([df_selection1.iloc[-1],
                               df_selection2.iloc[-1],
                               df_selection3.iloc[-1],
                               df_selection4.iloc[-1]]).reset_index(drop=True)
        st.dataframe(df_sel)
        st.dataframe(df)

        for i in range(1, int(num[0])+3):
            aver = round(df.iloc[i - 1].mean(), 1)
            max_value = round(df.iloc[i - 1].max(), 1)
            max_hrs = pd.DataFrame(df.iloc[i - 1])
            max_hrs = list(max_hrs.idxmax(axis=0))[-1]
            min_value = round(df.iloc[i - 1].min(), 1)
            min_hrs = pd.DataFrame(df.iloc[i - 1])
            min_hrs = list(min_hrs.idxmin(axis=0))[-1]
            if i is not int(num[0])+2:
                limit_value = df_sel['Max'].iloc[i - 1]
                units = str(df_sel['DonVi'].iloc[i - 1])
            else:
                limit_value = df_sel['Max'].iloc[i - 2]
                units = str(df_sel['DonVi'].iloc[i - 2])

            cols = st.columns(4)
            cols[0].header("Average Value:")
            cols[0].write(f'{aver} {units}')
            cols[1].header("Maximum Value:")
            cols[1].write(f'{max_value} {units} at {max_hrs}')
            cols[2].header("Minimum Value:")
            cols[2].write(f'{min_value} {units} at {min_hrs}')
            cols[3].header("Limit Value:")
            cols[3].write(f'{limit_value} {units}')

        units = str(df_sel['DonVi'].iloc[-1])
        st.markdown("----")

        fig1 = go.Figure(
            data=[
                go.Scatter(x=df.columns, y=df.iloc[0], name=f"{ngan1} - {tram1}"),
                go.Scatter(x=df.columns, y=df.iloc[1], name=f"{ngan2} - {tram2}"),
                go.Scatter(x=df.columns, y=df.iloc[2], name=f"{ngan3} - {tram3}"),
                go.Scatter(x=df.columns, y=df.iloc[3], name=f"{ngan4} - {tram4} before"),
                go.Scatter(x=df.columns, y=df.iloc[4], name=f"{ngan4} - {tram4} after"),
            ]
        )
        fig1.update_layout(
            autosize=False,
            width=1200,
            height=800,
            yaxis=dict(
                title_text=f"Value ({units})",
                titlefont=dict(size=30),
            ),
            xaxis=dict(
                title_text="Hour",
                titlefont=dict(size=30),
            )
        )

        st.plotly_chart(fig1, theme="streamlit")

        #fig = df.T
        #fig_1 = px.line(fig, orientation='v',
        #                labels={
        #                    "index": "Hour",
        #                    "value": f"Value ({units})",
        #                    # "variable": str(df_sel['Ngay'])
        #                })  # , color='country')
        # color_discrete_sequence=["#0083B8"],
        # template='plotly_white')

    if num[0] is '4':
        ngay1 = st.sidebar.multiselect("Choose Date:",
                                       options=df_tong["Ngay"].unique())

        df_11 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram1 = st.sidebar.multiselect("Choose 1st Substation/Power Plant:",
                                       options=df_11["TramNM"].unique())

        df_21 = df_11.query("TramNM == @tram1").reset_index(drop=True)

        ngan1 = st.sidebar.multiselect("Choose 1st Line:",
                                       options=df_21["Ngan"].unique())

        df_31 = df_21.query("Ngan == @ngan1").reset_index(drop=True)

        thongso1 = st.sidebar.multiselect("Choose 1st Parameter(P/Q/I):",
                                          options=df_31["ThongSo"].unique())

        df_selection1 = df_31.query("ThongSo == @thongso1").reset_index(drop=True)

        df_12 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram2 = st.sidebar.multiselect("Choose 2nd Substation/Power Plant:",
                                      options=df_12["TramNM"].unique())

        df_22 = df_12.query("TramNM == @tram2").reset_index(drop=True)

        ngan2 = st.sidebar.multiselect("Choose 2nd Line:",
                                      options=df_22["Ngan"].unique())

        df_32 = df_22.query("Ngan == @ngan2").reset_index(drop=True)

        thongso2 = st.sidebar.multiselect("Choose 2nd Parameter(P/Q/I):",
                                         options=df_32["ThongSo"].unique())

        df_selection2 = df_32.query("ThongSo == @thongso2").reset_index(drop=True)

        # MainPage
        st.title(":bar_chart: General Inform Dashboard")
        st.markdown("##")

        # General Information
        df1 = df_selection1.iloc[-1,7:-1]
        df1 = df1.astype(float)
        df11 = pd.DataFrame(df1).reset_index(drop=True)
        # df11 = df11.apply(half, axis=0)
        # df11 = pd.DataFrame(df11).astype(float)

        df2 = df_selection2.iloc[-1, 7:-1]
        df2 = df2.astype(float)
        df21 = pd.DataFrame(df2).reset_index(drop=True)

        df = df21.add(df11, fill_value=0)
        df = pd.DataFrame(data=df.values.astype(float), index=df2.index)
        # pd.DataFrame(data=no_col_names_df.values, columns=col_names_df.columns)

        df_sel = pd.DataFrame([df_selection1.iloc[-1], df_selection2.iloc[-1]]).reset_index(drop=True)
        st.dataframe(df_sel)

        df12 = pd.DataFrame([df1.T, df2.T]).reset_index(drop=True)
        df12 = pd.concat([df12, df.T], ignore_index=True)
        st.dataframe(df12)

        for i in range(1, int(num[0])):
            aver = round(df12.iloc[i-1].mean(), 1)
            max_value = round(df12.iloc[i-1].max(), 1)
            max_hrs = pd.DataFrame(df12.iloc[i-1])
            max_hrs = list(max_hrs.idxmax(axis=0))[-1]
            min_value = round(df12.iloc[i-1].min(), 1)
            min_hrs = pd.DataFrame(df12.iloc[i-1])
            min_hrs = list(min_hrs.idxmin(axis=0))[-1]
            if i is not int(num[0])-1:
                limit_value = df_sel['Max'].iloc[i-1]
                units = str(df_sel['DonVi'].iloc[i-1])
            else:
                limit_value = df_sel['Max'].iloc[i - 2]
                units = str(df_sel['DonVi'].iloc[i - 2])

            cols = st.columns(4)
            cols[0].header("Average Value:")
            cols[0].write(f'{aver} {units}')
            cols[1].header("Maximum Value:")
            cols[1].write(f'{max_value} {units} at {max_hrs}')
            cols[2].header("Minimum Value:")
            cols[2].write(f'{min_value} {units} at {min_hrs}')
            cols[3].header("Limit Value:")
            cols[3].write(f'{limit_value} {units}')

        units = str(df_sel['DonVi'].iloc[-1])
        st.markdown("--")

        fig1 = go.Figure(
            data=[
                go.Scatter(x=df12.columns, y=df12.iloc[0], name=f"{ngan1} - {tram1}"),
                go.Scatter(x=df12.columns, y=df12.iloc[1], name=f"{ngan2} - {tram2} before"),
                go.Scatter(x=df12.columns, y=df12.iloc[2], name=f"{ngan2} - {tram2} after"),
            ]
        )
        fig1.update_layout(
            autosize=False,
            width=1200,
            height=800,
            yaxis=dict(
                title_text=f"Value ({units})",
                titlefont=dict(size=30),
            ),
            xaxis=dict(
                title_text="Hour",
                titlefont=dict(size=30),
            )
        )

        st.plotly_chart(fig1, theme="streamlit")

    if num[0] is '5': ### 4 graphs
        ngay1 = st.sidebar.multiselect("Choose Date:",
                                       options=df_tong["Ngay"].unique())

        df_11 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram1 = st.sidebar.multiselect("Choose 1st Substation/Power Plant:",
                                       options=df_11["TramNM"].unique())

        df_21 = df_11.query("TramNM == @tram1").reset_index(drop=True)

        ngan1 = st.sidebar.multiselect("Choose 1st Line:",
                                       options=df_21["Ngan"].unique())

        df_31 = df_21.query("Ngan == @ngan1").reset_index(drop=True)

        thongso1 = st.sidebar.multiselect("Choose 1st Parameter(P/Q/I):",
                                          options=df_31["ThongSo"].unique())

        df_selection1 = df_31.query("ThongSo == @thongso1").reset_index(drop=True)

        df_12 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram2 = st.sidebar.multiselect("Choose 2nd Substation/Power Plant:",
                                       options=df_12["TramNM"].unique())

        df_22 = df_12.query("TramNM == @tram2").reset_index(drop=True)

        ngan2 = st.sidebar.multiselect("Choose 2nd Line:",
                                       options=df_22["Ngan"].unique())

        df_32 = df_22.query("Ngan == @ngan2").reset_index(drop=True)

        thongso2 = st.sidebar.multiselect("Choose 2nd Parameter(P/Q/I):",
                                          options=df_32["ThongSo"].unique())

        df_selection2 = df_32.query("ThongSo == @thongso2").reset_index(drop=True)

        method1 = st.sidebar.multiselect("Choose Method:", options=['Sum', 'Subtract'])

        df_13 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram3 = st.sidebar.multiselect("Choose 3rd Substation/Power Plant:",
                                       options=df_13["TramNM"].unique())

        df_23 = df_13.query("TramNM == @tram3").reset_index(drop=True)

        ngan3 = st.sidebar.multiselect("Choose 3rd Line:",
                                       options=df_23["Ngan"].unique())

        df_33 = df_23.query("Ngan == @ngan3").reset_index(drop=True)

        thongso3 = st.sidebar.multiselect("Choose 3rd Parameter(P/Q/I):",
                                          options=df_33["ThongSo"].unique())

        df_selection3 = df_33.query("ThongSo == @thongso3").reset_index(drop=True)

        # MainPage
        st.title(":bar_chart: General Inform Dashboard")
        st.markdown("##")

        # General Information
        df1 = df_selection1.iloc[-1, 7:-1]
        df1 = df1.astype(float)

        df2 = df_selection2.iloc[-1, 7:-1]
        df2 = df2.astype(float)

        df3 = df_selection3.iloc[-1, 7:-1]
        df3 = df3.astype(float)

        df21 = pd.DataFrame(df2).reset_index(drop=True)
        if method1[0] is 'Sum':
            df21 = pd.DataFrame(df1).reset_index(drop=True).add(df21, fill_value=0)
        else:
            df21 = pd.DataFrame(df1).reset_index(drop=True).sub(df21, fill_value=0)

        df31 = pd.DataFrame(df3).reset_index(drop=True)
        df31 = pd.DataFrame(df21).astype(float).reset_index(drop=True).add(df31, fill_value=0)
        df31 = pd.DataFrame(data=df31.values.astype(float), index=df2.index)

        df = pd.DataFrame([df1.T, df2.T, df3.T]).reset_index(drop=True)
        df123 = pd.concat([df, df31.T], ignore_index=True)

        df_sel = pd.DataFrame([df_selection1.iloc[-1],
                               df_selection2.iloc[-1],
                               df_selection3.iloc[-1]]).reset_index(drop=True)
        st.dataframe(df_sel)

        for i in range(1, int(num[0])):
            aver = round(df123.iloc[i - 1].mean(), 1)
            max_value = round(df123.iloc[i - 1].max(), 1)
            max_hrs = pd.DataFrame(df123.iloc[i - 1])
            max_hrs = list(max_hrs.idxmax(axis=0))[-1]
            min_value = round(df123.iloc[i - 1].min(), 1)
            min_hrs = pd.DataFrame(df123.iloc[i - 1])
            min_hrs = list(min_hrs.idxmin(axis=0))[-1]
            if i is not int(num[0])-1:
                limit_value = df_sel['Max'].iloc[i - 1]
                units = str(df_sel['DonVi'].iloc[i - 1])
            else:
                limit_value = df_sel['Max'].iloc[i - 2]
                units = str(df_sel['DonVi'].iloc[i - 2])

            cols = st.columns(4)
            cols[0].header("Average Value:")
            cols[0].write(f'{aver} {units}')
            cols[1].header("Maximum Value:")
            cols[1].write(f'{max_value} {units} at {max_hrs}')
            cols[2].header("Minimum Value:")
            cols[2].write(f'{min_value} {units} at {min_hrs}')
            cols[3].header("Limit Value:")
            cols[3].write(f'{limit_value} {units}')

        units = str(df_sel['DonVi'].iloc[-1])
        st.markdown("----")

        fig1 = go.Figure(
            data=[
                go.Scatter(x=df123.columns, y=df123.iloc[0], name=f"{ngan1} - {tram1}"),
                go.Scatter(x=df123.columns, y=df123.iloc[1], name=f"{ngan2} - {tram2}"),
                go.Scatter(x=df123.columns, y=df123.iloc[2], name=f"{ngan3} - {tram3} before"),
                go.Scatter(x=df123.columns, y=df123.iloc[3], name=f"{ngan3} - {tram3} after"),
            ]
        )
        fig1.update_layout(
            autosize=False,
            width=1200,
            height=800,
            yaxis=dict(
                title_text=f"Value ({units})",
                titlefont=dict(size=30),
            ),
            xaxis=dict(
                title_text="Hour",
                titlefont=dict(size=30),
            )
        )

        st.plotly_chart(fig1, theme="streamlit")

    if num[0] is '6': ### 5 graphs
        ngay1 = st.sidebar.multiselect("Choose Date:",
                                       options=df_tong["Ngay"].unique())

        df_11 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram1 = st.sidebar.multiselect("Choose 1st Substation/Power Plant:",
                                       options=df_11["TramNM"].unique())

        df_21 = df_11.query("TramNM == @tram1").reset_index(drop=True)

        ngan1 = st.sidebar.multiselect("Choose 1st Line:",
                                       options=df_21["Ngan"].unique())

        df_31 = df_21.query("Ngan == @ngan1").reset_index(drop=True)

        thongso1 = st.sidebar.multiselect("Choose 1st Parameter(P/Q/I):",
                                          options=df_31["ThongSo"].unique())

        df_selection1 = df_31.query("ThongSo == @thongso1").reset_index(drop=True)

        df_12 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram2 = st.sidebar.multiselect("Choose 2nd Substation/Power Plant:",
                                       options=df_12["TramNM"].unique())

        df_22 = df_12.query("TramNM == @tram2").reset_index(drop=True)

        ngan2 = st.sidebar.multiselect("Choose 2nd Line:",
                                       options=df_22["Ngan"].unique())

        df_32 = df_22.query("Ngan == @ngan2").reset_index(drop=True)

        thongso2 = st.sidebar.multiselect("Choose 2nd Parameter(P/Q/I):",
                                          options=df_32["ThongSo"].unique())

        df_selection2 = df_32.query("ThongSo == @thongso2").reset_index(drop=True)

        method1 = st.sidebar.multiselect("Choose 1st Method:", options=['Sum', 'Subtract'])

        df_13 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram3 = st.sidebar.multiselect("Choose 3rd Substation/Power Plant:",
                                       options=df_13["TramNM"].unique())

        df_23 = df_13.query("TramNM == @tram3").reset_index(drop=True)

        ngan3 = st.sidebar.multiselect("Choose 3rd Line:",
                                       options=df_23["Ngan"].unique())

        df_33 = df_23.query("Ngan == @ngan3").reset_index(drop=True)

        thongso3 = st.sidebar.multiselect("Choose 3rd Parameter(P/Q/I):",
                                          options=df_33["ThongSo"].unique())

        df_selection3 = df_33.query("ThongSo == @thongso3").reset_index(drop=True)

        method2 = st.sidebar.multiselect("Choose 2nd Method:", options=['Sum', 'Subtract'])

        df_14 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram4 = st.sidebar.multiselect("Choose 4th Substation/Power Plant:",
                                       options=df_14["TramNM"].unique())

        df_24 = df_14.query("TramNM == @tram4").reset_index(drop=True)

        ngan4 = st.sidebar.multiselect("Choose 4th Line:",
                                       options=df_24["Ngan"].unique())

        df_34 = df_24.query("Ngan == @ngan4").reset_index(drop=True)

        thongso4 = st.sidebar.multiselect("Choose 4th Parameter(P/Q/I):",
                                          options=df_34["ThongSo"].unique())

        df_selection4 = df_34.query("ThongSo == @thongso4").reset_index(drop=True)

        # MainPage
        st.title(":bar_chart: General Inform Dashboard")
        st.markdown("##")

        # General Information
        df1 = df_selection1.iloc[-1, 7:-1]
        df1 = df1.astype(float)

        df2 = df_selection2.iloc[-1, 7:-1]
        df2 = df2.astype(float)

        df3 = df_selection3.iloc[-1, 7:-1]
        df3 = df3.astype(float)

        df4 = df_selection4.iloc[-1, 7:-1]
        df4 = df4.astype(float)

        df21 = pd.DataFrame(df2).reset_index(drop=True)
        df31 = pd.DataFrame(df3).reset_index(drop=True)

        if method1[0] is 'Sum':
            df21 = pd.DataFrame(df1).reset_index(drop=True).add(df21, fill_value=0)
        else:
            df21 = pd.DataFrame(df1).reset_index(drop=True).sub(df21, fill_value=0)

        if method2[0] is 'Sum':
            df31 = pd.DataFrame(df21).astype(float).reset_index(drop=True).add(df31, fill_value=0)
        else:
            df31 = pd.DataFrame(df21).astype(float).reset_index(drop=True).sub(df31, fill_value=0)

        df41 = pd.DataFrame(df4).astype(float).reset_index(drop=True).add(df31, fill_value=0)
        df41 = pd.DataFrame(data=df41.values.astype(float), index=df2.index)

        df = pd.DataFrame([df1.T, df2.T, df3.T, df4.T]).reset_index(drop=True)
        df123 = pd.concat([df, df41.T], ignore_index=True)

        df_sel = pd.DataFrame([df_selection1.iloc[-1],
                               df_selection2.iloc[-1],
                               df_selection3.iloc[-1],
                               df_selection4.iloc[-1]]).reset_index(drop=True)
        st.dataframe(df_sel)

        for i in range(1, int(num[0])):
            aver = round(df123.iloc[i - 1].mean(), 1)
            max_value = round(df123.iloc[i - 1].max(), 1)
            max_hrs = pd.DataFrame(df123.iloc[i - 1])
            max_hrs = list(max_hrs.idxmax(axis=0))[-1]
            min_value = round(df123.iloc[i - 1].min(), 1)
            min_hrs = pd.DataFrame(df123.iloc[i - 1])
            min_hrs = list(min_hrs.idxmin(axis=0))[-1]
            if i is not int(num[0])-1:
                limit_value = df_sel['Max'].iloc[i - 1]
                units = str(df_sel['DonVi'].iloc[i - 1])
            else:
                limit_value = df_sel['Max'].iloc[i - 2]
                units = str(df_sel['DonVi'].iloc[i - 2])

            cols = st.columns(4)
            cols[0].header("Average Value:")
            cols[0].write(f'{aver} {units}')
            cols[1].header("Maximum Value:")
            cols[1].write(f'{max_value} {units} at {max_hrs}')
            cols[2].header("Minimum Value:")
            cols[2].write(f'{min_value} {units} at {min_hrs}')
            cols[3].header("Limit Value:")
            cols[3].write(f'{limit_value} {units}')

        units = str(df_sel['DonVi'].iloc[-1])
        st.markdown("----")

        fig1 = go.Figure(
            data=[
                go.Scatter(x=df123.columns, y=df123.iloc[0], name=f"{ngan1} - {tram1}"),
                go.Scatter(x=df123.columns, y=df123.iloc[1], name=f"{ngan2} - {tram2}"),
                go.Scatter(x=df123.columns, y=df123.iloc[2], name=f"{ngan3} - {tram3}"),
                go.Scatter(x=df123.columns, y=df123.iloc[3], name=f"{ngan4} - {tram4} before"),
                go.Scatter(x=df123.columns, y=df123.iloc[4], name=f"{ngan4} - {tram4} after")
            ]
        )
        fig1.update_layout(
            autosize=False,
            width=1200,
            height=800,
            yaxis=dict(
                title_text=f"Value ({units})",
                titlefont=dict(size=30),
            ),
            xaxis=dict(
                title_text="Hour",
                titlefont=dict(size=30),
            )
        )

        st.plotly_chart(fig1, theme="streamlit")

    if num[0] is '7': ### 6 graphs
        ngay1 = st.sidebar.multiselect("Choose Date:",
                                       options=df_tong["Ngay"].unique())

        df_11 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram1 = st.sidebar.multiselect("Choose 1st Substation/Power Plant:",
                                       options=df_11["TramNM"].unique())

        df_21 = df_11.query("TramNM == @tram1").reset_index(drop=True)

        ngan1 = st.sidebar.multiselect("Choose 1st Line:",
                                       options=df_21["Ngan"].unique())

        df_31 = df_21.query("Ngan == @ngan1").reset_index(drop=True)

        thongso1 = st.sidebar.multiselect("Choose 1st Parameter(P/Q/I):",
                                          options=df_31["ThongSo"].unique())

        df_selection1 = df_31.query("ThongSo == @thongso1").reset_index(drop=True)

        df_12 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram2 = st.sidebar.multiselect("Choose 2nd Substation/Power Plant:",
                                       options=df_12["TramNM"].unique())

        df_22 = df_12.query("TramNM == @tram2").reset_index(drop=True)

        ngan2 = st.sidebar.multiselect("Choose 2nd Line:",
                                       options=df_22["Ngan"].unique())

        df_32 = df_22.query("Ngan == @ngan2").reset_index(drop=True)

        thongso2 = st.sidebar.multiselect("Choose 2nd Parameter(P/Q/I):",
                                          options=df_32["ThongSo"].unique())

        df_selection2 = df_32.query("ThongSo == @thongso2").reset_index(drop=True)

        method1 = st.sidebar.multiselect("Choose 1st Method:", options=['Sum', 'Subtract'])

        df_13 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram3 = st.sidebar.multiselect("Choose 3rd Substation/Power Plant:",
                                       options=df_13["TramNM"].unique())

        df_23 = df_13.query("TramNM == @tram3").reset_index(drop=True)

        ngan3 = st.sidebar.multiselect("Choose 3rd Line:",
                                       options=df_23["Ngan"].unique())

        df_33 = df_23.query("Ngan == @ngan3").reset_index(drop=True)

        thongso3 = st.sidebar.multiselect("Choose 3rd Parameter(P/Q/I):",
                                          options=df_33["ThongSo"].unique())

        df_selection3 = df_33.query("ThongSo == @thongso3").reset_index(drop=True)

        method2 = st.sidebar.multiselect("Choose 2nd Method:", options=['Sum', 'Subtract'])

        df_14 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram4 = st.sidebar.multiselect("Choose 4th Substation/Power Plant:",
                                       options=df_14["TramNM"].unique())

        df_24 = df_14.query("TramNM == @tram4").reset_index(drop=True)

        ngan4 = st.sidebar.multiselect("Choose 4th Line:",
                                       options=df_24["Ngan"].unique())

        df_34 = df_24.query("Ngan == @ngan4").reset_index(drop=True)

        thongso4 = st.sidebar.multiselect("Choose 4th Parameter(P/Q/I):",
                                          options=df_34["ThongSo"].unique())

        df_selection4 = df_34.query("ThongSo == @thongso4").reset_index(drop=True)

        method3 = st.sidebar.multiselect("Choose 3rd Method:", options=['Sum', 'Subtract'])

        df_15 = df_tong.query("Ngay == @ngay1").reset_index(drop=True)

        tram5 = st.sidebar.multiselect("Choose 5th Substation/Power Plant:",
                                       options=df_15["TramNM"].unique())

        df_25 = df_15.query("TramNM == @tram5").reset_index(drop=True)

        ngan5 = st.sidebar.multiselect("Choose 5th Line:",
                                       options=df_25["Ngan"].unique())

        df_35 = df_25.query("Ngan == @ngan5").reset_index(drop=True)

        thongso5 = st.sidebar.multiselect("Choose 5th Parameter(P/Q/I):",
                                          options=df_35["ThongSo"].unique())

        df_selection5 = df_35.query("ThongSo == @thongso5").reset_index(drop=True)

        # MainPage
        st.title(":bar_chart: General Inform Dashboard")
        st.markdown("##")

        # General Information
        df1 = df_selection1.iloc[-1, 7:-1]
        df1 = df1.astype(float)

        df2 = df_selection2.iloc[-1, 7:-1]
        df2 = df2.astype(float)

        df3 = df_selection3.iloc[-1, 7:-1]
        df3 = df3.astype(float)

        df4 = df_selection4.iloc[-1, 7:-1]
        df4 = df4.astype(float)

        df5 = df_selection5.iloc[-1, 7:-1]
        df5 = df5.astype(float)

        df21 = pd.DataFrame(df2).reset_index(drop=True)
        df31 = pd.DataFrame(df3).reset_index(drop=True)
        df41 = pd.DataFrame(df4).reset_index(drop=True)

        if method1[0] is 'Sum':
            df21 = pd.DataFrame(df1).reset_index(drop=True).add(df21, fill_value=0)
        else:
            df21 = pd.DataFrame(df1).reset_index(drop=True).sub(df21, fill_value=0)

        if method2[0] is 'Sum':
            df31 = pd.DataFrame(df21).astype(float).reset_index(drop=True).add(df31, fill_value=0)
        else:
            df31 = pd.DataFrame(df21).astype(float).reset_index(drop=True).sub(df31, fill_value=0)

        if method3[0] is 'Sum':
            df41 = pd.DataFrame(df31).astype(float).reset_index(drop=True).add(df41, fill_value=0)
        else:
            df41 = pd.DataFrame(df31).astype(float).reset_index(drop=True).sub(df41, fill_value=0)

        df51 = pd.DataFrame(df5).astype(float).reset_index(drop=True).add(df41, fill_value=0)
        df51 = pd.DataFrame(data=df51.values.astype(float), index=df2.index)

        df = pd.DataFrame([df1.T, df2.T, df3.T, df4.T, df5.T]).reset_index(drop=True)
        df123 = pd.concat([df, df51.T], ignore_index=True)

        df_sel = pd.DataFrame([df_selection1.iloc[-1],
                               df_selection2.iloc[-1],
                               df_selection3.iloc[-1],
                               df_selection4.iloc[-1],
                               df_selection5.iloc[-1]]).reset_index(drop=True)
        st.dataframe(df_sel)

        for i in range(1, int(num[0])):
            aver = round(df123.iloc[i - 1].mean(), 1)
            max_value = round(df123.iloc[i - 1].max(), 1)
            max_hrs = pd.DataFrame(df123.iloc[i - 1])
            max_hrs = list(max_hrs.idxmax(axis=0))[-1]
            min_value = round(df123.iloc[i - 1].min(), 1)
            min_hrs = pd.DataFrame(df123.iloc[i - 1])
            min_hrs = list(min_hrs.idxmin(axis=0))[-1]
            if i is not int(num[0])-1:
                limit_value = df_sel['Max'].iloc[i - 1]
                units = str(df_sel['DonVi'].iloc[i - 1])
            else:
                limit_value = df_sel['Max'].iloc[i - 2]
                units = str(df_sel['DonVi'].iloc[i - 2])

            cols = st.columns(4)
            cols[0].header("Average Value:")
            cols[0].write(f'{aver} {units}')
            cols[1].header("Maximum Value:")
            cols[1].write(f'{max_value} {units} at {max_hrs}')
            cols[2].header("Minimum Value:")
            cols[2].write(f'{min_value} {units} at {min_hrs}')
            cols[3].header("Limit Value:")
            cols[3].write(f'{limit_value} {units}')

        units = str(df_sel['DonVi'].iloc[-1])
        st.markdown("----")

        fig1 = go.Figure(
            data=[
                go.Scatter(x=df123.columns, y=df123.iloc[0], name=f"{ngan1} - {tram1}"),
                go.Scatter(x=df123.columns, y=df123.iloc[1], name=f"{ngan2} - {tram2}"),
                go.Scatter(x=df123.columns, y=df123.iloc[2], name=f"{ngan3} - {tram3}"),
                go.Scatter(x=df123.columns, y=df123.iloc[3], name=f"{ngan4} - {tram4}"),
                go.Scatter(x=df123.columns, y=df123.iloc[4], name=f"{ngan5} - {tram5} before"),
                go.Scatter(x=df123.columns, y=df123.iloc[5], name=f"{ngan5} - {tram5} after")
            ]
        )
        fig1.update_layout(
            autosize=False,
            width=1200,
            height=800,
            yaxis=dict(
                title_text=f"Value ({units})",
                titlefont=dict(size=30),
            ),
            xaxis=dict(
                title_text="Hour",
                titlefont=dict(size=30),
            )
        )

        st.plotly_chart(fig1, theme="streamlit")