import plotly.graph_objects as go
from plotly.subplots import make_subplots


def main():
    from Evosonic import Evo
    evo = Evo()
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