from odoo import models, fields, api

class BalanceSheetReport(models.AbstractModel):
    _name = "report.custom_balance_sheet.balance_sheet_template"
    _description = "Balance Sheet Report"

    def _get_balance_sheet_data(self, date_from, date_to ):
        """Fetch balances from account_move_line and join to get account type and subtype information for assets, liabilities, and equity."""
        self.env.cr.execute("""
            SELECT aaw.code, aaw.name, aat.internal_group as account_type, 
                   aat.name as subtype_name,  -- Fetching subtype name
                   COALESCE(SUM(aml.debit), 0) AS total_debit,
                   COALESCE(SUM(aml.credit), 0) AS total_credit
            FROM account_move_line aml
            LEFT JOIN account_account aaw ON aml.account_id = aaw.id
            LEFT JOIN account_account_type aat ON aaw.user_type_id = aat.id
            WHERE aml.date BETWEEN %s AND %s
              AND aat.internal_group IN ('asset', 'liability', 'equity')
            GROUP BY aaw.code, aaw.name, aat.internal_group, aat.name
        """, (date_from, date_to))
        records = self.env.cr.fetchall()
        result = []

        for code, name, account_type, subtype_name, total_debit, total_credit in records:
            # Apply logic based on account type
            if account_type in ['asset' ]:
                balance = total_debit - total_credit
            elif account_type in [ 'liability', 'equity']:
                balance = total_credit - total_debit
            else:
                balance = 0

            result.append({
                'code': code,
                'name': name,
                'account_type': account_type,
                'subtype_name': subtype_name,
                'balance': round(balance,3),
            })
        result.sort(key=lambda x: x['subtype_name'])


        # records_per_page = [50] + [60] * ((len(result) - 50) // 60 + 1)
    
        # pages = []
        # start = 0
        # for count in records_per_page:
        #     if start >= len(result):
        #         break
        #     pages.append(result[start:start + count])
        #     start += count

        # pages = [result[i:i + records_per_page] for i in range(0, len(result), records_per_page)]
        return result

    @api.model
    def _get_report_values(self, docids, data=None):
        """Return data to the report template"""


        wizard = self.env['balance.sheet.wizard'].browse(docids)
        date_from = wizard.date_from
        date_to = wizard.date_to
        balance_data = self._get_balance_sheet_data(date_from, date_to)

        # Flatten the list to calculate totals
        all_records = [item for page in balance_data for item in page]

        total_assets = sum(row['balance'] for row in balance_data if row['account_type'] == 'asset') or 0
        total_liabilities = sum(row['balance'] for row in balance_data if row['account_type'] == 'liability') or 0
        total_equity = sum(row['balance'] for row in balance_data if row['account_type'] == 'equity') or 0
        total_liab_equity = total_assets + total_liabilities

        # print("??????????????????????????????????????????????????????????????????????")
        # print("??????????????????????????????????????????????????????????????????????")
        # print("??????????????????????????????????????????????????????????????????????")
        # print(total_assets)
        # print(total_liabilities)
        # print(total_equity)
        # print(total_liab_equity)



        return {
            'doc_ids': docids,
            'doc_model': 'balance.sheet.wizard',
            'docs': wizard,
            'date_from': date_from,
            'date_to': date_to,
            'balance_data': balance_data,
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'total_equity': total_equity,
            'total_liab_equity': total_liab_equity,
        }
