import proto.rpc_signin_user_pb2 as rpc_signin_user
import proto.rpc_create_vacancy_pb2 as rpc_create_vacancy
import proto.rpc_update_vacancy_pb2 as rpc_update_vacancy
import proto.vacancy_service_pb2 as vacancy_service


class Messages:
    @classmethod
    def sign_in_user(cls, email:str, password:str):
        return rpc_signin_user.SignInUserInput(
            email=email,
            password=password
        )

    @classmethod
    def create_vacancy(cls, country:str, description:str, division:int, title:str):
        return rpc_create_vacancy.CreateVacancyRequest(
            Country=country,
            Description=description,
            Division=division,
            Title=title
        )
    
    @classmethod
    def get_vacancy(cls, id:str):
        return vacancy_service.VacancyRequest(
            Id=id
        )
    
    @classmethod
    def get_vacancies(cls, page:int=1, limit:int=1):
        message = vacancy_service.GetVacanciesRequest()
        message.limit = 10
        # message.page = page
        return message

    @classmethod
    def update_vacancy(cls, id:str=None, country:str=None, description:str=None, division:int=None, title:str=None, views:int=None):
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
    def delete_vacancy(cls, id:str):
        return vacancy_service.VacancyRequest(
            Id=id
        )