import datetime



class Helpers():


    def is_int_in_range(self,value, min=None, max=None):
        """
            - Permet de determiner si un nombre est entier
        """
        try:
            int_value = int(value)
        except ValueError:
            return False
        if min is not None and int_value < min:
            return False
        if max is not None and int_value > max:
            return False
        
        return True

    def is_float_in_range(self,value, min=None, max=None):
        """Permet de determiner si un nombre est entier"""
        try:
            float_value = float(value)
        except ValueError:
            return False
            
        if min is not None and float_value < min:
            return False
        if max is not None and float_value > max:
            return False

        return True


    def get_date(self):
        today = datetime.date.today()
        # print(today)  # prints the current date (e.g. 2022-01-09)
        return today

    def get_datetime(self):
        now = datetime.datetime.now()
        current_time = now.time().strftime('%Y-%m-%d %H:%M:%S')
        # print(current_time)  # prints the current time (e.g. 14:32:10.354865)
        return current_time
