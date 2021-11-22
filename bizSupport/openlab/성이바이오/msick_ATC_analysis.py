# 단순히 저장하기 위해서 작성하였음
import pandas as pd
def all_data_merge():
    names = ['A02', 'A03', 'A04', 'X01', 'X02']
    atc_code_dict = {'A02': 'N06DA02', 'A03': 'N06DA03', 'A04': 'N06DA04',
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
    df = all_data_merge()
    df_msick_atc = df.groupby(['DW_MSICK_CD', 'ATC_CD'])['JID_cnt'].sum()
    # 전체 파일 각 코드 별 출력
    # 처방 순위 랭킹
    df_msick_atc =









    return 0


if __name__ == '__main__':
    msick_atc_main()
