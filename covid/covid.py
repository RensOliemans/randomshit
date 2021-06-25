import locale

import numpy as np
import pandas as pd

locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')


def main():
    print('Loading document...')
    df = pd.read_csv('COVID-19_casus_landelijk.csv', delimiter=';')
    print(f'Total amount of Covid cases in the Netherlands: {len(df):n}')

    deceased = df[df.Deceased == 'Yes']
    print(f'Total amount of deaths due to Covid: {len(deceased):n}')

    agegroups = ['<50', '50-59', '60-69', '70-79', '80-89', '90+']
    for agegroup in agegroups:
        if agegroup == '<50':
            # The csv has '<50' when talking about deceased, and individual age groups when talking about tests
            positive = df.loc[np.where((df.Agegroup == '0-9') | (df.Agegroup == '10-19') |
                                       (df.Agegroup == '20-29') | (df.Agegroup == '30-39') |
                                       (df.Agegroup == '40-49'))]
        else:
            positive = df[df.Agegroup == agegroup]
        deaths = df.loc[np.where((df.Agegroup == agegroup) & (df.Deceased == 'Yes'))]
        print(f'Age group {agegroup.ljust(5)} has {len(positive):n} positive cases and {len(deaths):n} deaths. '
              f'So {len(deaths) / len(positive):.3%} of the positively tested cases have died.')
    print(f'In total, {len(deceased) / len(df):.3%} of the positively tested cases have died.')
    print('The stated percentage is incomplete and cannot be used as a chance to die from Covid. This is in part due '
          'to the fact that people can be tested positive for Covid twice (and can only die once, pushing the % '
          'up). Furthermore, people can have Covid without getting a (positive) test, pushing the % down.')


if __name__ == '__main__':
    main()
