

def to_periodic_format(period):
    if period == 'Day':
        return 'daily'
    elif period == 'Week':
        return 'weekly'
    elif period == 'Month':
        return 'monthly'
    elif period == 'Year':
        return 'yearly'
    elif period == 'AllTime':
        return 'all time'
