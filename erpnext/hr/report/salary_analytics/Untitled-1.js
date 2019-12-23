//Check out date validation on check out date change
frappe.ui.form.on('Opportunity Item', {
    check_out_date: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (row.check_out_date < row.check_in_date) {
            msgprint('Check out date is before Check in date, please amend to continue');
            validated = false;
        }
    }
});

//Check out date validation on days change
frappe.ui.form.on('Opportunity Item', {
    days: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (row.check_out_date < row.check_in_date) {
            msgprint('Check out date is before Check in date, please amend to continue');
            validated = false;
        }
    }
});

//Days Calculation on Check out date change
frappe.ui.form.on('Opportunity Item', {
    check_out_date: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (row.check_out_date > row.check_in_date) {
            frappe.model.set_value(cdt, cdn, 'days', frappe.datetime.get_day_diff(row.check_out_date,row.check_in_date));
            frappe.model.set_value(cdt, cdn, 'qty', row.days * row.units);            
            frm.fields_dict["days"].grid.grid_rows_by_docname[cdn].days.refresh();
        }
    }
});

//Days Calculation on Check in date change
frappe.ui.form.on('Opportunity Item', {
    check_in_date: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (row.check_out_date > row.check_in_date) {
            frappe.model.set_value(cdt, cdn, 'days', frappe.datetime.get_day_diff(row.check_out_date,row.check_in_date));
            frappe.model.set_value(cdt, cdn, 'qty', row.days * row.units);
            frm.fields_dict["days"].grid.grid_rows_by_docname[cdn].days.refresh();
        }
    }
});

//Check out date Calculation on Days change
frappe.ui.form.on('Opportunity Item', {
    days: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (row.check_out_date > row.check_in_date) {
            frappe.model.set_value(cdt, cdn, 'check_out_date', frappe.datetime.add_days(row.check_in_date,row.days));
            frappe.model.set_value(cdt, cdn, 'qty', row.days * row.units); 
            frm.fields_dict["check_out_date"].grid.grid_rows_by_docname[cdn].check_out_date.refresh();
        }
    }
});

//Check out date Calculation on Check in date change
frappe.ui.form.on('Opportunity Item', {
    check_in_date: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (row.check_out_date > row.check_in_date) {
            frappe.model.set_value(cdt, cdn, 'check_out_date', frappe.datetime.add_days(row.check_in_date,row.days));
            frappe.model.set_value(cdt, cdn, 'qty', row.days * row.units); 
            frm.fields_dict["check_out_date"].grid.grid_rows_by_docname[cdn].check_out_date.refresh();
        }
    }
});

//Qty Calculation on Days Change
frappe.ui.form.on('Opportunity Item', {
    days: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (row.days) {
            frappe.model.set_value(cdt, cdn, 'qty', row.days * row.units);
            frm.fields_dict["qty"].grid.grid_rows_by_docname[cdn].qty.refresh();
        }
    }
});

//Qty Calculation on Units Change
frappe.ui.form.on('Opportunity Item', {
    units: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (row.units) {
            frappe.model.set_value(cdt, cdn, 'qty', row.units * row.days);
            frm.fields_dict["qty"].grid.grid_rows_by_docname[cdn].qty.refresh();
        }
    }
});
