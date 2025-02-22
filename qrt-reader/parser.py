import pandas as pd
import re

class QRTParser:
    LOB_S = [
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

    def s05010201_part1(self, company, year, data):
        
        df = self._s05010201_common(company, year, data)
        df['LoB'] = df.apply(lambda row: self.LOB_S[int(row.name)], axis=1)

        return df
    
    def s05010201_part2(self, company, year, data):
        
        df = self._s05010201_common(company, year, data)
        df['LoB'] = df.apply(lambda row: self.LOB_S[len(self.LOB_S) - (len(df.index)-int(row.name))], axis=1)

        return df

    def _s05010201_common(self, company, year, data):

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
        lines23 = [
            'Premiums written: Gross - Direct Business',
            'Premiums written: Gross - Proportional reinsurance accepted',
            'Premiums written: Gross - Non-proportional reinsurance accepted',
            "Premiums written: Reinsurers' share",
            'Premiums written: Net', 
            'Premiums earned: Gross - Direct Business',
            'Premiums earned: Gross - Proportional reinsurance accepted',
            'Premiums earned: Gross - Non-proportional reinsurance accepted', 
            "Premiums earned: Reinsurers' share",
            'Premiums earned: Net', 
            'Claims incurred: Gross - Direct Business',
            'Claims incurred: Gross - Proportional reinsurance accepted',
            'Claims incurred: Gross - Non-proportional reinsurance accepted', 
            "Claims incurred: Reinsurers' share",
            'Claims incurred: Net',
            'Changes in other technical provisions: Gross - Direct Business',
            'Changes in other technical provisions: Gross - Proportional reinsurance accepted',
            'Changes in other technical provisions: Gross - Non-proportional reinsurance accepted',
            "Changes in other technical provisions: Reinsurers'share",
            'Changes in other technical provisions: Net',
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
        codes_present = False
        for index, row in df.iterrows():
            codes_present = row.map(lambda x: 'R01' in str(x)).any()
            if codes_present:
                headerCol = index
                break
        if not codes_present:
            for index, row in df.iterrows():
                present = row.map(lambda x: 'gross' in str(x).lower()).any()
                if present:
                    headerCol = index
                    break
        df = df[headerCol:]
        df.columns = df.iloc[0]
        df = df[1:]

        # Remove coded headers
        map_ = df.apply(lambda row: not(row.map(lambda x: 'R01' in str(x)).any()), axis=1)
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
            case 23:
                df.columns = lines23
            case 26:
                df.loc[:, 'Premiums written'] = ''
                df.columns = lines27
            case 27:
                df.columns = lines27
        try:
            df = df.drop(["Premiums written", "Premiums earned", "Claims incurred"], axis=1)
        except KeyError:
            df = df.drop(["Premiums written", "Premiums earned", "Claims incurred"], axis=1, errors='ignore')

        # Clean up cell content to make numeric
        df = df.map(lambda x: re.sub('[ +' + zerocharacter + thousandseparator + ']', '', str(x)))

        # Implement standard QRT LoBs and add company and year
        df = df.reset_index(drop=True)
        df['Company'] = company
        df['Year'] = year

        # split merged cell contents
        for row_index, row in df.iterrows():
            for column_index in range(len(row)):
                if '\n' in str(row.iloc[column_index]):
                    cell_lines = str(row.iloc[column_index]).split('\n')
                    for line_counter in range(len(cell_lines)):
                        df.iloc[row_index, column_index+line_counter] = cell_lines[line_counter]
        
        return df
    
    def s17010201_part1(self, company, year, data):

        df = self._s17010201_common(company, year, data)
        df['LoB'] = df.apply(lambda row: self.LOB_S[int(row.name)], axis=1)

        return df
    
    def s17010201_part2(self, company, year, data):
        
        df = self._s17010201_common(company, year, data)
        df['LoB'] = df.apply(lambda row: self.LOB_S[len(self.LOB_S) - (len(df.index)-int(row.name))], axis=1)

        return df

    def _s17010201_common(self, company, year, data):

        # Number formatting (should be company specific)
        thousandseparator = '.'

        # Standard QRT lines
        lines14 = [
            'Technical provisions calculated as a whole',
            'Total Recoverables from reinsurance/SPV and Finite Re after the adjustment for expected losses due to counterparty default associated to TP calculated as a whole',
            'Gross premium provisions',
            'Total recoverable from reinsurance/SPV and Finite Re after the adjustment for expected losses due to counterparty default',
            'Net Best Estimate of Premium Provisions', 
            'Gross claims provisions',
            'Total recoverable from reinsurance/SPV and Finite Re after the adjustment for expected\nlosses due to counterparty default',
            'Net Best Estimate of Claims Provisions',
            'Total Best estimate - gross', 
            'Total Best estimate - net',
            'Risk margin', 
            'Technical provisions - total',
            'Recoverable from reinsurance contract/SPV and Finite Re after the adjustment for expected losses due to counterparty default - total',
            'Technical provisions minus recoverables from reinsurance/SPV and Finite Re - total'
        ]
        lines19 = [
            'Technical provisions calculated as a whole',
            'Total Recoverables from reinsurance/SPV and Finite Re after the adjustment for expected losses due to counterparty default associated to TP calculated as a whole',
            'Technical provisions calculated as a sum of BE and RM',
            'Best estimate', 
            'Premium provisions', 
            'Gross premium provisions',
            'Total recoverable from reinsurance/SPV and Finite Re after the adjustment for expected losses due to counterparty default',
            'Net Best Estimate of Premium Provisions', 
            'Claims provisions',
            'Gross claims provisions',
            'Total recoverable from reinsurance/SPV and Finite Re after the adjustment for expected\nlosses due to counterparty default',
            'Net Best Estimate of Claims Provisions',
            'Total Best estimate - gross', 
            'Total Best estimate - net',
            'Risk margin', 
            'Total technical provisions',
            'Technical provisions - total',
            'Recoverable from reinsurance contract/SPV and Finite Re after the adjustment for expected losses due to counterparty default - total',
            'Technical provisions minus recoverables from reinsurance/SPV and Finite Re - total'
        ]

        # Transpose data from QRT
        df = pd.DataFrame(data)[1:].transpose()
        
        # Find column names
        headerCol = 0
        codes_present = False
        for index, row in df.iterrows():
            codes_present = row.map(lambda x: 'R01' in str(x)).any()
            if codes_present:
                headerCol = index
                break
        if not codes_present:
            for index, row in df.iterrows():
                present = row.map(lambda x: 'provision' in str(x).lower()).any()
                if present:
                    headerCol = index
                    break
        df = df[headerCol:]
        df.columns = df.iloc[0]
        df = df[1:]

        # Remove coded headers
        map_ = df.apply(lambda row: not(row.map(lambda x: 'R01' in str(x)).any()), axis=1)
        df = df.loc[map_]
        map_ = df.apply(lambda row: not(row.map(lambda x: 'C0' in str(x)).any()), axis=0)
        df = df.loc[:, map_.tolist()]

        # Implement standard QRT line labels
        if len(df.columns) > 19:
            map_ = df.columns.map(lambda x: (x not in ['', 'None', 'in EUR', 'in thousand EUR']) and (x is not None))
            df = df.loc[:, map_.tolist()]
        match len(df.columns):
            case 14:
                df.columns = lines14
            case 19:
                df.columns = lines19
        try:
            df = df.drop(['Technical provisions calculated as a sum of BE and RM', 'Best estimate', 'Premium provisions', 'Claims provisions', 'Total technical provisions'], axis=1)
        except KeyError:
            df = df.drop(['Technical provisions calculated as a sum of BE and RM', 'Best estimate', 'Premium provisions', 'Claims provisions', 'Total technical provisions'], axis=1, errors='ignore')

        # Clean up cell content to make numeric
        df = df.map(lambda x: re.sub('[ +' + thousandseparator + ']', '', str(x)))

        # Implement standard QRT LoBs and add company and year
        df = df.reset_index(drop=True)
        df['Company'] = company
        df['Year'] = year

        # split merged cell contents
        for row_index, row in df.iterrows():
            for column_index in range(len(row)):
                if '\n' in str(row.iloc[column_index]):
                    cell_lines = str(row.iloc[column_index]).split('\n')
                    for line_counter in range(len(cell_lines)):
                        df.iloc[row_index, column_index+line_counter] = cell_lines[line_counter]
        
        return df