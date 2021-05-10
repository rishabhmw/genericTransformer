import pandas as pd


class Transformer:

    @staticmethod
    def transform(input_df: pd.DataFrame, col_map_df: pd.DataFrame,
                  static_map_df: pd.DataFrame) -> pd.DataFrame:

        """
        This method transforms the input_df according to col_map_df and
        static_map_df.
        :param input_df: pandas.DataFrame
        DataFrame of the input to be transformed.
        :param col_map_df: pandas.DataFrame
        The col_map_df specifies what cols in output should be mapped to
        which input_df col. If the mapping is blank then that col isn't
        mapped with any of the input_df col.
        :param static_map_df: pandas.DataFrame
        The static_map_df is then used to set a col value based on the value
        of some other col in the same row.
        :return: pandas.DataFrame
        """

        op_df = pd.DataFrame()
        for row in range(len(col_map_df.index)):
            op_col = col_map_df.iloc[row, 0]
            ip_col = col_map_df.iloc[row, 1]

            if pd.isna(ip_col):
                op_df[op_col] = ''
            else:
                op_df[op_col] = input_df[ip_col]

        rule_groups = static_map_df.groupby('Deciding Column')
        rules = dict()
        for rule_group in rule_groups.groups:
            # create dict such as -> {USD:[aff_col,aff_val],...}
            rule_group_df = rule_groups.get_group(rule_group)
            rule_dict = dict()
            for rule in range(len(rule_group_df.index)):
                key = rule_group_df.iloc[rule]['Deciding Value']
                val = [rule_group_df.iloc[rule]['Affected Column'],
                       rule_group_df.iloc[rule]['Affected Value']]
                if key in rule_dict:
                    rule_dict[key].append(val)
                else:
                    rule_dict[key] = [val]
            rules[rule_group] = rule_dict

        for row in range(len(op_df.index)):
            for deciding_col, affects in rules.items():
                val = op_df.iloc[row][deciding_col]
                if val in affects:
                    for affect_list in affects[val]:
                        op_df.loc[row, affect_list[0]] = affect_list[1]
        print(op_df)

        return op_df
