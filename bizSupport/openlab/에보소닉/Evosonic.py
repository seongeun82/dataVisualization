class Evo:
    from bizSupport.config.config import common_path_mac, common_path_linux
    import pandas as pd

    def __init__(self):
        self.common_path = self.common_path_linux
        # self.common_path = self.common_path_mac
        self.file_path = self.common_path + '/bizSupport/openlab/에보소닉/data/2648135854_비즈데이터_GNL_1102_수정.txt'
        self.value_codes = ['HID_cnt', 'JID_cnt', 'AMT_sum', 'TOT_USE_QTY_OR_EXEC_FQ_sum']

        self.GNL_NM_CDS = ['224507CPC', '148602ATD']

    def get_all_data(self):
        df = self.pd.read_csv(self.file_path, delimiter='\t')
        df['MSICK_CD'] = df['DW_MSICK_CD'].apply(lambda x: x[1:] if len(x[1:]) > 1 else x[1:] + '00')
        df['RV_YM'] = df['RV_YM'].apply(str)
        df['SIDO'] = df['SIDO'].apply(str)
        df['SEX_TP_CD'] = df['SEX_TP_CD'].apply(lambda x: '남성' if x == 1 else '여성')
        cl_cd_dict = {11: '종합병원', 21: '병원', 31: '의원',
                      28: '요양병원', 71: '보건소', 72: '보건지소',
                      92: "한방병원", 75: "보건의료원", 41: "치과병원",
                      51: "치과의원", 29: "정신병원"}
        sido_cd_dict = {"11": "서울", "21": "부산", "22": "인천", "23": "대구", "24": "광주", "25": "대전", "26": "울산", "31": "경기",
                        "32": "강원", "33": "충북", "34": "충남", "35": "전북", "36": "전남", "37": "경북", "38": "경남", "39": "제주"}
        df['SIDO'] = df['SIDO'].apply(lambda x: sido_cd_dict.get(x, '기타'))
        df['CL_CD'] = df['CL_CD'].apply(lambda x: cl_cd_dict.get(x, '기타'))
        df_sickcd = self.pd.read_excel(
            self.common_path + '/bizSupport/openlab/sick_code.xlsx')
        df_decoded = self.pd.merge(df, df_sickcd, left_on='MSICK_CD', right_on='SICK_CD')
        return df_decoded

    def get_total_comparision_data(self):
        df = self.get_all_data()
        df_comparison = df.groupby(['GNL_NM_CD'])[
            'HID_cnt', 'JID_cnt', 'AMT_sum', 'TOT_USE_QTY_OR_EXEC_FQ_sum'].sum().reset_index()
        return df_comparison

    def get_trend_data(self):
        df = self.get_all_data()
        df_trend = df.groupby(['RV_YM', 'GNL_NM_CD'])[self.value_codes].sum().reset_index()
        return df_trend

    def get_comparision_data(self, group_cd=[]):
        df = self.get_all_data()
        df_comparison = df.groupby(['GNL_NM_CD'] + group_cd)[self.value_codes].sum().reset_index()
        return df_comparison

    def trend_data_by_group(self, group_cd=[]):
        df = self.get_all_data()
        res = df.groupby(['RV_YM', 'GNL_NM_CD'] + group_cd)[self.value_codes].sum().reset_index()
        return res
