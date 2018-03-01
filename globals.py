class mpi:
	getChannel = None
	getProgramRank = None
	getChannelTrend = None
	filters = None
	quickcharts = None
	channel_ids = []
	
	time_period_list = [
		'currentMonth',
		'currentQuarter',
		'YTD',
		'previousMonth',
		'previousQuarter',
		'previousYear',
		'last12Month'
	]
	
	isAttribution_dict = {
	  'Successes': ['false'],
	  'New Names': ['false'],
	  '{"First-Touch":["New Opportunities"]}': ['false'],
	  '{"First-Touch":["Pipeline Created"]}': ['false'],
	  '{"First-Touch":["Pipeline Open"]}': ['false'],
	  '{"First-Touch":["Expected Revenue"]}': ['false'],
	  '{"Multi-Touch":["New Opportunities"]}': ['false'],
	  '{"Multi-Touch":["Pipeline Created"]}': ['false'],
	  '{"Multi-Touch":["Pipeline Open"]}': ['false'],
	  '{"Multi-Touch":["Expected Revenue"]}': ['false'],
	  '{"First-Touch":["Opportunities Won"]}': ['false'],
	  '{"First-Touch":["Revenue Won"]}': ['false'],
	  '{"Multi-Touch":["Opportunities Won"]}': ['false'],
	  '{"Multi-Touch":["Revenue Won"]}': ['false'],
	  '{"First-Touch":["Cost Per Opportunity Created"]}': ['false', 'true'],
	  '{"First-Touch":["Pipeline Created to Cost Ratio"]}': ['false', 'true'],
	  '{"Multi-Touch":["Cost Per Opportunity Created"]}': ['false', 'true'],
	  '{"Multi-Touch":["Pipeline Created to Cost Ratio"]}': ['false', 'true'],
	  '{"First-Touch":["Cost Per Opportunity Won"]}': ['false', 'true'],
	  '{"First-Touch":["Revenue Won to Cost Ratio"]}': ['false', 'true'],
	  '{"Multi-Touch":["Cost Per Opportunity Won"]}': ['false', 'true'],
	  '{"Multi-Touch":["Revenue Won to Cost Ratio"]}': ['false', 'true']
	}
	
	settings_dict = {
	  'Successes': {
	    None: 'n/a'
	  },
	  'New Names': {
	    None: 'n/a'
	  },
	  '{"First-Touch":["New Opportunities"]}': {
	    None: '{"Before Opportunity Created":[]}',
	    '{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
	    '{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
	    '{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}'
	  },
	  '{"First-Touch":["Pipeline Created"]}': {
	    None: '{"Before Opportunity Created":[]}',
	    '{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
	    '{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
	    '{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}'
	  },
	  '{"First-Touch":["Pipeline Open"]}': {
	    None: '{"Before Opportunity Created":[]}',
	    '{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
	    '{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
	    '{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}'
	  },
	  '{"First-Touch":["Expected Revenue"]}': {
	    None: '{"Before Opportunity Created":[]}',
	    '{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
	    '{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
	    '{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}'
	  },
	  '{"First-Touch":["Cost Per Opportunity Created"]}': {
	    None: '{"Before Opportunity Created":[]}',
	    '{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
	    '{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
	    '{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}'
	  },
	  '{"First-Touch":["Pipeline Created to Cost Ratio"]}': {
	    None: '{"Before Opportunity Created":[]}',
	    '{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
	    '{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
	    '{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}'
	  },
	  '{"Multi-Touch":["New Opportunities"]}': {
	    None: '{"Before Opportunity Created":[]}',
	    '{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
	    '{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
	    '{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}'
	  },
	  '{"Multi-Touch":["Pipeline Created"]}': {
	    None: '{"Before Opportunity Created":[]}',
	    '{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
	    '{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
	    '{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}'
	  },
	  '{"Multi-Touch":["Pipeline Open"]}': {
	    None: '{"Before Opportunity Created":[]}',
	    '{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
	    '{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
	    '{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}'
	  },
	  '{"Multi-Touch":["Expected Revenue"]}': {
	    None: '{"Before Opportunity Created":[]}',
	    '{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
	    '{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
	    '{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}'
	  },
	  '{"Multi-Touch":["Cost Per Opportunity Created"]}': {
	    None: '{"Before Opportunity Created":[]}',
	    '{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
	    '{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
	    '{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}'
	  },
	  '{"Multi-Touch":["Pipeline Created to Cost Ratio"]}': {
	    None: '{"Before Opportunity Created":[]}',
	    '{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
	    '{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
	    '{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}'
	  },
	  '{"First-Touch":["Opportunities Won"]}': {
	    None: '{"Before Opportunity Closed":[]}',
	    '{"Before Opportunity Closed":["Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}',
	    '{"Before Opportunity Closed":["Show First-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}',
	    '{"Before Opportunity Closed":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}'
	  },
	  '{"First-Touch":["Revenue Won"]}': {
	    None: '{"Before Opportunity Closed":[]}',
	    '{"Before Opportunity Closed":["Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}',
	    '{"Before Opportunity Closed":["Show First-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}',
	    '{"Before Opportunity Closed":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}'
	  },
	  '{"First-Touch":["Cost Per Opportunity Won"]}': {
	    None: '{"Before Opportunity Closed":[]}',
	    '{"Before Opportunity Closed":["Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}',
	    '{"Before Opportunity Closed":["Show First-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}',
	    '{"Before Opportunity Closed":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}'
	  },
	  '{"First-Touch":["Revenue Won to Cost Ratio"]}': {
	    None: '{"Before Opportunity Closed":[]}',
	    '{"Before Opportunity Closed":["Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}',
	    '{"Before Opportunity Closed":["Show First-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}',
	    '{"Before Opportunity Closed":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}'
	  },
	  '{"Multi-Touch":["Opportunities Won"]}': {
	    None: '{"Before Opportunity Closed":[]}',
	    '{"Before Opportunity Closed":["Show First-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}',
	    '{"Before Opportunity Closed":["Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}',
	    '{"Before Opportunity Closed":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}'
	  },
	  '{"Multi-Touch":["Revenue Won"]}': {
	    None: '{"Before Opportunity Closed":[]}',
	    '{"Before Opportunity Closed":["Show First-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}',
	    '{"Before Opportunity Closed":["Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}',
	    '{"Before Opportunity Closed":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}'
	  },
	  '{"Multi-Touch":["Cost Per Opportunity Won"]}': {
	    None: '{"Before Opportunity Closed":[]}',
	    '{"Before Opportunity Closed":["Show First-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}',
	    '{"Before Opportunity Closed":["Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}',
	    '{"Before Opportunity Closed":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}'
	  },
	  '{"Multi-Touch":["Revenue Won to Cost Ratio"]}': {
	    None: '{"Before Opportunity Closed":[]}',
	    '{"Before Opportunity Closed":["Show First-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}',
	    '{"Before Opportunity Closed":["Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}',
	    '{"Before Opportunity Closed":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}'
	  }
	}