import pandas as pd
import re
from modules.DataManipulation import DataManipulation
from plotly.subplots import make_subplots
import plotly.graph_objects as go

mani = DataManipulation()


def data_load():
    common_path = '/Users/imac/PycharmProjects/dataVisualization'
    df_inout = pd.read_excel(common_path + '/bizSupport/openlab/스몰머신즈/data/1_3단질병성별입원외래별현황(진료년월).xls')
    df_age = pd.read_excel(common_path + '/bizSupport/openlab/스몰머신즈/data/1_3단질병성별연령5세구간별현황(진료년월).xls')
    df_ykiho = pd.read_excel(common_path + '/bizSupport/openlab/스몰머신즈/data/1_3단질병요양기관그룹별현황(진료년월).xls')
    df_region = pd.read_excel(common_path + '/bizSupport/openlab/스몰머신즈/data/1_3단질병요양기관소재지별현황(진료년월) .xls')

    df_inout = mani.hira_excel_treats(df_inout)
    df_age = mani.hira_excel_treats(df_age)
    df_ykiho = mani.hira_excel_treats(df_ykiho)
    df_region = mani.hira_excel_treats(df_region)


def fig_output(fig, file_path):
    fig.write_html(full_html=True, file=f'{file_path}.html')
    fig.write_image(format='png', file=f'{file_path}.png' )
    return 0



def main():
    df_inout, df_in, df_out = mani.get_inout_data_handling()


    default_colors = ['Red', 'Blue', 'Green', 'Yellow']
    yyyymm = sorted(df_inout.yyyymm.unique())

    dataList = ['환자수', '내원일수', '청구건수', '진료비']

    df_data = {'입원':df_in, '외래': df_out}

    for name in ['입원', '외래']:
        fig = make_subplots(rows=2, cols=2, shared_xaxes=True)
        plotList = [go.Scatter(
            mode="lines+markers",
            name=f"{name}",
            x=yyyymm,
            y=df_data.get(name)[dataList[i]],
            marker=dict(
                color=default_colors[i],
                size=7,
                line=dict(
                    color=default_colors[i],
                    width=5
                )),
            showlegend=False
        ) for i in [0, 1, 2, 3]]

        fig.add_trace(plotList[0], row=1, col=1)
        fig.add_trace(plotList[1], row=1, col=2)
        fig.add_trace(plotList[2], row=2, col=1)
        fig.add_trace(plotList[3], row=2, col=2)

        title_name = name + ' 기준 추이'
        fig.update_layout(title=f'<b>{title_name}</b>')

        fig.update_layout(
            dict(
                height=600,
                width=800,
                #         title_text = ''
                yaxis=dict(title=dict(text='환자수', standoff=0.2)),
                yaxis2=dict(title=dict(text='내원일수', standoff=0.2)),
                yaxis3=dict(title=dict(text='청구건수', standoff=0.2)),
                yaxis4=dict(title=dict(text='진료비', standoff=0.2)),
                xaxis3=dict(title='년/월'),
                xaxis4=dict(title='년/월')
            )
        )

        fig.update_layout(
            xaxis3=dict(
                tickmode='array',
                tickvals=['2018년 01월', '2018년 03월', '2018년 06월', '2018년 09월', '2018년 12월',
                          '2019년 03월', '2019년 06월', '2019년 09월', '2019년 12월',
                          '2020년 03월', '2020년 06월', '2020년 09월', '2020년 12월'],
                ticktext=['2018년 01월', '3월', '6월', '9월', '12월',
                          '2019년 03월', '6월', '9월', '12월',
                          '2020년 03월', '6월', '9월', '12월']
            ))

        fig.update_layout(
            xaxis4=dict(
                tickmode='array',
                tickvals=['2018년 01월', '2018년 03월', '2018년 06월', '2018년 09월', '2018년 12월',
                          '2019년 03월', '2019년 06월', '2019년 09월', '2019년 12월',
                          '2020년 03월', '2020년 06월', '2020년 09월', '2020년 12월'],
                ticktext=['2018년 01월', '3월', '6월', '9월', '12월',
                          '2019년 03월', '6월', '9월', '12월',
                          '2020년 03월', '6월', '9월', '12월']
            ))
        file_path = title_name
        fig_output(fig=fig, file_path=file_path)

    return 0






if __name__ == '__main__':
    main()






