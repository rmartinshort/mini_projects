import datetime
from dateutil.relativedelta import relativedelta

class DateFinder(object):
    
    def __init__(self,year=None,month=None,quarter=None,day=None):
        
        if year and quarter:
            self.year = year + (quarter-1) // 4
        else:
            # Set to today's date
            today = datetime.date.today()
            self.year = today.year
            self.month = today.month
            self.day = today.day
            
        if quarter:
            self.quarter = (quarter-1) % 4 + 1
        if month:
            self.month = month
        if day:
            self.day = day
            
    @classmethod
    def from_today(cls):
        
        return cls()
        
    @classmethod
    def from_date(cls, date):
        
        if isinstance(date,str):
            date = datetime.datetime.strptime(date,"%Y-%m-%d")
            
        return cls(year=date.year, month=date.month,quarter=((date.month-1)//3)+1,day=date.day)
    
    def add_quarter(self, n):
        
        if isinstance(n,int):
            return DateFinder(self.year, month=None, quarter=self.quarter + n)
        else:
            raise ArithmeticError()
    
    def n_days_ago(self,n):
        
        if isinstance(n,int):
            return datetime.date(year=self.year,month=self.month,day=self.day) - relativedelta(days=n)
        else:
            raise ArithmeticError()
            
    def n_weeks_ago(self,n):
        
        if isinstance(n,int):
            return datetime.date(year=self.year,month=self.month,day=self.day) - relativedelta(weeks=n)
        else:
            raise ArithmeticError()
            
    def n_months_ago(self,n):
        
        if isinstance(n,int):
            return datetime.date(year=self.year,month=self.month,day=self.day) - relativedelta(months=n)
        else:
            raise ArithmeticError()
            
    def n_years_ago(self,n):
        
        if isinstance(n,int):
            return datetime.date(year=self.year,month=self.month,day=self.day) - relativedelta(years=n)
        else:
            raise ArithmeticError()
            
    def month_start_date(self):
        return datetime.date(year=self.year,month=self.month,day=1)
    
    def month_end_date(self):
        return datetime.date(year=self.year,month=self.month,day=1) + relativedelta(months=1) - datetime.timedelta(days=1)
    
    def quarter_start_date(self):
        return datetime.date(year=self.year, month=(self.quarter-1)*3+1, day=1)
    
    def quarter_end_date(self):
        return self.add_quarter(1).quarter_start_date() - datetime.timedelta(days=1)

    @staticmethod 
    def output_to_string(date_output):

        return datetime.datetime.strftime(date_output,format="%Y-%m-%d")
        
