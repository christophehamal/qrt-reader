from sqlalchemy.orm import Session
from sqlalchemy import MetaData, create_engine, Table, insert, delete
import pandas as pd
from dto import S05010201, S17010201

class Database():

    DB = {
        'dev': {
            'driver': 'mysql+pymysql',
            'user': 'qrt',
            'pw': 'qrt',
            'url': 'localhost/qrt'
        }
    }

    def __init__(self):
        conn_str = '{}://{}:{}@{}'.format(self.DB['dev']['driver'], self.DB['dev']['user'], self.DB['dev']['pw'], self.DB['dev']['url'])
        self.engine = create_engine(conn_str,echo=True)
    
    def update_s05010201(self, records):
        insert_list = []
        for i, record in records.iterrows():
            insert_list.append(
                S05010201(
                    Company = record['Company'], 
                    Year = record['Year'],
                    LoB = record['LoB'],
                    R0110 = record.get('Premiums written: Gross - Direct Business', 0) if record.get('Premiums written: Gross - Direct Business', str(0)).isdigit() else 0,
                    R0120 = record.get('Premiums written: Gross - Proportional reinsurance accepted', 0) if record.get('Premiums written: Gross - Proportional reinsurance accepted', str(0)).isdigit() else 0,
                    R0130 = record.get('Premiums written: Gross - Non-proportional reinsurance accepted', 0) if record.get('Premiums written: Gross - Non-proportional reinsurance accepted', str(0)).isdigit() else 0,
                    R0140 = record.get("Premiums written: Reinsurers' share", 0) if record.get("Premiums written: Reinsurers' share", str(0)).isdigit() else 0,
                    R0200 = record.get('Premiums written: Net', 0) if record.get('Premiums written: Net', str(0)).isdigit() else 0,
                    R0210 = record.get('Premiums earned: Gross - Direct Business', 0) if record.get('Premiums earned: Gross - Direct Business', str(0)).isdigit() else 0,
                    R0220 = record.get('Premiums earned: Gross - Proportional reinsurance accepted', 0) if record.get('Premiums earned: Gross - Proportional reinsurance accepted', str(0)).isdigit() else 0,
                    R0230 = record.get('Premiums earned: Gross - Non-proportional reinsurance accepted', 0) if record.get('Premiums earned: Gross - Non-proportional reinsurance accepted', str(0)).isdigit() else 0,
                    R0240 = record.get("Premiums earned: Reinsurers' share", 0) if record.get("Premiums earned: Reinsurers' share", str(0)).isdigit() else 0,
                    R0300 = record.get('Premiums earned: Net', 0) if record.get('Premiums earned: Net', str(0)).isdigit() else 0,
                    R0310 = record.get('Claims incurred: Gross - Direct Business', 0) if record.get('Claims incurred: Gross - Direct Business', str(0)).isdigit() else 0,
                    R0320 = record.get('Claims incurred: Gross - Proportional reinsurance accepted', 0) if record.get('Claims incurred: Gross - Proportional reinsurance accepted', str(0)).isdigit() else 0,
                    R0330 = record.get('Claims incurred: Gross - Non-proportional reinsurance accepted', 0) if record.get('Claims incurred: Gross - Non-proportional reinsurance accepted', str(0)).isdigit() else 0,
                    R0340 = record.get("Claims incurred: Reinsurers' share", 0) if record.get("Claims incurred: Reinsurers' share", str(0)).isdigit() else 0,
                    R0400 = record.get('Claims incurred: Net', 0) if record.get('Claims incurred: Net', str(0)).isdigit() else 0,
                    R0410 = record.get('Changes in other technical provisions: Gross - Direct Business', 0) if record.get('Changes in other technical provisions: Gross - Direct Business', str(0)).isdigit() else 0,
                    R0420 = record.get('Changes in other technical provisions: Gross - Proportional reinsurance accepted', 0) if record.get('Changes in other technical provisions: Gross - Proportional reinsurance accepted', str(0)).isdigit() else 0,
                    R0430 = record.get('Changes in other technical provisions: Gross - Non-proportional reinsurance accepted', 0) if record.get('Changes in other technical provisions: Gross - Non-proportional reinsurance accepted', str(0)).isdigit() else 0,
                    R0440 = record.get("Changes in other technical provisions: Reinsurers'share", 0) if record.get("Changes in other technical provisions: Reinsurers'share", str(0)).isdigit() else 0,
                    R0500 = record.get('Changes in other technical provisions: Net', 0) if record.get('Changes in other technical provisions: Net', str(0)).isdigit() else 0,
                    R0550 = record.get('Expenses incurred', 0) if record.get('Expenses incurred', str(0)).isdigit() else 0,
                    R1210 = record.get('Other expenses', 0) if record.get('Other expenses', str(0)).isdigit() else 0,
                    R1300 = record.get('Total expenses', 0) if record.get('Total expenses', str(0)).isdigit() else 0
                )
            )
        with Session(self.engine) as session:
            stmt = delete(S05010201).where(S05010201.Company == records.loc[0, 'Company']).where(S05010201.Year == records.loc[0, 'Year']).where(S05010201.LoB.in_(records['LoB'].values.tolist()))
            session.execute(stmt)
            session.add_all(insert_list)
            session.commit()

    def update_s17010201(self, records):
        insert_list = []
        for i, record in records.iterrows():
            insert_list.append(
                S17010201(
                    Company = record['Company'], 
                    Year = record['Year'],
                    LoB = record['LoB'],
                    R0010 = record.get('Technical provisions calculated as a whole', 0) if record.get('Technical provisions calculated as a whole', str(0)).isdigit() else 0,
                    R0050 = record.get('Total Recoverables from reinsurance/SPV and Finite Re after the adjustment for expected losses due to counterparty default associated to TP calculated as a whole', 0) if record.get('Total Recoverables from reinsurance/SPV and Finite Re after the adjustment for expected losses due to counterparty default associated to TP calculated as a whole', str(0)).isdigit() else 0,
                    R0060 = record.get('Gross premium provisions', 0) if record.get('Gross', str(0)).isdigit() else 0,
                    R0140 = record.get('Total recoverable from reinsurance/SPV and Finite Re after the adjustment for expected losses due to counterparty default', 0) if record.get('Total recoverable from reinsurance/SPV and Finite Re after the adjustment for expected losses due to counterparty default', str(0)).isdigit() else 0,
                    R0150 = record.get('Net Best Estimate of Premium Provisions', 0) if record.get('Net Best Estimate of Premium Provisions', str(0)).isdigit() else 0,
                    R0160 = record.get('Gross claims provisions', 0) if record.get('Gross claims provisions', str(0)).isdigit() else 0,
                    R0240 = record.get('Total recoverable from reinsurance/SPV and Finite Re after the adjustment for expected\nlosses due to counterparty default', 0) if record.get('Total recoverable from reinsurance/SPV and Finite Re after the adjustment for expected\nlosses due to counterparty default', str(0)).isdigit() else 0,
                    R0250 = record.get('Net Best Estimate of Claims Provisions', 0) if record.get('Net Best Estimate of Claims Provisions', str(0)).isdigit() else 0,
                    R0260 = record.get('Total Best estimate - gross', 0) if record.get('Total Best estimate - gross', str(0)).isdigit() else 0,
                    R0270 = record.get('Total Best estimate - net', 0) if record.get('Total Best estimate - net', str(0)).isdigit() else 0,
                    R0280 = record.get('Risk margin', 0) if record.get('Risk margin', str(0)).isdigit() else 0,
                    R0320 = record.get('Technical provisions - total', 0) if record.get('Technical provisions - total', str(0)).isdigit() else 0,
                    R0330 = record.get('Recoverable from reinsurance contract/SPV and Finite Re after the adjustment for expected losses due to counterparty default - total', 0) if record.get('Recoverable from reinsurance contract/SPV and Finite Re after the adjustment for expected losses due to counterparty default - total', str(0)).isdigit() else 0,
                    R0340 = record.get('Technical provisions minus recoverables from reinsurance/SPV and Finite Re - total', 0) if record.get('Technical provisions minus recoverables from reinsurance/SPV and Finite Re - total', str(0)).isdigit() else 0,
                )
            )
        with Session(self.engine) as session:
            stmt = delete(S17010201).where(S17010201.Company == records.loc[0, 'Company']).where(S17010201.Year == records.loc[0, 'Year']).where(S17010201.LoB.in_(records['LoB'].values.tolist()))
            session.execute(stmt)
            session.add_all(insert_list)
            session.commit()