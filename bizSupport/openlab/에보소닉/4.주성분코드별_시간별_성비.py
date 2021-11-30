import plotly.graph_objects as go
from plotly.subplots import make_subplots
from Evosonic import Evo
import pandas as pd
evo = Evo()

# 5개의 각기 다른 차트 생성
def main():
    df = evo.trend_data_by_group(group_cd=['SEX_TP_CD'])
    df_trend = evo.get_trend_data()
    total_cols_nm = {'HID_cnt': 'HID_cnt_total', 'JID_cnt': 'JID_cnt_total', 'AMT_sum': 'AMT_sum_total',
                     'TOT_USE_QTY_OR_EXEC_FQ_sum': 'TOT_USE_QTY_OR_EXEC_FQ_sum_total'}
    df_trend_total = df_trend.rename(columns=total_cols_nm)
    df_sex_trend = pd.merge(df, df_trend_total, on=['RV_YM', 'GNL_NM_CD'])
    for col_nm in ['HID_cnt', 'JID_cnt', 'AMT_sum', 'TOT_USE_QTY_OR_EXEC_FQ_sum']:
        df_sex_trend['ratio_'+ col_nm] = df_sex_trend[col_nm] / df_sex_trend[col_nm + '_total']

    df_plot = df_sex_trend


    default_colors = ['Red', 'Blue', 'Green', 'Yellow', 'Pink']
    yyyymm = sorted(df.RV_YM.unique())

    dataList = ['환자수 비교', '진단수 비교', '총금액 비교', '총사용량 비교']
    dataColNm = ['HID_cnt', 'JID_cnt', 'AMT_sum', 'TOT_USE_QTY_OR_EXEC_FQ_sum']
    dataColNm = ['ratio_'+i for i in dataColNm]


    # ATC_CDS = ['N06DA02', 'N06DA03', 'N06DA04', 'N06DX01', 'N07AX02']
    GNL_CDS = evo.GNL_NM_CDS
    markertype = ['circle', 'triangle-up', 'square', 'diamond', 'cross']
    gubun_codes = ['남성']

    plotList = []
    row_num = 2
    col_num = 2


    for gubun_cd in gubun_codes:
        fig = make_subplots(rows=row_num, cols=col_num, shared_xaxes='all')
        df = df_plot.query(f'SEX_TP_CD == "{gubun_cd}"').copy()
        for colNm in dataColNm:
            for idx, cd in enumerate(GNL_CDS):
                inputdata = df.query(f'GNL_NM_CD== "{cd}"').sort_values(by='RV_YM')
                insert_p = go.Scatter(
                    mode="lines+markers",
                    name=f"{cd}",
                    x=yyyymm,
                    y=inputdata[colNm],
                    marker=dict(
                        symbol=markertype[idx],
                        color=default_colors[idx],
                        size=7,
                        line=dict(
                            color=default_colors[idx],
                            width=5
                        )),
                    showlegend=True
                )
                plotList.append(insert_p)
        # fig.update_yaxes(type="log")
        for i in range(0, 8):
            row_num = (i // 4 + 1)
            col_num = (i % 4) // 2 + 1
            fig.add_trace(plotList[i], row=row_num, col=col_num)

        title_name = '성별 GNL 코드별 추이분석'
        fig.update_layout(title=f'<b>{title_name}</b>')
        sex_name = gubun_cd
        fig.update_layout(
            dict(
                height=600,
                width=800,
                yaxis=dict(title=dict(text=f'{sex_name} 환자비율', standoff=0.2)),
                yaxis2=dict(title=dict(text=f'{sex_name} 진단 비율', standoff=0.2)),
                yaxis3=dict(title=dict(text=f'{sex_name} 총금액 비율', standoff=0.2)),
                yaxis4=dict(title=dict(text=f'{sex_name} 총사용량 비율', standoff=0.2)),
                xaxis3=dict(title='년/월'),
                xaxis4=dict(title='년/월')
            )
        )

        fig.layout.yaxis.title.standoff = 0.2


        file_name = '성별에 따른 GNL코드별_트렌드 분석'
        fig.write_html(full_html=True, file=f'{file_name}_{sex_name}.html')
        fig.write_image(format='png', file=f'{file_name}_{sex_name}.png')
    # fig.show()
    return 0



if __name__ == "__main__":
    main()