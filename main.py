import re
import pandas as pd

csv = pd.read_csv(r'D:\Users\myusername\Desktop\pathpath\filename.csv', encoding='unicode_escape')

cols = ['date', 'payment_type', 'transaction', 'paid', 'daily_balance']
full_df = pd.DataFrame(columns=cols)

for index, row in csv.iterrows():
    bank_statement_string = csv['full_statement'][index]
    continuous_bank_statement_string = re.sub(
        '([0-9]{2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2}) BALANCE BROUGHT FORWARD .*?used by deaf or speech impaired customers',
        '', bank_statement_string)  # removes header and footer in between the data
    continuous_bank_statement_string = re.sub(
        'BALANCE CARRIED FORWARD .*?used by deaf or speech impaired customers',
        '', continuous_bank_statement_string)  # removes header and footer in between the data
    continuous_bank_statement_string = re.sub(
        'Credit inte re st 0.00% upto 500 0.00% ove r 500 .*$',
        '', continuous_bank_statement_string)   # removes document end
    continuous_bank_statement_string = re.sub(
        'BALANCE BROUGHT FORWARD',
        '', continuous_bank_statement_string)

    split_string = re.split(r'([0-9]{2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2})', continuous_bank_statement_string) # makes each date a
    split_string_df = pd.DataFrame(split_string)

    split_string_df.drop(split_string_df.head(1).index, inplace=True)

    dated_df = pd.DataFrame({'date':split_string_df[0].iloc[::2].values, 'transactions':split_string_df[0].iloc[1::2].values})
    dated_df['transactions'] = dated_df['transactions'].str.strip()

    if dated_df.tail(1).iloc[0]['transactions'] == "":
        dated_df.drop(dated_df.tail(1).index, inplace=True)  # remove document end

    dated_df['transactions'] = dated_df['transactions'].str.strip()
    dated_df['daily_balance'] = dated_df.transactions.str.extract('((?:\d+)?,?\d+(?:\.\d+)?)$')
    dated_df['transactions'] = dated_df['transactions'].str.replace('((?:\d+)?,?\d+(?:\.\d+)?)$', '').str.strip()

    dated_df['listed_transactions'] = ""
    for index, row in dated_df.iterrows():
        transaction_record = re.split(r'((?:\d+)?,?\d+(?:\.\d+))', dated_df['transactions'][index])
        dated_df['listed_transactions'][index] = [i+j for i, j in zip(transaction_record[::2], transaction_record[1::2])]

    dated_df = dated_df.explode('listed_transactions')
    dated_df = dated_df.drop(columns='transactions')

    dated_df['transaction'] = dated_df['listed_transactions'].str.strip()
    dated_df = dated_df.drop(columns='listed_transactions')

    dated_df['paid'] = dated_df.transaction.str.extract('((?:\d+)?,?\d+(?:\.\d+)?)$')
    dated_df['transaction'] = dated_df['transaction'].str.replace('((?:\d+)?,?\d+(?:\.\d+)?)$', '').str.strip()

    dated_df['payment_type'] = dated_df.transaction.str.extract('(?P<transaction>.{3})')
    dated_df['payment_type'] = dated_df['payment_type'].str.strip()

    dated_df['transaction'] = dated_df['transaction'].str[3:]
    dated_df['transaction'] = dated_df['transaction'].str.strip()

    dated_df = dated_df[cols]
    full_df = full_df.append(dated_df)

full_df.to_csv(r'D:\Users\username\Desktop\parsed_statement.csv')
