import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from Evosonic import Evo
evo = Evo()

def draw_comparison_plot_for_each_ATC():
    group_cd = 'CL_CD'
    title_name = '요양기관별'
    df_all = evo.get_comparision_data(group_cd=[group_cd])
    # 환자수, 사용기관수, 총금액, 총사용량
    specs = [[{'type': 'domain'}, {'type': 'domain'}], [{'type': 'domain'}, {'type': 'domain'}]]
    sub_titles = ['환자수 비교', '진단수 비교', '총금액 비교', '총사용량 비교']
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

    for gnl_cd in evo.GNL_NM_CDS:
        df_data = df_all.query(f'GNL_NM_CD =="{gnl_cd}"')
        fig = make_subplots(rows=2, cols=2, specs=specs,
                            subplot_titles=sub_titles)

        fig_res = []
        for fig_info in data_info:
            fig_res.append(go.Pie(
                values=df_data[fig_info.get('code')],
                labels=df_data[group_cd],
                name=fig_info.get('name')
            ))

        for idx, sub_fig in enumerate(fig_res):
            row_col = [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1)]
            (row, col) = row_col[idx]
            fig.add_trace(sub_fig, row=row, col=col)

        fig.update_layout(
            dict(
                height=600,
                width=800,
                title_text=f'GNL_CODE: {gnl_cd}'
            )

        )
        file_name = f'{gnl_cd}_{title_name} 규모비교'
        fig.write_html(full_html=True, file=f'{file_name}.html')
        fig.write_image(format='png', file=f'{file_name}.png')

    return 0


if __name__ == '__main__':
    draw_comparison_plot_for_each_ATC()
