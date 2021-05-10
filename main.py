from Transformer import Transformer
import pandas as pd


def main():
    input_df = pd.read_csv('input_data.csv')
    col_map_df = pd.read_csv('col_map.csv')
    static_map_df = pd.read_csv('static_map.csv')
    output = Transformer.transform(input_df, col_map_df, static_map_df)
    output.to_csv('output.csv')


if __name__ == '__main__':
    main()
