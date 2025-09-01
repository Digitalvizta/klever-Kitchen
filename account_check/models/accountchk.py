def action_confirm(self):
    self.ensure_one()

    # TODO used to get correct ir properties
    self = self.with_context(
        company_id=self.company_id.id,
        force_company=self.company_id.id,
    )

    for check in self.env['account.check'].browse(self._context.get('active_ids', [])):
        self.validate_action(self.action_type, check)
        vals = self.get_vals(self.action_type, check, self.date)

        aml_obj = self.env['account.move.line'].with_context(check_move_validity=False)
        currency = check.voucher_id.currency_id
        price_subtotal = check.amount

        if currency and currency != check.company_id.currency_id:

            balance = currency._convert(check.amount, check.company_id.currency_id, check.company_id,
                                        date=check.payment_date)
            amount_currency = price_subtotal
            debit = balance > 0.0 and balance or 0.0
            credit = balance < 0.0 and -balance or 0.0
            currency_id = currency.id

        else:
            amount_currency = 0.0
            debit = price_subtotal > 0.0 and price_subtotal or 0.0
            credit = price_subtotal < 0.0 and -price_subtotal or 0.0
            currency_id = False

        # extraemos los vals
        move_vals = vals.get('move_vals', {})
        debit_line_vals = vals.get('debit_line_vals', {})
        debit_line_vals.update({'debit': debit, 'credit': credit, 'amount_currency': amount_currency or False,
                                'currency_id': currency_id})
        credit_line_vals = vals.get('credit_line_vals', {})
        credit_line_vals.update({'debit': credit, 'credit': debit, 'amount_currency': -1 * amount_currency or False,
                                 'currency_id': currency_id})
        check_move_field = vals.get('check_move_field')
        signal = vals.get('signal')
        move = self.env['account.move'].with_context({}).create(move_vals)
        debit_line_vals['move_id'] = move.id
        credit_line_vals['move_id'] = move.id
        # move.line_ids.with_context({}).create(debit_line_vals)
        aml_obj.create(debit_line_vals)
        # move.line_ids.with_context({}).create(credit_line_vals)
        aml_obj.create(credit_line_vals)
        check.write({check_move_field: move.id})

        check.state = signal
        move.post()

    return True
