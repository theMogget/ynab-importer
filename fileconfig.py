multiplier_dict = {
	'name': 'multiplier',
	'truncate_pattern': 'Transaction Date',
	'mapping': {
	    'Transaction Date': 'date',
	    'Debit Amount': 'outflow',
	    'Credit Amount': 'inflow',
	    'Client Reference': 'payee'
	},
	'date_format': '%d %b %Y'
}


livefresh_dict = {
	'name': 'livefresh',
	'truncate_pattern': 'date',
	'mapping': {
	    'date': 'date',
	    'outflow': 'outflow',
	    'inflow': 'inflow',
	    'payee': 'payee'
	},
	'date_format': '%d %b %Y'
}