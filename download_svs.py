import pandas as pd
import argparse
import os

args = argparse.ArgumentParser()
args.add_argument('-d', '--drug', type=str, nargs='+')  # 여러 약물 이름을 받을 수 있도록 수정
args.add_argument('-t', '--type', choices=['aria2c', 'axel'], default='aria2c')

args = args.parse_args()

# df = pd.read_csv('../0.Data/TG-GATE/svsfiles.csv')
df = pd.read_csv('/home/local/yooeunkim_980629/MedAI/0.Data/TG-GATE/svsfiles.csv')

for drug in args.drug:  # 여러 약물을 처리하는 루프
    drug_name = drug.replace(' ', '_')

    os.makedirs(f'/home/local/yooeunkim_980629/MedAI/0.Data/TG-GATE/SVS/{drug_name}', exist_ok=True)

    df_drug = df[df['COMPOUND_NAME_x'] == drug]
    
    for i, (_, row) in enumerate(df_drug.iterrows()):
        if row['FILE_LOCATION'].split('/')[-1] in os.listdir(f'/home/local/yooeunkim_980629/MedAI/0.Data/TG-GATE/SVS/{drug_name}'):
            print(f'{row["FILE_LOCATION"].split("/")[-1]} already exists')
        else:
            print(f'Downloading {i}/{len(df_drug)} for {drug_name}')
            if args.type == 'aria2c':
                file_location = f'https://dbarchive.biosciencedbc.jp/data/open-tggates-pathological-images/LATEST/images/{drug_name}/Liver/{row["FILE_LOCATION"].split("/")[-1]}'
                os.system(f"aria2c -x 8 {file_location} -d /home/local/yooeunkim_980629/MedAI/0.Data/TG-GATE/SVS/{drug_name}/")
            else:
                os.system(f"axel -a -n 8 {row['FILE_LOCATION']} -o /home/local/yooeunkim_980629/MedAI/0.Data/TG-GATE/SVS/{drug_name}/{row['FILE_LOCATION'].split('/')[-1]}")
