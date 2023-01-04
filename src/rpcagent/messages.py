import proto.rpc_signin_user_pb2 as rpc_signin_user

class Messages:
    @classmethod
    def signinUser(cls, email, password):
        return rpc_signin_user.SignInUserInput(
            email=email,
            password=password
        )