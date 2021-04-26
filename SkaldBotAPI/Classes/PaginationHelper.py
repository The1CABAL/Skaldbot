from Models.Models import *

class PaginationHelper():
    """Take in the response args and set the pagination values"""
    def __init__(self, args, defaultOrderBy, allowedOrderBy):
        self.OrderBy = args.get('OrderBy')
        self.PerPage = args.get('PerPage')
        self.SearchTerm = args.get('SearchTerm')
        self.CurrentPage = args.get('CurrentPage')
        self.TotalPages = args.get('TotalPages')
        self.IsAscending = args.get('IsAscending')

        if (self.IsAscending.lower() == "true"):
            self.IsAscending = "1"
        else:
            self.IsAscending = "0"

        if (self.OrderBy == None or self.OrderBy == '' or self.OrderBy not in allowedOrderBy):
            self.OrderBy = defaultOrderBy

    def getModel(self):
         return PaginationModel(self.OrderBy, self.PerPage, self.SearchTerm, self.CurrentPage, self.TotalPages, self.IsAscending)

    def replaceParams(self, sql):
        model = self.getModel();

        sql = sql.replace("@SortColumn", model[0])
        sql = sql.replace("@MaxRows", model[1])
        sql = sql.replace("@SearchTerm", str(model[2]))
        sql = sql.replace("@CurrentPage", model[3])
        sql = sql.replace("@Ascending", model[5])

        return sql