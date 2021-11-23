# 단순히 저장하기 위해서 작성하였음
import pandas as pd


def all_data_merge():
    names = ['A02', 'A03', 'A04', 'X01', 'X02']
    atc_code_dict = {'A02': 'N06DA02', 'A03': 'N06DA03',
                     'A04': 'N06DA04',
                     'X01': 'N06DX01', 'X02': 'N07AX02'}
    path1 = '/home/seongeun/PycharmProjects/dataVisualization/bizSupport/openlab/성이바이오/data/2648135854_비즈데이터_RESULT_{atc_cd}.txt'
    path2 = '/home/seongeun/PycharmProjects/dataVisualization/bizSupport/openlab/성이바이오/data/2648135854_비즈데이터_RESULT_{atc_cd}_1026.txt'
    res = []
    for atc_cd in names:
        for path in [path1, path2]:
            df = pd.read_csv(path.format(atc_cd=atc_cd), delimiter='|')
            df['ATC_CD'] = atc_code_dict.get(atc_cd)
            res.append(df)
    df_res = pd.concat(res)
    return df_res


def msick_atc_main():
    atc_code_dict = {'A02': 'N06DA02', 'A03': 'N06DA03', 'A04': 'N06DA04',
                     'X01': 'N06DX01', 'X02': 'N07AX02'}
    df = all_data_merge()
    df_msick_atc = df.groupby(['DW_MSICK_CD', 'ATC_CD'])['JID_cnt'].sum().reset_index()
    df_msick_atc['MSICK_CD'] = df_msick_atc['DW_MSICK_CD'].apply(lambda x: x[1:] if len(x[1:]) > 1 else x[1:] + '00')
    df_sickcd = pd.read_excel('/home/seongeun/PycharmProjects/dataVisualization/bizSupport/openlab/sick_code.xlsx')
    df_msick_atc = pd.merge(df_msick_atc, df_sickcd, left_on='MSICK_CD', right_on='SICK_CD')

    for atc_code in list(atc_code_dict.values()):
        query = 'ATC_CD == "{atc_code}"'.format(atc_code=atc_code)
        df_tmp = df_msick_atc.query(query) \
            .sort_values(by='JID_cnt', ascending=False) \
            .reset_index(drop=True) \
            .rename(columns={'JID_cnt': 'cnt'}) \
            .drop('YID_cnt', inplace=True)
        df_tmp.to_excel('./{fileName}.xlsx'.format(fileName=atc_code))
    return 0


if __name__ == '__main__':
    msick_atc_main()
