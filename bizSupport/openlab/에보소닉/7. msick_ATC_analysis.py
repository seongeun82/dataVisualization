import pandas as pd
from Evosonic import Evo
evo = Evo()

def msick_atc_main():
    df = evo.get_all_data()
    df_msick_atc = df.groupby(['SICK_CD','SICK_CD_NM', 'GNL_NM_CD'])['JID_cnt'].sum().reset_index()

    for gnl_code in evo.GNL_NM_CDS :
        query = f'GNL_NM_CD == "{gnl_code}"'
        df_tmp = df_msick_atc.query(query) \
            .sort_values(by='JID_cnt', ascending=False) \
            .reset_index(drop=True) \
            .rename(columns={'JID_cnt': 'cnt'})
        df_tmp.to_excel('./{fileName}.xlsx'.format(fileName=gnl_code))
    return 0


if __name__ == '__main__':
    msick_atc_main()
