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
    df_age = mani.get_age_data_handling()
    df = df_age.copy()
    yyyymm = sorted(df.yyyymm.unique())

    dataList = ['환자수', '내원일수', '청구건수', '진료비']
    label_list = ['5세미만', '5_9세', '10_14세', '15_19세', '20_24세', '25_29세', '30_34세', '35_39세',
                  '40_44세', '45_49세', '50_54세', '55_59세', '60_64세', '65_69세', '70_74세', '75_79세', '80세이상']
    plotList = []
    markertype = figures.markers24

    for dl in dataList:
        for idx, cd in enumerate(label_list):
            inputdata = df.query(f'연령구분5세 == "{cd}"').sort_values(by='yyyymm')
            insert_p = go.Scatter(
                mode="lines+markers",
                name=f"{cd}",
                #             legendgroup = '1',
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

        fig.write_html(full_html=True, file=f'연령별_{val_name}.html')
        fig.write_image(format='png', file=f'연령별_{val_name}.png')

    return 0


if __name__ == '__main__':
    main()
