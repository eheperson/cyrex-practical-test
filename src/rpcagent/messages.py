import proto.rpc_signin_user_pb2 as rpc_signin_user
import proto.rpc_create_vacancy_pb2 as rpc_create_vacancy
import proto.rpc_update_vacancy_pb2 as rpc_update_vacancy
import proto.vacancy_service_pb2 as vacancy_service


class Messages:
    @classmethod
    def signInUser(cls, email, password):
        return rpc_signin_user.SignInUserInput(
            email=email,
            password=password
        )

    @classmethod
    def createVacancy(cls, country, description, division, title):
        return rpc_create_vacancy.CreateVacancyRequest(
            Country=country,
            Description=description,
            Division=division,
            Title=title
        )
    
    @classmethod
    def getVacancy(cls, id):
        return vacancy_service.VacancyRequest(
            Id=id
        )
    
    @classmethod
    def getVacancies(cls, page:int=None, limit:int=None):
        message = vacancy_service.GetVacanciesRequest()

        if limit != None:
            message.limit = limit
        if page != None:
            message.page = page

        return message

    @classmethod
    def updateVacancy(cls, id:str=None, country:str=None, description:str=None, division:int=None, title:str=None, views:int=None):
        message = rpc_update_vacancy.UpdateVacancyRequest()

        if id==None:
            return "id cannot be null, must be a string"
        
        if division != None:
            if division<0 or division>3:
                return "division must be between 0 - 3"

        message.Id = id

        if country != None:
            message.Country = country
        
        if description != None:
            message.Description = description

        if division != None:
            message.Division = division

        if title != None:
            message.Title = title

        if views != None:
            message.Views = views

        return message

    @classmethod
    def deleteVacancy(cls, id):
        return vacancy_service.VacancyRequest(
            Id=id
        )