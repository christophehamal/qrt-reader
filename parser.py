import pandas as pd
import re

class QRTParser:
    
    def s050102_part1(self, company, year, data):
        
        LoBs = [
            "C0010",
            "C0020",
            "C0030",
            "C0040",
            "C0050", 
            "C0060",
            "C0070",
            "C0080",
            "C0090",
            "C0100",
            "C0110",
            "C0120",
            "C0130", 
            "C0140",
            "C0150", 
            "C0160",
            "C0200"
        ]

        df = self._s050102_common(company, year, data)
        df['LoB'] = df.apply(lambda row: LoBs[int(row.name)], axis=1)

        return df
    
    def s050102_part2(self, company, year, data):
        
        LoBs = [
            "C0010",
            "C0020",
            "C0030",
            "C0040",
            "C0050", 
            "C0060",
            "C0070",
            "C0080",
            "C0090",
            "C0100",
            "C0110",
            "C0120",
            "C0130", 
            "C0140",
            "C0150", 
            "C0160",
            "C0200"
        ]

        df = self._s050102_common(company, year, data)
        df['LoB'] = df.apply(lambda row: LoBs[len(LoBs) - (len(df.index)-int(row.name))], axis=1)

        return df

    def _s050102_common(self, company, year, data):

        # Number formatting (should be company specific)
        thousandseparator = '.'
        zerocharacter = '-'

        # Standard QRT lines and LoBs
        lines21 = [
            'Premiums written', 
            'Premiums written: Gross - Direct Business',
            'Premiums written: Gross - Proportional reinsurance accepted',
            'Premiums written: Gross - Non-proportional reinsurance accepted',
            "Premiums written: Reinsurers' share",
            'Premiums written: Net', 
            'Premiums earned', 
            'Premiums earned: Gross - Direct Business',
            'Premiums earned: Gross - Proportional reinsurance accepted',
            'Premiums earned: Gross - Non-proportional reinsurance accepted', 
            "Premiums earned: Reinsurers' share",
            'Premiums earned: Net', 
            'Claims incurred', 
            'Claims incurred: Gross - Direct Business',
            'Claims incurred: Gross - Proportional reinsurance accepted',
            'Claims incurred: Gross - Non-proportional reinsurance accepted', 
            "Claims incurred: Reinsurers' share",
            'Claims incurred: Net', 
            'Expenses incurred', 
            'Other expenses', 
            'Total expenses'
        ]

        lines27 = [
            'Premiums written', 
            'Premiums written: Gross - Direct Business',
            'Premiums written: Gross - Proportional reinsurance accepted',
            'Premiums written: Gross - Non-proportional reinsurance accepted',
            "Premiums written: Reinsurers' share",
            'Premiums written: Net', 
            'Premiums earned', 
            'Premiums earned: Gross - Direct Business',
            'Premiums earned: Gross - Proportional reinsurance accepted',
            'Premiums earned: Gross - Non-proportional reinsurance accepted', 
            "Premiums earned: Reinsurers' share",
            'Premiums earned: Net', 
            'Claims incurred', 
            'Claims incurred: Gross - Direct Business',
            'Claims incurred: Gross - Proportional reinsurance accepted',
            'Claims incurred: Gross - Non-proportional reinsurance accepted', 
            "Claims incurred: Reinsurers' share",
            'Claims incurred: Net',
            'Changes in other technical provisions',
            'Changes in other technical provisions: Gross - Direct Business',
            'Changes in other technical provisions: Gross - Proportional reinsurance accepted',
            'Changes in other technical provisions: Gross - Non-proportional reinsurance accepted',
            "Changes in other technical provisions: Reinsurers'share",
            'Changes in other technical provisions: Net',
            'Expenses incurred', 
            'Other expenses', 
            'Total expenses'
        ]

        # Transpose data from QRT
        df = pd.DataFrame(data)[1:].transpose()
        
        # Find column names
        headerCol = 0
        for index, row in df.iterrows():
            present = row.map(lambda x: 'gross' in str(x).lower()).any()
            if present:
                headerCol = index
                break
        df = df[headerCol:]
        df.columns = df.iloc[0]
        df = df[1:]

        # Remove coded headers
        map_ = df.apply(lambda row: not(row.map(lambda x: 'R011' in str(x)).any()), axis=1)
        df = df.loc[map_]
        map_ = df.apply(lambda row: not(row.map(lambda x: 'C0' in str(x)).any()), axis=0)
        df = df.loc[:, map_.tolist()]

        # Implement standard QRT line labels
        if len(df.columns) > 21:
            map_ = df.columns.map(lambda x: (x not in ['', 'None', 'in EUR', 'in thousand EUR']) and (x is not None))
            df = df.loc[:, map_.tolist()]

        match len(df.columns):
            case 21:
                df.columns = lines21
            case 26:
                df.loc[:, 'Premiums written'] = ''
                df.columns = lines27
            case 27:
                df.columns = lines27
        df = df.drop(["Premiums written", "Premiums earned", "Claims incurred"], axis=1)

        # Clean up cell content to make numeric
        df = df.map(lambda x: re.sub('[ +' + zerocharacter + thousandseparator + ']', '', str(x)))

        # Implement standard QRT LoBs and add company and year
        df = df.reset_index(drop=True)
        df['Company'] = company
        df['Year'] = year

        return df