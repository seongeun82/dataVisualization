import plotly.graph_objects as go
from plotly.subplots import make_subplots


def main():
    from Evosonic import Evo
    evo = Evo()
    df = evo.get_trend_data()
    default_colors = ['Red', 'Blue', 'Green', 'Yellow', 'Pink']
    yyyymm = sorted(df.RV_YM.unique())
    dataList = ['환자수 비교', '진단수 비교', '총금액 비교', '총사용량 비교']

    GNL_NM_CDS = ['148602ATD', '224507CPC']
    markertype = ['circle', 'triangle-up', 'square', 'diamond', 'cross']

    plotList = []
    fig = make_subplots(rows=2, cols=2, shared_xaxes='all')
    for colNm in evo.value_codes:
        for idx, cd in enumerate(GNL_NM_CDS):
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
    fig.update_yaxes(type="log")
    for i in range(0, 8):
        row_num = (i // 10 + 1)
        col_num = (i % 10) // 5 + 1
        fig.add_trace(plotList[i], row=row_num, col=col_num)

    title_name = 'ATC코드별 추이분석'
    fig.update_layout(title=f'<b>{title_name}</b>')

    fig.update_layout(
        dict(
            height=600,
            width=800,
            yaxis=dict(title=dict(text='환자수', standoff=0.2)),
            yaxis2=dict(title=dict(text='진단수', standoff=0.2)),
            yaxis3=dict(title=dict(text='총금액', standoff=0.2)),
            yaxis4=dict(title=dict(text='총사용량', standoff=0.2)),
            xaxis3=dict(title='년/월'),
            xaxis4=dict(title='년/월')
        )
    )

    fig.layout.yaxis.title.standoff = 0.2

    file_name = 'ATC코드별_트렌드분석'
    fig.write_html(full_html=True, file=f'{file_name}.html')
    fig.write_image(format='png', file=f'{file_name}.png')

    return 0

    df_data = evo.get_total_comparision_data()
    specs = [[{'type': 'domain'}, {'type': 'domain'}], [{'type': 'domain'}, {'type': 'domain'}]]
    sub_titles = ['환자수 비교', '진단수 비교', '총금액 비교', '총사용량 비교']
    fig = make_subplots(rows=2, cols=2, specs=specs, subplot_titles=sub_titles)
    data_info = [{"name": '환자수',
                  "code": "HID_cnt",
                  "title": "환자수 비교"},
                 {"name": '진단수',
                  "code": "JID_cnt",
                  "title": "진단수 비교"},
                 {"name": '총금액',
                  "code": "AMT_sum",
                  "title": "총금액 비교"},
                 {"name": '총사용량',
                  "code": "TOT_USE_QTY_OR_EXEC_FQ_sum",
                  "title": "총사용량 비교"}
                 ]
    fig_res = []
    for fig_info in data_info:
        fig_res.append(go.Pie(
            values=df_data[fig_info.get('code')],
            labels=df_data['GNL_NM_CD'],
            name=fig_info.get('name')
        ))

    for idx, sub_fig in enumerate(fig_res):
        row_col = [(1, 1), (1, 2), (2, 1), (2, 2)]
        (row, col) = row_col[idx]
        fig.add_trace(sub_fig, row=row, col=col)

    fig.update_layout(
        dict(
            height=600,
            width=800
        )
    )
    file_name = '주성분코드 규모비교'
    fig.write_html(full_html=True, file=f'{file_name}.html')
    fig.write_image(format='png', file=f'{file_name}.png')
    return 0




if __name__ == "__main__":
    main()



