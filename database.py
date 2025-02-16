from sqlalchemy.orm import Session
from sqlalchemy import MetaData, create_engine, Table, insert, delete
import pandas as pd
from dto import S050102

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
    
    def update_s050102(self, records):
        insert_list = []
        for i, record in records.iterrows():
            insert_list.append(
                S050102(
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
            stmt = delete(S050102).where(S050102.Company == records.loc[0, 'Company']).where(S050102.Year == records.loc[0, 'Year']).where(S050102.LoB.in_(records['LoB'].values.tolist()))
            session.execute(stmt)
            session.add_all(insert_list)
            session.commit()