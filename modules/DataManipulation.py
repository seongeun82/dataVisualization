class DataManipulation:
    import pandas as pd
    from bizSupport.config.config import common_path

    def __init__(self):
        self.data_nms = ['환자수', '내원일수', '청구건수', '요양급여비용총액', '보험자부담금']
        self.gb_nms = ['코드', '성별구분', '입원외래구분', '연령구분5세', '연령구분10세', '요양기관소재지구분', '요양기관그룹']
        # self.common_path = '/Users/imac/PycharmProjects/dataVisualization'



    def hira_excel_treats(self, df_raw):
        import re
        df = df_raw.copy()
        df = df.applymap(lambda x: x.replace(',', ''))
        df = df.replace({'-': None})  # <- 데이터 없음 파일 ''로 입력
        index_cols = [name in self.gb_nms for name in df.iloc[0, :]]
        re_com = re.compile(('([0-9]{4}년 [0-9]{2}월)'))
        yyyymm = [re_com.findall(i) for i in df.columns]
        yyyymm_list = sorted(set(sum(yyyymm, [])))

        res = []
        for year_month in yyyymm_list:
            value_index_year_mm = [i[0] == year_month if i else False for i in yyyymm]
            select_index = [value_index_year_mm[idx] | val for idx, val in enumerate(index_cols)]
            df_ym = df.loc[:, select_index].copy()
            df_ym.rename(columns=df.iloc[0], inplace=True)
            df_ym.drop(df.index[0], inplace=True)
            df_ym['yyyymm'] = year_month
            res.append(df_ym)
        return self.pd.concat(res)


    def get_inout_data_handling(self):
        df_inout = self.pd.read_excel(self.common_path + '/bizSupport/openlab/스몰머신즈/data/1_3단질병성별입원외래별현황(진료년월).xls')
        df_inout = self.hira_excel_treats(df_inout)
        df_in_1 = df_inout.query('성별구분 == "남" & 입원외래구분=="입원"').copy()
        df_in_2 = df_inout.query('성별구분 == "여" & 입원외래구분=="입원"').copy()
        df_out_1 = df_inout.query('성별구분 == "남" & 입원외래구분=="외래"')
        df_out_2 = df_inout.query('성별구분 == "여" & 입원외래구분=="외래"')

        df_inout[self.data_nms] = df_inout[self.data_nms].applymap(int)
        in_1 = df_in_1.set_index(['코드', '입원외래구분', 'yyyymm'])[self.data_nms].applymap(int)
        in_2 = df_in_2.set_index(['코드', '입원외래구분', 'yyyymm'])[self.data_nms].applymap(int)
        out_1 = df_out_1.set_index(['코드', '입원외래구분', 'yyyymm'])[self.data_nms].applymap(int)
        out_2 = df_out_2.set_index(['코드', '입원외래구분', 'yyyymm'])[self.data_nms].applymap(int)

        df_in = in_1 + in_2
        df_out = out_1 + out_2

        df_in = df_in.reset_index()
        df_out = df_out.reset_index()

        df_inout['진료비'] = df_inout['요양급여비용총액'] + df_inout['보험자부담금']
        df_in['진료비'] = df_in['요양급여비용총액'] + df_in['보험자부담금']
        df_out['진료비'] = df_out['요양급여비용총액'] + df_out['보험자부담금']
        return df_inout, df_in, df_out


    def get_sex_data_handling(self):
        df_inout, _, __ = self.get_inout_data_handling()
        df_sex = df_inout.groupby(['성별구분', 'yyyymm'])[['환자수', '내원일수', '청구건수', '요양급여비용총액', '보험자부담금', '진료비']].sum().reset_index()
        return df_sex


    def get_age_data_handling(self):
        df_age = self.pd.read_excel(self.common_path + '/bizSupport/openlab/스몰머신즈/data/1_3단질병성별연령5세구간별현황(진료년월).xls')
        df_age = self.hira_excel_treats(df_age)
        df_age.fillna(0, inplace=True)
        df_age[self.data_nms] = df_age[self.data_nms].applymap(int)
        df_age['진료비'] = df_age['요양급여비용총액'] + df_age['보험자부담금']
        df_age = df_age.groupby(['연령구분5세', 'yyyymm'])[['환자수', '내원일수', '청구건수', '요양급여비용총액', '보험자부담금', '진료비']].sum().reset_index()
        return df_age

    def get_region_data_handling(self):
        df_region = self.pd.read_excel(self.common_path + '/bizSupport/openlab/스몰머신즈/data/1_3단질병요양기관소재지별현황(진료년월) .xls')
        df_region = self.hira_excel_treats(df_region)
        df_region.fillna(0, inplace=True)
        df_region[self.data_nms] = df_region[self.data_nms].applymap(int)
        df_region['진료비'] = df_region['요양급여비용총액'] + df_region['보험자부담금']
        df_region = df_region.groupby(['요양기관소재지구분', 'yyyymm'])[
            ['환자수', '내원일수', '청구건수', '요양급여비용총액', '보험자부담금', '진료비']].sum().reset_index()
        return df_region

    def get_ykiho_data_handling(self, file_path , label_col_nm):
        df = self.pd.read_excel(self.common_path + file_path)
        df = self.hira_excel_treats(df)
        df.fillna(0, inplace=True)
        df[self.data_nms] = df[self.data_nms].applymap(int)
        df['진료비'] = df['요양급여비용총액'] + df['보험자부담금']
        df = df.groupby([label_col_nm, 'yyyymm'])[
            ['환자수', '내원일수', '청구건수', '요양급여비용총액', '보험자부담금', '진료비']].sum().reset_index()
        return df


























