class Figures:
    from plotly.subplots import make_subplots
    from modules.DataManipulation import DataManipulation
    import plotly.graph_objects as go

    data = DataManipulation()

    def __init__(self):
        self.default_colors = ['Red', 'Blue', 'Green', 'Yellow']
        self.multi_colors = ['rgba(1, 102, 150, 255)', 'rgba(108, 71, 114, 25)', 'rgba(100, 158, 11, 255)',
                             'rgba(246, 147, 30. 255)', 'rgba(208, 67, 66, 255)', 'rgba(0,176,176,255)',
                             'rgba(99,189,234,255)', 'rgba(149,96,157,255)',
                             'rgba(161,202,100,255)', 'rgba(251,175,64,255)', 'rgba(201,121,129,255)',
                             'rgba(66,220,218,255)']
        self.marker_types = ['circle', 'triangle-up', 'square', 'diamond',
                             'cross', 'star', 'pentagon', 'diamond-wide',  'x', 'hexagram',
                             'asterisk', 'diamond-tall']
        self.markers24 = sum([[i + j for i in self.marker_types ] for j in ['','-open']], [])

        self.marker_numbers = [225, 226, 227, 228, 229, 230, 231, 232, 233, 234,235, 237,
                           238, 239, 240, 241, 242, 243, 244, 245,246, 247, 248, 249, 250, 251, 252,
                          325, 326, 327, 328, 329, 330, 331, 332, 333, 334,325, 326, 327,
                           328, 329, 330, 331, 332, 333, 334,325, 326, 327, 328, 329, 330, 331, 332, 333, 334,
                          335, 337, 338, 339, 340, 341, 342, 343, 344, 345,346, 347, 348, 349, 350, 351, 352]




    def get_sub_plot_example(self):
        df_inout, df_in, df_out = self.data.get_inout_data_handling()
        yyyymm = sorted(df_inout.yyyymm.unique())
        dataList = ['환자수', '내원일수', '청구건수', '요양급여비용총액']
        plotList = [self.go.Scatter(
            mode="lines+markers",
            # name="전체",
            x=yyyymm,
            y=df_inout.query('성별구분 == "계"')[self.data.data_nms[i]],
            marker=dict(
                color=self.default_colors[i],
                size=7,
                line=dict(
                    color=self.default_colors[i],
                    width=5
                )),
            showlegend=False
        ) for i in [0, 1, 2, 3]]

        fig = self.make_subplots(rows=2, cols=2, shared_xaxes='all')
        fig.add_trace(plotList[0], row=1, col=1)
        fig.add_trace(plotList[1], row=1, col=2)
        fig.add_trace(plotList[2], row=2, col=1)
        fig.add_trace(plotList[3], row=2, col=2)

        fig.update_layout(
            dict(
                yaxis=dict(title='환자수',
                           standoff=0.2),
                yaxis2=dict(title='내원일수'),
                xaxis3=dict(title='년/월'),
                yaxis3=dict(title='청구건수'),
                xaxis4=dict(title='년/월'),
                yaxis4=dict(title='요양급여비용총액'),
            )
        )

        # ['환자수', '내원일수', '청구건수', '요양급여비용총액'

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

        fig.write_html(full_html=True, file='./aa.html')
        fig.write_image(format='png', file='./aa.png')

        return fig
