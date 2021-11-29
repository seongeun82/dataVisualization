import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots



def all_data_merge():
    names = ['A02', 'A03', 'A04', 'X01', 'X02']
    atc_code_dict = {'A02': 'N06DA02',
                     'A03': 'N06DA03',
                     'A04': 'N06DA04',
                     'X01': 'N06DX01',
                     'X02': 'N07AX02'}

    path1 = '/Users/imac/PycharmProjects/dataVisualization/bizSupport/openlab/성이바이오/data/2648135854_비즈데이터_RESULT_{atc_cd}.txt'
    path2 = '/Users/imac/PycharmProjects/dataVisualization/bizSupport/openlab/성이바이오/data/2648135854_비즈데이터_RESULT_{atc_cd}_1026.txt'

    res = []
    for atc_cd in names:
        for path in [path1, path2]:
            df = pd.read_csv(path.format(atc_cd=atc_cd), delimiter='|')
            df['ATC_CD'] = atc_code_dict.get(atc_cd)
            res.append(df)
    df_res = pd.concat(res)
    return df_res

def trend_data_by_group(group_cd = []):
    df = all_data_merge()
    df['RV_YM'] = df['RV_YM'].apply(str)
    values = ['HID_cnt', 'JID_cnt', 'AMT_sum', 'TOT_USE_QTY_OR_EXEC_FQ_sum']
    res = df.groupby(['RV_YM', 'ATC_CD'] + group_cd)[values].sum().reset_index()
    return res


def get_comparison_data(group_cd=[]):
    df = all_data_merge()
    df['RV_YM'] = df['RV_YM'].apply(str)
    values = ['HID_cnt', 'JID_cnt', 'AMT_sum', 'TOT_USE_QTY_OR_EXEC_FQ_sum']
    res = df.groupby(['ATC_CD'] + group_cd)[values].sum().reset_index()
    return res


def draw_comparison_plot():
    df_data = get_comparison_data()
    # 환자수, 사용기관수, 총금액, 총사용량
    specs = [[{'type': 'domain'}, {'type': 'domain'}], [{'type': 'domain'}, {'type': 'domain'}]]
    sub_titles = ['환자수 비교', '진단수 비교', '총금액 비교', '총사용량 비교']
    fig = make_subplots(rows=3, cols=2, specs=specs,
                        subplot_titles=sub_titles)
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
            labels=df_data['ATC_CD'],
            name=fig_info.get('name')
        ))

    for idx, sub_fig in enumerate(fig_res):
        row_col = [(1, 1), (1, 2), (2, 1), (2, 2), (3,1)]
        (row, col) = row_col[idx]
        fig.add_trace(sub_fig, row=row, col=col)

    fig.update_layout(
        dict(
            height=600,
            width=800
        )
    )
    file_name = 'ATC코드별 성별 규모비교'
    fig.write_html(full_html=True, file=f'{file_name}.html')
    fig.write_image(format='png', file=f'{file_name}.png')
    return 0


if __name__ == '__main__':
    draw_comparison_plot()
