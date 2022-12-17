week = 50
weekList = [week, week+1, week+2, week+3, week+4]
weekList = [week if week <= 52 else week - 52 for week in weekList]
print(weekList)