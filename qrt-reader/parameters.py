class Parameters():
   
    AVAILABLE_QRTS = [
        'S.05.01.02.01 (part 1)', 
        'S.05.01.02.01 (part 2)', 
        'S.05.01.02.01 (single table)',
        'S.17.01.02.01 (part 1)', 
        'S.17.01.02.01 (part 2)', 
        'S.17.01.02.01 (single table)'
    ]

    FILENAME_MASKS = {
        'AG': 'AG',
        'AXA': 'AXA',
        'P&V': 'PV',
        'Baloise': 'Baloise'
    }

    TABLE_STRATEGIES = {
        'tables': {
            'AG': {'horizontal_strategy': 'text', 'vertical_strategy': 'text', 'snap_tolerance': 5},
            'AXA': {'horizontal_strategy': 'lines', 'vertical_strategy': 'lines', 'snap_y_tolerance': 5},
            'P&V':{'horizontal_strategy': 'text', 'vertical_strategy': 'text', 'snap_tolerance': 5}
        },
        'cells':{
            'AG': {'horizontal_strategy': 'text', 'vertical_strategy': 'lines'},
            'AXA': {'vertical_strategy': 'lines', 'snap_x_tolerance': 10},
            'P&V': {'horizontal_strategy': 'lines', 'vertical_strategy': 'text', 'min_words_vertical': 10, 'snap_x_tolerance': 20}
        }
    }

    def company_tablestrategy(self, company):
        return self.TABLE_STRATEGIES['tables'][company]
    
    def company_cellstrategy(self, company, table_bbox, page, qrt):
        combined_strategy = self.TABLE_STRATEGIES['cells'][company]

        if company == 'AXA' and qrt == 'S.05.01.02 (part 1)':
            horizontal_lines_list = []
            line_strategy = combined_strategy
            line_strategy.update({'horizontal_strategy': 'lines', 'join_y_tolerance': 5, 'snap_y_tolerance': 5})
            horizontal_lines_box = page.crop((table_bbox[0]+70, table_bbox[1], table_bbox[0]+90, table_bbox[3]))
            if horizontal_lines_box.lines != []:
                for line in horizontal_lines_box.lines:
                    if line['height'] < 2: # horizontal lines only
                        horizontal_lines_list.append(line['top'])
            else: # fallback for 2022 AXA format
                horizontal_lines_table = horizontal_lines_box.find_table(table_settings=line_strategy)
                for row in horizontal_lines_table.rows:
                    horizontal_lines_list.append(row.bbox[1])
            horizontal_lines_list.append(table_bbox[1])
            horizontal_lines_list.append(table_bbox[3])
            combined_strategy.update({'horizontal_strategy': 'explicit', 'explicit_horizontal_lines': horizontal_lines_list})

        combined_strategy.update({'explicit_vertical_lines': [table_bbox[0], table_bbox[2]]})

        return combined_strategy
