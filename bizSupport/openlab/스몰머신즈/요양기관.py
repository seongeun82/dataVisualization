import pandas as pd
import re
from modules.DataManipulation import DataManipulation
from modules.Figures import Figures
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express.colors as color_module

mani = DataManipulation()
figures = Figures()


def main():
    label_col_nm = '요양기관그룹'
    df_ykiho = mani.get_ykiho_data_handling(file_path='/bizSupport/openlab/스몰머신즈/data/1_3단질병요양기관그룹별현황(진료년월).xls'
                                            , label_col_nm=label_col_nm)
    df = df_ykiho.copy()
    yyyymm = sorted(df.yyyymm.unique())

    dataList = ['환자수', '내원일수', '청구건수', '진료비']
    label_list = ['상급종합병원', '종합병원', '병원급', '의원급', '보건기관등']
    file_gb = '요양기관그룹별'

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
