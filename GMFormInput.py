import xlrd

class GMFormInput():
	"""
	This class gets the important information for a row in the Input spreadsheet.
	"""
	def __init__(self):
		super(GMFormInput, self).__init__()

	def GMFormInput(self, row, filename):
		loc = filename		
		
		wb = xlrd.open_workbook(loc)		#open excel sheet
		sheet = wb.sheet_by_index(0)		
		# pathname = sheet.cell_value(row,4)     	#Takes each cell from the sheet
		scenario = sheet.cell_value(row,1)
		subgoal = sheet.cell_value(row,2)
		action = sheet.cell_value(row,3)
		url = sheet.cell_value(row, 4)   
		return scenario.lower(), subgoal.lower(), action.lower(), url

	# Fetch "before" action for the current URL
	def before_action(self, row, filename):
		loc = filename		
		
		wb = xlrd.open_workbook(loc)		#open excel sheet
		sheet = wb.sheet_by_index(0)		
		action = sheet.cell_value(row,3)   
		return action.lower()

	# Fetch "after" action for the current URL
	def before_pathname(self, row):
		loc = ('ID_input.xlsx')			
		
		wb = xlrd.open_workbook(loc)		#open excel sheet
		sheet = wb.sheet_by_index(0)		
		action = sheet.cell_value(row,4)   
		return action.lower()

	# Fetch keywords for the "before" action for the current URL
	def before_action_keywords(self, row):
		loc = ('ID_input.xlsx')			
		
		wb = xlrd.open_workbook(loc)		#open excel sheet
		sheet = wb.sheet_by_index(0)		
		keywords = sheet.cell_value(row,6)   
		return keywords
