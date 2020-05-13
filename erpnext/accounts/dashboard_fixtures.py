# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from erpnext import get_default_company

import frappe
import json


def get_data():
	data = frappe._dict({
		"dashboards": [],
		"charts": []
	})
	company = get_company_for_dashboards()
	if company:
		company_doc = frappe.get_doc("Company", company)
		data.dashboards = get_dashboards()
		data.charts = get_charts(company_doc)
	return data

def get_dashboards():
	return [{
		"name": "Accounts",
		"dashboard_name": "Accounts",
		"charts": [
			{ "chart": "Outgoing Bills (Sales Invoice)" },
			{ "chart": "Incoming Bills (Purchase Invoice)" },
			{ "chart": "Bank Balance" },
			{ "chart": "Income" },
			{ "chart": "Expenses" }
		]
	}]

def get_charts(company):
	income_account = company.default_income_account or get_account("Income Account", company.name)
	expense_account = company.default_expense_account or get_account("Expense Account", company.name)
	bank_account = company.default_bank_account or get_account("Bank", company.name)

	return [
		{
			"doctype": "Dashboard Chart",
			"time_interval": "Quarterly",
			"name": "Income",
			"chart_name": "Income",
			"timespan": "Last Year",
			"color": None,
			"filters_json": json.dumps({"company": company.name, "account": income_account}),
			"source": "Account Balance Timeline",
			"chart_type": "Custom",
			"timeseries": 1,
			"owner": "Administrator",
			"type": "Line"
		},
		{
			"doctype": "Dashboard Chart",
			"time_interval": "Quarterly",
			"name": "Expenses",
			"chart_name": "Expenses",
			"timespan": "Last Year",
			"color": None,
			"filters_json": json.dumps({"company": company.name, "account": expense_account}),
			"source": "Account Balance Timeline",
			"chart_type": "Custom",
			"timeseries": 1,
			"owner": "Administrator",
			"type": "Line"
		},
		{
			"doctype": "Dashboard Chart",
			"time_interval": "Quarterly",
			"name": "Bank Balance",
			"chart_name": "Bank Balance",
			"timespan": "Last Year",
			"color": "#ffb868",
			"filters_json": json.dumps({"company": company.name, "account": bank_account}),
			"source": "Account Balance Timeline",
			"chart_type": "Custom",
			"timeseries": 1,
			"owner": "Administrator",
			"type": "Line"
		},
		{
			"doctype": "Dashboard Chart",
			"time_interval": "Monthly",
			"name": "Incoming Bills (Purchase Invoice)",
			"chart_name": "Incoming Bills (Purchase Invoice)",
			"timespan": "Last Year",
			"color": "#a83333",
			"value_based_on": "base_grand_total",
			"filters_json": json.dumps({}),
			"chart_type": "Sum",
			"timeseries": 1,
			"based_on": "posting_date",
			"owner": "Administrator",
			"document_type": "Purchase Invoice",
			"type": "Bar"
		},
		{
			"doctype": "Dashboard Chart",
			"time_interval": "Monthly",
			"name": "Outgoing Bills (Sales Invoice)",
			"chart_name": "Outgoing Bills (Sales Invoice)",
			"timespan": "Last Year",
			"color": "#7b933d",
			"value_based_on": "base_grand_total",
			"filters_json": json.dumps({}),
			"chart_type": "Sum",
			"timeseries": 1,
			"based_on": "posting_date",
			"owner": "Administrator",
			"document_type": "Sales Invoice",
			"type": "Bar"
		}
	]

def get_account(account_type, company):
	accounts = frappe.get_list("Account", filters={"account_type": account_type, "company": company})
	if accounts:
		return accounts[0].name

def get_company_for_dashboards():
	company = get_default_company()
	if not company:
		company_list = frappe.get_list("Company")
		if company_list:
			company = company_list[0].name
	return company
