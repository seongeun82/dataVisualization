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
    # fig.update_yaxes(type="log")
    for i in range(0, 8):
        row_num = (i // 4 + 1)
        col_num = (i % 4) // 2 + 1
        fig.add_trace(plotList[i], row=row_num, col=col_num)

    title_name = '주성분 코드별 추이분석'
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

    file_name = '주성분코드별_트렌드분석'
    fig.write_html(full_html=True, file=f'{file_name}.html')
    fig.write_image(format='png', file=f'{file_name}.png')

    return 0



if __name__ == "__main__":
    main()



