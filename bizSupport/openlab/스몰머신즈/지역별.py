import pandas as pd
import re
from modules.DataManipulation import DataManipulation
from modules.Figures import Figures
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express.colors as color_module

mani = DataManipulation()
figures = Figures()


def fig_output(fig, file_path):
    fig.write_html(full_html=True, file=f'{file_path}.html')
    fig.write_image(format='png', file=f'{file_path}.png')
    return 0


def main():
    df_region = mani.get_region_data_handling()
    df = df_region.copy()
    yyyymm = sorted(df.yyyymm.unique())

    dataList = ['환자수', '내원일수', '청구건수', '진료비']
    label_list = ['서울', '부산', '인천', '대구', '광주', '대전', '울산', '경기', '강원', '충북',
                  '충남', '전북', '전남', '경북', '경남', '제주', '세종']
    label_col_nm = '요양기관소재지구분'
    file_gb = '지역별'

    plotList = []
    markertype = figures.markers24

    for dl in dataList:
        for idx, cd in enumerate(label_list):
            inputdata = df.query(f'{label_col_nm} == "{cd}"').sort_values(by='yyyymm')
            insert_p = go.Scatter(
                mode="lines+markers",
                name=f"{cd}",
                x=yyyymm,
                y=inputdata[dl],
                marker=dict(
                    symbol=markertype[idx],
                    color=color_module.qualitative.Light24[idx],
                    size=7,
                    line=dict(
                        color=color_module.qualitative.Light24[idx],
                        width=5
                    )),
                showlegend=True
            )
            plotList.append(insert_p)

    for fignum in [1, 2, 3, 4]:
        fig = go.Figure()
        label_len = len(label_list)
        for plot in plotList[label_len * (fignum - 1):label_len * fignum]:
            fig.add_trace(plot)

        val_names = ['환자수', '내원일수', '청구건수', '진료비']
        val_name = val_names[fignum - 1]
        yaxis = dict(title=dict(text=val_name, standoff=0.2))
        fig.update_layout(
            dict(
                height=600,
                width=800,
                yaxis=yaxis,
                xaxis=dict(title='년/월')
            )
        )

        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=['2018년 01월', '2018년 03월', '2018년 06월', '2018년 09월', '2018년 12월',
                          '2019년 03월', '2019년 06월', '2019년 09월', '2019년 12월',
                          '2020년 03월', '2020년 06월', '2020년 09월', '2020년 12월'],
                ticktext=['2018년 01월', '3월', '6월', '9월', '12월',
                          '2019년 03월', '6월', '9월', '12월',
                          '2020년 03월', '6월', '9월', '12월']
            ))

        fig.write_html(full_html=True, file=f'{file_gb}_{val_name}.html')
        fig.write_image(format='png', file=f'{file_gb}_{val_name}.png')

    return 0


if __name__ == '__main__':
    main()
